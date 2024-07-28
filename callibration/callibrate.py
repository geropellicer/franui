import cv2
import numpy as np
import glob
import settings

# Define the chessboard size (number of inner corners)
chessboard_size = (settings.CALLIBRATION_MARKER_CORNERS_X, settings.CALLIBRATION_MARKER_CORNERS_Y)

# Real world dimensions of the chessboard squares (in meters)
square_size = settings.CALLIBRATION_MARKER_SQUARE_SIZE

# Termination criteria for cornerSubPix
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), ..., (8,5,0)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays to store object points and image points from all images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Load all images
images = glob.glob(f'{settings.CARPETA_IMAGENES_CALIBRACION}/calibration_images/*.jpg')  # Change the path to your images
count = 0

for fname in images:
    count += 1
    print(f"Processing image {count}/{len(images)}")
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        
        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Perform camera calibration
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix:")
print(camera_matrix)

print("Distortion coefficients:")
print(dist_coeffs)
