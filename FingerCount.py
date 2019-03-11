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
        center_y  = (top[1] + bottom[1]) // 2 + 20
        
        #Calculate the distance from the center to all the extreme points
        distance = pairwise.euclidean_distances([(center_x, center_y)], Y=[left, right, top, bottom])[0]
        max_distance = distance.max()
        
        #Create a circle with a 70% percent radius of the max in distance.(i found work wall on my hand)
        radius = int(0.65*max_distance)
        
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
            
            limit_points1 = cnt.shape[0] < 90
            limit_points2 = cnt.shape[0] > 20
            
            #Check if the contour region is in the right range
            out_of_wrist = (center_y + center_y*0.20)  > y+h
            
            
            if  out_of_wrist and limit_points1 and limit_points2:
                counter += 1
            if counter > 5:
                counter = 5
                
             
        #Visual the data(for debug use)
        visual_threshold = visual_data(thresholded,radius,center_x,center_y,x,y,w,h)
        frame = cv2.flip(frame, 1)
        visual_color = visual_data(frame,radius,center_x,center_y,x,y,w,h)
        return (counter,visual_threshold,visual_color)
         
    #Visual the data(for debug use)
    visual_threshold = visual_data(thresholded,radius,center_x,center_y,x,y,w,h)
    frame = cv2.flip(frame, 1)
    visual_color = visual_data(frame,radius,center_x,center_y,x,y,w,h)
    return (counter,visual_threshold,visual_color)
       

"""
Visual all the calculates in the image.
hand - binary image of the hand
radius,center_x,center_y - use for draw the circle(also for debuging use) 
x,y,w,h - Draw rectangle around the contours 
"""
def visual_data(hand,radius,center_x,center_y,x,y,w,h):
    #Draw the circle and the center of the circle
    procedures = cv2.circle(hand, (center_x,center_y), radius,(0,255,0), thickness=4)
    cv2.circle(procedures, (center_x,center_y),5, (0,255,255), -1)
    #Draw boundingRect of the contours
    cv2.rectangle(procedures,(x,y),(x+w,y+h),(0,0,255),2)
    
    return procedures     


"""
Break a given video to frames and store them in a list.
Return that list
"""
def break_video_to_frames():
    cap = cv2.VideoCapture('TestVideo.mp4')
    check , vid = cap.read()
    # Grab the current frame. 
    check , vid = cap.read()
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    counter = 0
    #Initialize the value  of check variable
    check = True
    #List of frames
    frame_list = []
  
    while(check == True):
        cv2.imwrite("frame%d.jpg" %counter , vid) 
        #Check value is false and the last frame is None in the end of the video 
        check,vid = cap.read() 
        #Add each frame in the list
        frame_list.append(vid)
        counter += 1
    #Remove the last frame (None)
    frame_list.pop() 
    return frame_list,width,height
    
"""
Change the number of frame in frame list
Return the number of frame
"""
def control(finger,frame_number_on_video):
    # 0 -> stop video
    if fingers == 0:
        frame_number_on_video -= 1
    #Backword
    elif fingers == 1:
        frame_number_on_video -= 3
    elif fingers == 2:
        frame_number_on_video += 3
  
    
    return frame_number_on_video
      
        
######################################################################################################################################

cam = cv2.VideoCapture(0)
#List of frames from the video
frame_list,width_video,height_video = break_video_to_frames()
#Variables for save the output as a video on windows
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer_frame = cv2.VideoWriter('FingerCount.mp4',cv2.VideoWriter_fourcc(*'DIVX'),20,(width,height))
writer_video = cv2.VideoWriter('ControlledVideo.mp4',cv2.VideoWriter_fourcc(*'DIVX'),20,(width_video,height_video))

#Defult variables
number_of_frame = 0
frame_number_on_video = 0
fingers = -1;
while True:   
    
    frame_number_on_video += 1
    #Start the video over and over
    if (frame_number_on_video >= len(frame_list) or frame_number_on_video <= 0):
        frame_number_on_video = 0
        
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
        #The cÎ¿ntroled video
        cv2.putText(frame_list[frame_number_on_video],"<< backwards",(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame_list[frame_number_on_video],"Stop",(70,90),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame_list[frame_number_on_video],"forward >>",(70,135),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame_list[frame_number_on_video],"normal",(70,190),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        
        if fingers == 0:
            cv2.putText(frame_list[frame_number_on_video],"Stop",(70,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        elif fingers == 1:
            cv2.putText(frame_list[frame_number_on_video],"<< backwards",(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        elif fingers == 2:
            cv2.putText(frame_list[frame_number_on_video],"forward >>",(70,135),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        else:
            cv2.putText(frame_list[frame_number_on_video],"normal",(70,190),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        
        writer_video.write(frame_list[frame_number_on_video])
        cv2.imshow("CÎ¿ntrol",frame_list[frame_number_on_video])
        
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
            frame_number_on_video = control(fingers,frame_number_on_video)
        
    cv2.rectangle(frame_copy,(roi_left,roi_top),(roi_right,roi_bottom),(0,0,255),5)
    
    number_of_frame += 1
    
    cv2.imshow("Finger Count", frame_copy)
    
   
    #Save the output
    writer_frame.write(frame_copy)
    
  
    #Close windows with Esc
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
writer_frame.release()
writer_video.release()
cam.release()
 
