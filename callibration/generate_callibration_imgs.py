import cv2

cap = cv2.VideoCapture(0)
# Set camera resolution
desired_width = 1920
desired_height = 1280
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
        
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow('frame', frame)
    
    # Press 's' to save the frame
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'/home/gero/Documents/franui/callibration/calibration_images/image_{count}.jpg', frame)
        print(f'Image {count} saved. To folder calibration_images')
        count += 1
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
