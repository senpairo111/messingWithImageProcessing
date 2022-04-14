import gbvision as gbv
CAMERA_PORT = 1 
EXPOSURE = -7
SINGLE_DUCK_THRSESHOLD = gbv.ColorThreshold([[12, 22], [199, 255], [56, 136]], 'HSV')
MULTIPLE_DUCKS_THRESHOLD = gbv.ColorThreshold([[19, 28], [215, 255], [24, 154]], 'HSV')
MULTIPLE_DUCKS = gbv.GameObject(0.109544511501)
SINGLE_DUCK =  gbv.GameObject(0.039633272976)