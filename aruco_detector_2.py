import cv2
import numpy as np
from pythonosc import udp_client
import settings


def normalize_x_position(x, width):
    # TODO: Ajustar de -1 a 1
    return x


def normalize_y_position(y, height):
    # TODO: Ajustar de -1 a 1
    return y


# Initialize ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

# Initialize OSC client to send data to Resolume
client = udp_client.SimpleUDPClient("localhost", settings.OSC_PORT)
client.send_message("/test", "Hello from Python!")

# Initialize video capture
cap = cv2.VideoCapture(settings.CAMERA_INDEX_NUM)

# Set camera resolution
desired_width = settings.CAMERA_PIXELS_WIDTH
desired_height = settings.CAMERA_PIXELS_HEIGHT
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

# Get the dimensions of the video frame
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Track currently detected markers
current_markers = set()

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
        gray, aruco_dict, parameters=parameters
    )

    # Draw detected markers
    if ids is not None:
        detected_ids = set(ids.flatten())

        # Print markers entering the scene
        for marker_id in detected_ids - current_markers:
            if marker_id in settings.MARKERS_PAGINAS:
                client.send_message(
                    settings.PAGE_ENTER_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    1,
                )
                print("KEY: ")
                print(
                    settings.PAGE_ENTER_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    )
                )
            if marker_id in settings.MARKERS_OBJETOS:
                client.send_message(
                    settings.OBJECT_ENTER_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    1,
                )
                print("KEY: ")
                print(
                    settings.OBJECT_ENTER_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    )
                )
            print(f"Marker {marker_id} entered the scene")

        # Print markers leaving the scene
        for marker_id in current_markers - detected_ids:
            if marker_id in settings.MARKERS_PAGINAS:
                client.send_message(
                    settings.PAGE_LEAVES_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    1,
                )
            if marker_id in settings.MARKERS_OBJETOS:
                client.send_message(
                    settings.OBJECT_LEAVES_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    1,
                )
            print(f"Marker {marker_id} left the scene")

        # Update current markers
        current_markers = detected_ids

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
                client.send_message(
                    settings.OBJECT_POSITION_X_UPDATE_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    norm_x,
                )
                client.send_message(
                    settings.OBJECT_POSITION_Y_UPDATE_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    norm_y,
                )
                client.send_message(
                    settings.OBJECT_ROTATION_Z_UPDATE_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    yaw_degrees,
                )
                client.send_message(
                    settings.OBJECT_SCALE_UPDATE_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    float(scale),
                )

    else:
        # If no markers detected, print markers leaving the scene
        for marker_id in current_markers:
            if marker_id in settings.MARKERS_PAGINAS:
                client.send_message(
                    settings.PAGE_LEAVES_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    1,
                )
            if marker_id in settings.MARKERS_OBJETOS:
                client.send_message(
                    settings.OBJECT_LEAVES_EVENT.format(
                        OSC_PREFIX=settings.OSC_PREFIX, marker_id=marker_id
                    ),
                    1,
                )
            print(f"Marker {marker_id} left the scene")
        current_markers.clear()

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == settings.TECLA_SALIR:
        break

cap.release()
cv2.destroyAllWindows()
