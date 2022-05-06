import gbvision as gbv
CAMERA_PORT = 1
EXPOSURE = -5

default_vals = [26, 190, 170]
default_range = [5, 35, 40]

MAIN_DUCK_THRESHOLD = gbv.ColorThreshold([[default_vals[0] - default_range[0], 
                                           default_vals[0] + default_range[0]], 
                                          [default_vals[1] - default_range[1],
                                           default_vals[1] + default_range[1]],
                                          [default_vals[2] - default_range[2],
                                           default_vals[2] + default_range[2]]],
                                         'HSV')

SINGLE_DUCK_THRSESHOLD = gbv.ColorThreshold([[10, 20], [207, 255], [78, 198]], 'HSV')
#MULTIPLE_DUCKS_THRESHOLD = gbv.ColorThreshold([[19, 28], [215, 255], [24, 154]], 'HSV')
MULTIPLE_DUCKS_THRESHOLD = gbv.ColorThreshold([[20, 30], [147, 227], [153, 255]], 'HSV')
MULTIPLE_DUCKS = gbv.GameObject(0.109544511501)
SINGLE_DUCK =  gbv.GameObject(0.039633272976)

HUE_KP = 0.0000003
HUE_KI = 0.00000000001
HUE_KD = 0.000004

SAT_KP = 0.011
SAT_KI = 0.0000002 
SAT_KD = 0.007 

VAL_KP = 0.0091
VAL_KI = 0.0000021 
VAL_KD = 0.0878

RANGE_HUE_KP = 0
RANGE_SAT_KP = 0
RANGE_VAL_KP = 0

EXPOSURE_KP = 0.0098
EXPOSURE_KI = 0.000249
EXPOSURE_KD = 0.00096


