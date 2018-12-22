import cv2
import numpy as np
from sklearn.metrics import pairwise

#Global variables
background = None
accumulated_weight = 0.02
#The corners of the rectangle 
roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600

"""
Calculate the average of the background value(pre-processing)
""" 
 #Average of the background value
def calc_accum_avg(frame,accumulated_weight):
    
    global background
    #Set the background to be a copy of the frame
    if background is None:
        background = frame.copy().astype("float")
        return None
    #If alpha is a higher value, average image tries to catch even very fast and short changes in the data
    #If it is lower value, average becomes sluggish and it won't consider fast changes in the input images
    cv2.accumulateWeighted(frame,background,accumulated_weight)

"""
Grabbed the hands segment from the region of interest.
In order to perform background subtraction, we first must â€œlearn; a model of the background.
Once learned, this background model is compared against the current image and then the known background parts ae 
subtracted away.
The object left after subtraction are presumably new foreground objects.
And then we can find the external contours from the image.
And find the extrem points.
frame - current frame
threshold_min - min threshold value
Return extrem points of the hand
"""
def segment(frame,threshold_min=25):
    #Removing noise
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN,(4,4))
    #Calculate the absolute difference between the background and the past and frame.
    diff = cv2.absdiff(background.astype("uint8"),frame)
    #Blur the background for better results 
    diff = cv2.GaussianBlur(diff,(7,7),1.5)
    ret, thresholded = cv2.threshold(diff,threshold_min,255,cv2.THRESH_BINARY)
    
    #Grab the external contours from the image.
    image,contours,hierarchy = cv2.findContours(thresholded.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #No contours
    if len(contours) == 0:
        return None
    else:
        #Grab the largest contours points
        hand_segment = max(contours,key=cv2.contourArea)
        
    return (thresholded,hand_segment)
        
"""
Count the fingers being held up.
The idea is this:
1)Find the extrem points in the hand
2)Then use their intersection to estimate the center of the hand.
3)Calculate the distance for the point further away from the center
4)Using that distance to create circle(Any points that are outside of the circle,those should be extended fingers)
Return the number of the fingers and procedures frames.
"""
def count_fingers(frame,thresholded,hand_segment):
    
    #Find the top, bottom, left , and right in the hand_segment with the extream points
    top = tuple(hand_segment[hand_segment[:, :, 1].argmin()][0])
    bottom = tuple(hand_segment[hand_segment[:, :, 1].argmax()][0])
    left = tuple(hand_segment[hand_segment[:, :, 0].argmin()][0])
    right = tuple(hand_segment[hand_segment[:, :, 0].argmax()][0])
    
    #Center of the hand is going to be halfway between the top and bottom and halfway between the left and right
    center_x = (left[0] + right[0]) // 2
    center_y = (top[1] + bottom[1]) // 2
    
    #Calculate the distance from the center to all the extreme points
    distance = pairwise.euclidean_distances([(center_x, center_y)], Y=[left, right, top, bottom])[0]
    max_distance = distance.max()
    
    #Create a circle with a 70% percent radius of the max in distance.(i found work wall on my hand)
    radius = int(0.7*max_distance)
    circumference = (2*np.pi*radius)
    
    #Set circular ROI
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    #Draw the circular ROI
    cv2.circle(circular_roi,(center_x,center_y),radius,255,10)
     #This then returns the cut out obtained using the mask on the thresholded hand image.
    circular_roi = cv2.bitwise_and(thresholded,thresholded,mask=circular_roi)
    
    #Grab all the contours in this circular region of interest.
    image,contours,hierarchy = cv2.findContours(circular_roi.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    counter = 0
    
    for cnt in contours:
        #Grab the bounding box of the contour.
        (x,y,w,h) = cv2.boundingRect(cnt)
        #Check if the contour region is in the right range
        out_of_wrist = ((center_y + (center_y*0.27)) > (y+h))
        
        #Check if the contour is outside the circumference
        limit_points = ((circumference*0.26) > cnt.shape[0])
        limit_points1 = ((circumference*0.04) < cnt.shape[0])
    
        if  out_of_wrist and limit_points and limit_points1:
            counter += 1
        if counter > 5:
            counter = 5
         
    #Visual the data(for debug use)
    visual_threshold = visual_data(thresholded,radius,circumference,center_x,center_y,x,y,w,h)
    frame = cv2.flip(frame, 1)
    visual_color = visual_data(frame,radius,circumference,center_x,center_y,x,y,w,h)
    return (counter,visual_threshold,visual_color)
       

"""
Visual all the calculates in the image.
hand - binary image of the hand
radius,circumference,center_x,center_y - use for draw the circle(also for debuging use) 
x,y,w,h - Draw rectangle around the contours 
"""
def visual_data(hand,radius,circumference,center_x,center_y,x,y,w,h):
    #Draw the circle and the center of the circle
    procedures = cv2.circle(hand, (center_x,center_y), radius,(0,255,0), thickness=4)
    cv2.circle(procedures, (center_x,center_y),5, (0,255,255), -1)
    #Draw boundingRect of the contours
    cv2.rectangle(procedures,(x,y),(x+w,y+h),(0,0,255),2)
    
    return procedures     
##########################################################################################################

cam = cv2.VideoCapture(0)
#Variables for save the output as a video on windows
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer_frame = cv2.VideoWriter('FingerCount.mp4',cv2.VideoWriter_fourcc(*'DIVX'),20,(width,height))
writer_visual_threshold = cv2.VideoWriter('VisualThreshold.mp4',cv2.VideoWriter_fourcc(*'DIVX'),20,(width,height))
writer_visual_color = cv2.VideoWriter('VisualColor.mp4',cv2.VideoWriter_fourcc(*'DIVX'),20,(width,height))
number_of_frame = 0

while True:
    
    ret,frame = cam.read()
    # flip the frame so that it is not the mirror view
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()
    
    #Grab the ROI from the frame in grar scale
    roi = frame[roi_top:roi_bottom,roi_right:roi_left]
    gray_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    #Blur and removing noise from ROI
    gray_roi = cv2.GaussianBlur(gray_roi,(7,7),3)
    gray_roi = cv2.morphologyEx(gray_roi, cv2.MORPH_OPEN,(4,4))
    #Calculate that background for 60 frames
    if number_of_frame < 60:
        calc_accum_avg(gray_roi,accumulated_weight)
        if number_of_frame <= 59:
            cv2.putText(frame_copy,'WAIT,GETTING BACKGROUND',(200,400),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.imshow('Finger Count',frame_copy)
    else:#After 60 frames
        #Segments the hand region
        hand = segment(gray_roi)
        
        if hand is not None:
            #threshold and hand segment
            thresholded, hand_segment = hand
            #Number of fingers and frames that show the procedures
            fingers, visual_threshold, visual_color = count_fingers(frame_copy.copy(),thresholded,hand_segment)      
            visual_color = cv2.flip(visual_color, 1)
            #Draw contours around real hand in live stream and the num
            cv2.drawContours(visual_color,[hand_segment + (roi_right,roi_top)],-1,(255,0,0),1)
            cv2.putText(frame_copy,str(fingers),(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(visual_color,str(fingers),(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.rectangle(visual_color,(roi_left,roi_top),(roi_right,roi_bottom),(0,0,255),5)
            cv2.imshow("Visual threshold",visual_threshold)
            cv2.imshow("Visual color",visual_color)
            
    cv2.rectangle(frame_copy,(roi_left,roi_top),(roi_right,roi_bottom),(0,0,255),5)
    
    number_of_frame += 1
    
    cv2.imshow("Finger Count", frame_copy)
    
    #Save the output
    writer_frame.write(frame_copy)
    #writer_visual_color.write(visual_color)
    #writer_visual_threshold.write(visual_threshold)

    #Close windows with Esc
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
        

cv2.destroyAllWindows()
writer_frame.release()
writer_visual_color.release()
writer_visual_threshold.release()
cam.release()
 
