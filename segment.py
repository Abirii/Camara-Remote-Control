import cv2

background = None

"""
Calculate the average of the background value(pre-processing)
"""


# Average of the background value
def calc_accum_avg(frame, accumulated_weight=0.02):
    global background
    # Set the background to be a copy of the frame
    if background is None:
        background = frame.copy().astype("float")
        return None
    # If alpha is a higher value, average image tries to catch even very fast and short changes in the data
    # If it is lower value, average becomes sluggish and it won't consider fast changes in the input images
    cv2.accumulateWeighted(frame, background, accumulated_weight)


"""
Grabbed the hands segment from the region of interest.
In order to perform background subtraction, we first must Ã¢â‚¬Å“learn; a model of the background.
Once learned, this background model is compared against the current image and then the known background parts ae 
subtracted away.
The object left after subtraction are presumably new foreground objects.
And then we can find the external contours from the image.
And find the extrem points.
frame - current frame
threshold_min - min threshold value
Return extrem points of the hand
"""


def hand_segmentation(frame, threshold_min=25):
    # Removing noise
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, (4, 4))
    # Calculate the absolute difference between the background and the past and frame.
    diff = cv2.absdiff(background.astype("uint8"), frame)
    # Blur the background for better results
    diff = cv2.GaussianBlur(diff, (7, 7), 1.5)
    ret, thresholded = cv2.threshold(diff, threshold_min, 255, cv2.THRESH_BINARY)

    # Grab the external contours from the image.
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # No contours
    if len(contours) == 0:
        return None
    else:
        # Grab the largest contours points
        hand_segment = max(contours, key=cv2.contourArea)

    return (thresholded, hand_segment)