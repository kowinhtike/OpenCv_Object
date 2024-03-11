import cv2
import numpy as np
import time
import winsound

# Initialize video capture
cap = cv2.VideoCapture(0)
object_number = 0
control = True
# Initialize the time of the last processed frame
last_frame_time = time.time()
total_time = 3

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Convert frame from BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define the range of your color in HSV
    lower_yellow = np.array([95, 150, 150])  # Adjust these values according to your needs
    upper_yellow = np.array([115, 255, 255])  # Adjust these values according to your needs
    # Create a mask for your color
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    # Find contours in the mask
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 2000:
            if (control):
                object_number += 1
                winsound.Beep(frequency=700,duration=100)
                control = False
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(frame, f'Object Size {area}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
        elif area > 500:
            cv2.putText(frame, f'Object Size must be greater than 5000', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # time
    current_time = time.time()
    result_time = current_time - last_frame_time
    # setting for bar
    start_x = 10
    start_y = 50
    bar_height = 100
    range_width = 100

    if result_time <= (total_time - (total_time/2)):
        result_time = int(result_time)
        cv2.rectangle(frame, (start_x, start_y), (start_x + (range_width * total_time), bar_height), (255, 0, 0), 5)
        cv2.rectangle(frame, (start_x, start_y), (start_x + (result_time * range_width), bar_height), (255, 0, 0), -1)
    elif result_time <= (total_time - (total_time/3)):
        result_time = int(result_time)
        cv2.rectangle(frame, (start_x, start_y), (start_x + (range_width * total_time), bar_height), (0, 255, 255), 5)
        cv2.rectangle(frame, (start_x, start_y), (start_x + (result_time * range_width), bar_height), (0, 255, 255), -1)
    else:
        result_time = int(result_time)
        cv2.rectangle(frame, (start_x, start_y), (10 + (range_width * total_time), bar_height), (0, 0, 255), 5)
        cv2.rectangle(frame, (start_x, start_y), (10 + (result_time * range_width), bar_height), (0, 0, 255), -1)

    # Check a few seconds have passed since the last processed frame
    if current_time - last_frame_time >= total_time:
        # Update the time of the last processed frame
        last_frame_time = current_time
        control = True

    # Display the resulting frame with yellow object count
    cv2.putText(frame, f'Total Number : {object_number}', (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
    cv2.imshow('Number counter project', frame)
    # Press Q on keyboard to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
