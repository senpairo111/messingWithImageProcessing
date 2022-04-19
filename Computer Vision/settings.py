import gbvision as gbv
CAMERA_PORT = 1
EXPOSURE = -7
SINGLE_DUCK_THRSESHOLD = gbv.ColorThreshold([[25, 34], [217, 255], [5, 119]], 'HSV')
#MULTIPLE_DUCKS_THRESHOLD = gbv.ColorThreshold([[19, 28], [215, 255], [24, 154]], 'HSV')
MULTIPLE_DUCKS_THRESHOLD = gbv.ColorThreshold([[26, 36], [203, 255], [36, 156]], 'HSV')
MULTIPLE_DUCKS = gbv.GameObject(0.109544511501)
SINGLE_DUCK =  gbv.GameObject(0.039633272976)