#################################################
#################################################
#           ANTES DE LA CALIBRACIÓN             #
#################################################
#################################################
CAMERA_INDEX_NUM = 0
CAMERA_PIXELS_WIDTH = 1280
CAMERA_PIXELS_HEIGHT = 720

TECLA_SALIR = ord("q")
CARPETA_IMAGENES_CALIBRACION = "/home/gero/Documents/franui/callibration"

CALLIBRATION_MARKER_CORNERS_X = 9
CALLIBRATION_MARKER_CORNERS_Y = 6
CALLIBRATION_MARKER_SQUARE_SIZE = 0.02 # 20 cm


#################################################
#################################################
#    CON EL RESULTADO DE LA CALIBRACIÓN         #
#################################################
#################################################
CAMERA_MATRIX_FROM_CALIBRATION = [
    [1.20185186e03, 0.00000000e00, 9.26639602e02],
    [0.00000000e00, 1.19509508e03, 5.92507593e02],
    [0.00000000e00, 0.00000000e00, 1.00000000e00],
]  # El primer resultado de la calibración (Camera matrix:)
DISTORTION_COEFFS_FROM_CALIBRATION = [
    [0.43099149, -1.12989648, 0.00513272, -0.02113329, 0.97396071]
]  # El segundo resultado de la calibración ("Distortion coefficients:)



#################################################
#################################################
#              POST CALIBRACIÓN                 #
#################################################
#################################################
MIN_X = -0.5  # IZQUIERDA DE LA PANTALLA
MAX_X = 0.5  # DERECHA DE LA PANTALLA
MAX_Y = 0.5  # ARRIBA DE LA PANTALLA
MIN_Y = -0.5  # ABAJO DE LA PANTALLA

OSC_IP_RESOLUME = "192.168.1.38"
OSC_PORT_RESOLUME = 7000
OSC_IP_UNITY = "192.168.1.38"
OSC_PORT_UNITY = 8000
OSC_PREFIX = "/franui"

# Setear acá y agregar a la lista
PAGINA_1_MARKER_ID = 1
PAGINA_2_MARKER_ID = 2
MARKERS_PAGINAS = [PAGINA_1_MARKER_ID, PAGINA_2_MARKER_ID]

# Setear acá y agregar a la lista
OBJETO_1_MARKER_ID = 3
OBJETO_2_MARKER_ID = 4
MARKERS_OBJETOS = [OBJETO_1_MARKER_ID, OBJETO_2_MARKER_ID]

# All markers
MARKERS_TO_TRACK = MARKERS_PAGINAS + MARKERS_OBJETOS

MARKER_SIZE = 0.05 # 5 cm

# Eventos OSC
OBJECT_ENTER_EVENT = "{OSC_PREFIX}/object/{marker_id}/scene/enters"
OBJECT_LEAVES_EVENT = "{OSC_PREFIX}/object/{marker_id}/scene/leaves"
PAGE_ENTER_EVENT = "{OSC_PREFIX}/page/{marker_id}/scene/enters"
PAGE_LEAVES_EVENT = "{OSC_PREFIX}/page/{marker_id}/scene/leaves"
OBJECT_POSITION_X_UPDATE_EVENT = "{OSC_PREFIX}/object/{marker_id}/position/x"
OBJECT_POSITION_Y_UPDATE_EVENT = "{OSC_PREFIX}/object/{marker_id}/position/y"
OBJECT_ROTATION_Z_UPDATE_EVENT = "{OSC_PREFIX}/object/{marker_id}/rotation/z"
OBJECT_SCALE_UPDATE_EVENT = "{OSC_PREFIX}/object/{marker_id}/scale"