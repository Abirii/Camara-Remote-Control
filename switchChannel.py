import cv2
import masks

OPEN_LOCK = 35
RESTART = 1

current_channel = 'current'
all_channels_index = 0


""" switch recognition:
return -1 for previous channel ->  and lock the funcion for 20 frames
return 1 for next channel -> and lock the funcion for 20 frames
return 0 for current channel
"""
def switch_recognition(frame,number_of_fingers):

    switch_channel_image = masks.for_switch_channel(frame)

    contours, hierarchy = cv2.findContours(switch_channel_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    number_of_fingers_limit = number_of_fingers == 0 or number_of_fingers == 1 or number_of_fingers == 2

    counter = 0
    for cnt in contours:

        # check the side of the cnt (left or right) by boundingRect x coordinate
        x, _, _, _ = cv2.boundingRect(cnt)

        if cnt.shape[0] > 20 and cnt.shape[0] < 80 and number_of_fingers_limit:
            counter += 1

            current_channel = hand_side(x)

    if counter >= 1:
        if current_channel == 'next':
            return 1
        elif current_channel == 'previous':
            return -1
        else:
            return 0

"""" 
check the side of the contour
coordinate - x coordinate 
counter - number of cnt
"""
def hand_side(coordinate):

    # left side
    if coordinate <= 1:
        return 'previous'
    # right side
    return 'next'



""" get next or previous index in channel list """
def switch_channel(channel, channels_index, all_channels):

    if channel == -1:
        channels_index -= 1
        if channels_index < 0:
            channels_index = all_channels - 1


    elif channel == 1:
        channels_index += 1
        if channels_index > all_channels - 1:
            channels_index = 0

    return channels_index





""" restart the counter in OPEN_LOCK frame"""
def count_number_of_frames(counter_for_lock_channel):

    if counter_for_lock_channel == OPEN_LOCK or counter_for_lock_channel == 1:
        return 1
    return counter_for_lock_channel

""" open the lock every OPEN_LOCK(20) frames """
def open_and_close_lock(counter_for_lock_channel, lock):
    if counter_for_lock_channel == 1:
        return False
    return lock

