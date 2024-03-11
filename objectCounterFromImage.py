import cv2
import numpy as np
frame = cv2.imread("numbers.png")
# Convert frame from BGR to HSV
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# Define the range of your color in HSV
lower_yellow = np.array([20, 150, 150])  # Adjust these values according to your needs
upper_yellow = np.array([30, 255, 255])  # Adjust these values according to your needs
# Create a mask for your color
yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
# Find contours in the mask
contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
object_number = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 500:
        object_number += 1
        # Calculate the centroid of the object
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        # Draw the contour and centroid on the frame
        cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 5)
        cv2.circle(frame, (cX, cY), 20, (255, 0, 0), -1)


# Display the resulting frame with yellow object count
cv2.putText(frame, f'Total Number : {object_number}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
cv2.imshow('Number counter project', frame)
cv2.imshow('Yellow Mask',yellow_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
