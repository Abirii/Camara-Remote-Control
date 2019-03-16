import cv2

def draw_finger_number(frame,fingerCount):
    cv2.putText(frame,str(fingerCount),(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    

def draw_ROI(frame,roi_left,roi_top,roi_right,roi_bottom):
    cv2.rectangle(frame,(roi_left,roi_top),(roi_right,roi_bottom),(0,0,255),5)
    

#Visual the data(for debug use)    
def visual_data(hand,radius,center_x,center_y):
    #Draw the circle and the center of the circle
    procedures = cv2.circle(hand, (center_x,center_y), radius,(0,255,0), thickness=4)
    cv2.circle(procedures, (center_x,center_y),5, (0,255,255), -1)
    return procedures


def draw_manipulation(frame,fingers):
        cv2.putText(frame,"<< backwards",(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame,"Stop",(70,90),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame,"forward >>",(70,135),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame,"normal",(70,190),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        
        if fingers == 0:
            cv2.putText(frame,"Stop",(70,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        elif fingers == 1:
            cv2.putText(frame,"<< backwards",(70,45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        elif fingers == 2:
            cv2.putText(frame,"forward >>",(70,135),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        else:
            cv2.putText(frame,"normal",(70,190),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        
        cv2.imshow("CÎ¿ntrol",frame)
