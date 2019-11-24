
# Camara Remote Control  
##### Using Image Processing techniques
A remote control that's operated via a camera. The remote control enables channel switching and controlling video speed through hand and fingers movements.
Implemented in Python and OpenCV.

 0 fingers for stop.

 3 finger for backward.

 5 fingers for forward.

 Hand wave to the left for previous channel.
 
 Hand wave to the right for next channel.




# Demo

![Demo](https://user-images.githubusercontent.com/40145410/58424277-c254bf00-809f-11e9-9db9-a81e0a0925e6.gif)





# The main idea

● Store the video frames

● Iteration over the frames

● Count how many fingers are being held up

● Identify when the fingers reach the edge of the frame  

# Store the video frames
Take a video as the input and break it into frames. Simultaneously store those frames in a list.

# Iteration over the frames
After getting a list of frames we perform iteration over the frames, and control the index of the list with the number of fingers that are being held up.

# Count how many fingers are being held up

![video1545480416](https://user-images.githubusercontent.com/40145410/50406760-26164b80-07d3-11e9-8bee-ccc3980f445a.gif) 


![capture](https://user-images.githubusercontent.com/40145410/50406794-dd12c700-07d3-11e9-86da-fada81684e47.PNG)


# Motion Region of Interest
Background Extraction from a video. Background extraction comes important in object tracking. If you already have an image with constant background, then it is simple. But in the real world, the backround we see is noisy, so one has to estimate the background over time. That is where we use Running Average implemented by ​cv2.accumulateWeighted(). We keep feeding each frame to this function, and the function keeps finding the averages of all frames. 0.02 = α We found that it achieves good results for 60 frames. This results in an estimated background model learnt over time.


# Hand Segmentation
For each frame in time - The estimated background is substracted from the current image. The objects left after subtraction are presumably the foreground objects. We had to blur the frames using ​Gaussian blur ​and morphology operations (​opening​) to ​achieve better results. Finally, we can find the external contours from the Hand Segment.

# Count the fingers being held up 
We follow the steps bellow: 


● Find the extrema locations in the hand segment

![1](https://user-images.githubusercontent.com/40145410/50377346-54a1f400-0624-11e9-9669-133a7a101086.PNG)

●  Use the extrema locations to calculate the hand center

![capture](https://user-images.githubusercontent.com/40145410/50377348-7307ef80-0624-11e9-8847-f5b047dfec78.PNG)


● Calculate the distance between the center and the point that is the farthest from the center

![capture](https://user-images.githubusercontent.com/40145410/50377359-93d04500-0624-11e9-9354-8dec40f4dcac.PNG)


● Use that distance to create a circle (any points that are outside of the circle are the extended fingers) 

![capture](https://user-images.githubusercontent.com/40145410/50377366-b06c7d00-0624-11e9-9ae9-a7a359aaffbe.PNG)



● Return the number of the fingers. 


# Identify when the fingers reach the edge of the frame


● Create a mask with two lines along the edges.

![mask_lines](https://user-images.githubusercontent.com/40145410/57573093-e53e6c80-742b-11e9-940f-859fc0c61e24.PNG)

● Then use the "and" bitwise operator


![hand](https://user-images.githubusercontent.com/40145410/57572655-1ae05700-7426-11e9-9c0a-c54738a56c0b.PNG) 

● The result of the previous step will give us a few contours.

![final](https://user-images.githubusercontent.com/40145410/57573163-449c7c80-742c-11e9-8998-db6c711f8f8b.PNG)

● Determine the size that's allowed of the contour (the size should be small)

● Find the location of the contours.

● Switch channel if:
  
   1) The size of the contours are in the right range.
  
   2) The location of the contours are on one side of the frame.
  
   3) There is only one finger that being held up.
