import cv2
import numpy as np
from pythonosc import udp_client
import settings
from custom_arucos_2 import get_custom_arucos_dict, save_custom_arucos_images
import time

# Initialize OSC client to send data to Resolume
resolume_client = udp_client.SimpleUDPClient(settings.OSC_IP_RESOLUME, settings.OSC_PORT_RESOLUME)
resolume_client.send_message("/test", "Hello from Python to Resolume!")

unity_client = udp_client.SimpleUDPClient(settings.OSC_IP_UNITY, settings.OSC_PORT_UNITY)
unity_client.send_message("/test", "Hello from Python to Unity!")


def normalize_x_position(x, width):
    # TODO: Ajustar de -1 a 1
    return x


def normalize_y_position(y, height):
    # TODO: Ajustar de -1 a 1
    return y


def send_page_change(marker_id):
    resolume_client.send_message(
        settings.PAGE_ENTER_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        1,
    )
    unity_client.send_message(
        settings.PAGE_ENTER_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        1,
    )

    MARKER_ID_TO_COLUMN_ID = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7"
    }

    column_id = MARKER_ID_TO_COLUMN_ID[marker_id]

    resolume_client.send_message(f"/composition/columns/{column_id}/connect", 1)



def send_object_enters(marker_id):
    unity_client.send_message(
        settings.OBJECT_ENTER_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        1,
    )


def send_object_leaves(marker_id):
    unity_client.send_message(
        settings.OBJECT_LEAVES_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        1,
    )

    

# Initialize dictionaries to store previous values for smoothing
previous_positions = {}
previous_rotations = {}

# Smoothing factor (0 < alpha < 1)
alpha = 0.5

def smooth_value(previous, current, alpha):
    return alpha * current + (1 - alpha) * previous

def send_update_object(norm_x, norm_y, yaw_degrees, scale, marker_id):
    # Smooth the position and rotation values
    if marker_id in previous_positions:
        norm_x = smooth_value(previous_positions[marker_id][0], norm_x, alpha)
        norm_y = smooth_value(previous_positions[marker_id][1], norm_y, alpha)
    if marker_id in previous_rotations:
        yaw_degrees = smooth_value(previous_rotations[marker_id], yaw_degrees, alpha)

    # Update previous values
    previous_positions[marker_id] = (norm_x, norm_y)
    previous_rotations[marker_id] = yaw_degrees

    unity_client.send_message(
        settings.OBJECT_POSITION_X_UPDATE_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        norm_x,
    )
    unity_client.send_message(
        settings.OBJECT_POSITION_Y_UPDATE_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        norm_y,
    )
    unity_client.send_message(
        settings.OBJECT_ROTATION_Z_UPDATE_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        yaw_degrees,
    )
    unity_client.send_message(
        settings.OBJECT_SCALE_UPDATE_EVENT.format(
            OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
        ),
        float(scale),
    )
    print(f"Sent update for marker {marker_id}. Position: ({norm_x}, {norm_y}), Rotation: {yaw_degrees}, Scale: {scale}")


# CUSTOM ARUCOS SETUP
arucos_dict = get_custom_arucos_dict()
save_custom_arucos_images(arucos_dict)

parameters = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(arucos_dict, parameters)

# open video capture from (first) webcam
cap = cv2.VideoCapture(settings.CAMERA_INDEX_NUM)

# Set camera resolution
desired_width = settings.CAMERA_PIXELS_WIDTH
desired_height = settings.CAMERA_PIXELS_HEIGHT
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Get the dimensions of the video frame
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Track currently detected markers with timestamps
current_markers = {}
leave_delay = 2  # seconds

# Define camera matrix and distortion coefficients for pose estimation
# These values should be obtained from camera calibration
CAMERA_MATRIX_FROM_CALIBRATION = settings.CAMERA_MATRIX_FROM_CALIBRATION
DISTORTION_COEFFS_FROM_CALIBRATION = settings.DISTORTION_COEFFS_FROM_CALIBRATION
fx, fy, cx, cy, k1, k2, p1, p2, k3 = (
    CAMERA_MATRIX_FROM_CALIBRATION[0][0],
    CAMERA_MATRIX_FROM_CALIBRATION[1][1],
    CAMERA_MATRIX_FROM_CALIBRATION[0][2],
    CAMERA_MATRIX_FROM_CALIBRATION[1][2],
    DISTORTION_COEFFS_FROM_CALIBRATION[0][0],
    DISTORTION_COEFFS_FROM_CALIBRATION[0][1],
    DISTORTION_COEFFS_FROM_CALIBRATION[0][2],
    DISTORTION_COEFFS_FROM_CALIBRATION[0][3],
    DISTORTION_COEFFS_FROM_CALIBRATION[0][4],
)
camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = cv2.aruco.detectMarkers(
        gray, arucos_dict, parameters=parameters
    )

    # Draw detected markers
    if ids is not None:
        detected_ids = set(ids.flatten())

        # Print markers entering the scene
        for marker_id in detected_ids - current_markers.keys():
            if marker_id in settings.MARKERS_PAGINAS:
                send_page_change(marker_id)

            if marker_id in settings.MARKERS_OBJETOS:
                send_object_enters(marker_id)

            print(f"Marker {marker_id} entered the scene")
            current_markers[marker_id] = time.time()

        # Update current markers
        for marker_id in detected_ids:
            current_markers[marker_id] = time.time()

        # Print markers leaving the scene
        for marker_id in list(current_markers.keys()):
            if marker_id not in detected_ids:
                if time.time() - current_markers[marker_id] > leave_delay:
                    if marker_id in settings.MARKERS_OBJETOS:
                        send_object_leaves(marker_id)
                    print(f"Marker {marker_id} left the scene")
                    del current_markers[marker_id]

        for i, corner in enumerate(corners):
            marker_id = int(ids[i][0])  # Ensure marker_id is an integer

            # Draw marker outline
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Estimate pose
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                corner, settings.MARKER_SIZE, camera_matrix, dist_coeffs
            )

            # Calculate scale (this is a placeholder, actual scale calculation might differ)
            scale = 1 - np.linalg.norm(tvec)

            # Convert rvec to rotation matrix
            rotation_matrix, _ = cv2.Rodrigues(rvec)

            # Extract Z-axis rotation (yaw) from the rotation matrix
            yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])

            # Convert yaw from radians to degrees
            yaw_degrees = np.degrees(yaw)

            # Normalize the position to range [-1, 1]
            norm_x = normalize_x_position(tvec[0][0][0], frame_width)
            norm_y = normalize_y_position(tvec[0][0][1], frame_height)

            # Send normalized position, rotation, and scale to Resolume including the marker ID
            if marker_id in settings.MARKERS_OBJETOS:
                send_update_object(norm_x, norm_y, yaw_degrees, scale, marker_id)

    else:
        # If no markers detected, print markers leaving the scene
        for marker_id in list(current_markers.keys()):
            if time.time() - current_markers[marker_id] > leave_delay:
                if marker_id in settings.MARKERS_OBJETOS:
                    send_object_leaves(marker_id)
                print(f"Marker {marker_id} left the scene")
                del current_markers[marker_id]

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == settings.TECLA_SALIR:
        break

cap.release()
cv2.destroyAllWindows()
