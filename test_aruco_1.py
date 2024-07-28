import cv2
import numpy as np
from pythonosc import udp_client

# Initialize ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

# Initialize OSC client to send data to Resolume
client = udp_client.SimpleUDPClient("localhost", 7000)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Get the dimensions of the video frame
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Track currently detected markers
current_markers = set()

# Define camera matrix and distortion coefficients for pose estimation
# These values should be obtained from camera calibration
camera_matrix = np.array([[640, 0, 320], [0, 480, 240], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5,), dtype=np.float32)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect markers
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    # Draw detected markers
    if ids is not None:
        for i, corner in enumerate(corners):
            marker_id = ids[i][0]
            
            # Draw marker outline
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Estimate pose
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, 0.05, camera_matrix, dist_coeffs)
            
            # Calculate scale (this is a placeholder, actual scale calculation might differ)
            scale = 1 - np.linalg.norm(tvec)
            
            # Convert rvec to rotation matrix
            rotation_matrix, _ = cv2.Rodrigues(rvec)
            
            # Extract Z-axis rotation (yaw) from the rotation matrix
            yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
            
            # Convert yaw from radians to degrees
            yaw_degrees = np.degrees(yaw)
            
            # Print raw and translated Z-axis rotation
            print(f"Marker {marker_id} raw Z rotation (radians): {yaw}")
            print(f"Marker {marker_id} Z rotation (degrees): {yaw_degrees}")

            # Send position, rotation, and scale to Resolume including the marker ID
            client.send_message(f"/object/{marker_id}/position", [float(tvec[0][0][0]), float(tvec[0][0][1]), float(tvec[0][0][2])])
            client.send_message(f"/object/{marker_id}/rotation", yaw_degrees)
            client.send_message(f"/object/{marker_id}/scale", [float(scale)])

        detected_ids = set(ids.flatten())
        
        # Print markers entering the scene
        for marker_id in detected_ids - current_markers:
            print(f"Marker {marker_id} entered the scene")
        
        # Print markers leaving the scene
        for marker_id in current_markers - detected_ids:
            print(f"Marker {marker_id} left the scene")
        
        # Update current markers
        current_markers = detected_ids
    else:
        # If no markers detected, print markers leaving the scene
        for marker_id in current_markers:
            print(f"Marker {marker_id} left the scene")
        current_markers.clear()
    
    # Display the resulting frame
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
