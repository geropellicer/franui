import numpy as np
import cv2
import cv2.aruco as aruco

# we will not use a built-in dictionary, but we could
# aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

def get_custom_arucos_dict():
    # define an empty custom dictionary with 
    aruco_dict = aruco.Dictionary(0, 9, 1)
    # add empty bytesList array to fill with 3 markers later
    aruco_dict.bytesList = np.empty(shape = (4,11,4), dtype = np.uint8)

    # add new marker(s)
    mybits_0 = np.array([
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1],
    [1,1,0,1,1,1,0,1,1],
    [1,1,0,1,1,1,0,1,1],
    [1,1,1,0,1,0,1,1,1],
    [1,1,1,0,1,0,1,1,1],
    [1,1,0,1,1,1,0,1,1],
    [1,1,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1],
    ], dtype = np.uint8)


    aruco_dict.bytesList[0] = aruco.Dictionary.getByteListFromBits(mybits_0) 

    mybits_1 = np.array([
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,0,1,1],
    [1,1,0,1,1,1,1,0,1],
    [1,1,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,1],
    [1,0,1,1,0,1,1,1,1],
    [1,0,1,1,1,0,1,1,1],
    [1,0,1,1,1,1,0,0,1],
    [1,1,1,1,1,1,1,1,1],
    ], dtype = np.uint8)
    aruco_dict.bytesList[1] = aruco.Dictionary.getByteListFromBits(mybits_1)

    mybits_2 = np.array([
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1],
    [1,1,0,1,1,1,0,1,1],
    [1,1,0,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,1,1],
    [1,1,1,0,0,0,1,1,1],
    [1,1,1,0,1,0,1,1,1],
    [1,1,1,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    ], dtype = np.uint8)
    aruco_dict.bytesList[2] = aruco.Dictionary.getByteListFromBits(mybits_2)

    mybits_3 = np.array([
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,0,0,1,1],
    [1,1,1,1,0,1,1,0,1],
    [1,1,1,1,1,0,1,0,1],
    [1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    ], dtype = np.uint8)
    aruco_dict.bytesList[3] = aruco.Dictionary.getByteListFromBits(mybits_3)

    return aruco_dict

def save_custom_arucos_images(aruco_dict):
    # save marker images
    for i in range(len(aruco_dict.bytesList)):
        cv2.imwrite("./markers_img/custom_aruco_" + str(i) + ".png", aruco.generateImageMarker(aruco_dict, i, 128))
