import cv2

"""
Break a given video to frames and store them in a list.
Return that list
"""
def break_video_to_frames(channel):
    cap = cv2.VideoCapture(channel)
    # Grab the current frame.
    check, vid = cap.read()

    counter = 0
    # Initialize the value  of check variable
    check = True
    # List of frames
    frame_list = []

    while (check == True):
        cv2.imwrite("frame%d.jpg" % counter, vid)
        # Check value is false and the last frame is None in the end of the video
        check, vid = cap.read()
        # Add each frame in the list
        frame_list.append(vid)
        counter += 1
    # Remove the last frame (None)
    frame_list.pop()
    return frame_list


"""
Change the number of frame in frame list
Return the number of frame
"""
def control(fingers, frame_number_on_video):
    # 0 -> stop video
    if fingers == 0:
        frame_number_on_video -= 1
    # Backword --> 3
    elif fingers == 3:
        frame_number_on_video -= 3
    # forword =-->  5
    elif fingers == 5:
        frame_number_on_video += 3

    return frame_number_on_video