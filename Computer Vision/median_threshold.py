import cv2
import numpy as np
import gbvision as gbv
import settings as settings
stdv = np.array([5, 40, 60])


def main():
    camera = gbv.USBCamera(settings.CAMERA_PORT)
    camera.set_exposure(settings.EXPOSURE)
    window = gbv.CameraWindow('feed', camera)
    window.open()
    
    while True:
        frame = window.show_and_get_frame()
        k = window.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('feed', frame)
            
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()
    print(bbox)
    print(thr)

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr)

    original.open()
    after_proc.open()
    while True:
        ok, frame = camera.read()
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break

    original.close()
    after_proc.close()


if __name__ == '__main__':
    main()