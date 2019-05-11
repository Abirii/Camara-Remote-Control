import cv2
import segment
import draw
import fingerCount as cf
import videoManipulation as vm
import switchChannel as swc

# The corners of the rectangle
roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600
# Defult variables
number_of_frame = 0
frame_number_on_video = 0
fingers = -1;
cam = cv2.VideoCapture(0)
# List of frames



frame_list1 = vm.break_video_to_frames('channel1.mp4')
frame_list2 = vm.break_video_to_frames('channel2.mp4')
frame_list3 = vm.break_video_to_frames('channel3.mp4')
frame_list = frame_list1

all_channels = [frame_list1, frame_list2, frame_list3]
channels_index = 0

# variable for switch channel
lock = 0
counter_for_lock_channel = 1



while True:

    frame_number_on_video += 1
    # Start the video over and over
    if (frame_number_on_video >= len(frame_list) or frame_number_on_video <= 0):
        frame_number_on_video = 0

    ret, frame = cam.read()
    # flip the frame so that it is not the mirror view
    frame = cv2.flip(frame, 1)
    frame_copy = frame.copy()

    # Grab the ROI from the frame in grar scale
    roi = frame[roi_top:roi_bottom, roi_right:roi_left]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Blur and removing noise from ROI
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 3)
    gray_roi = cv2.morphologyEx(gray_roi, cv2.MORPH_OPEN, (4, 4))

    # Calculate that background for 40 frames
    if number_of_frame < 40:
        segment.calc_accum_avg(gray_roi)
        if number_of_frame <= 40:
            cv2.putText(frame_copy, 'WAIT,GETTING BACKGROUND', (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Finger Count', frame_copy)

    else:  # After 60 frames

        # Segments the hand region
        hand = segment.hand_segmentation(gray_roi)
        draw.manipulation(frame_list[frame_number_on_video], fingers)
        # draw channel number
        draw.channel_number(frame_list[frame_number_on_video],channels_index+1)


        if hand is not None:
            # threshold and hand segment
            thresholded, hand_segment = hand

            # Number of fingers and frames that show the procedures
            fingers, visual_threshold, visual_color = cf.count_fingers(frame_copy.copy(), thresholded, hand_segment)

            # if switch channel just work, lock the function for 20 frames
            counter_for_lock_channel += 1
            counter_for_lock_channel = swc.count_number_of_frames(counter_for_lock_channel)
            # every 20 frames open the lock for switch
            lock = swc.open_and_close_lock(counter_for_lock_channel,lock)

            if not lock:
                # switch and lock switch for 20 frames
                lock = swc.switch_recognition(thresholded, fingers)

                channels_index = swc.switch_channel(lock,channels_index, len(all_channels))
                frame_list = all_channels[channels_index]


            # Draw contours around real hand in live stream and the number of fingers
            visual_color = cv2.flip(visual_color, 1)
            cv2.drawContours(visual_color, [hand_segment + (roi_right, roi_top)], -1, (255, 0, 0), 1)
            draw.finger_number(frame_copy, fingers)
            draw.finger_number(visual_color, fingers)

            draw.ROI(visual_color, roi_left, roi_top, roi_right, roi_bottom)

            cv2.imshow("Visual threshold", visual_threshold)
            cv2.imshow("Visual color", visual_color)

            frame_number_on_video = vm.control(fingers, frame_number_on_video)

    draw.ROI(frame_copy, roi_left, roi_top, roi_right, roi_bottom)
    number_of_frame += 1



    cv2.imshow("Finger Count", frame_copy)

    # Close windows with Esc
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cam.release()