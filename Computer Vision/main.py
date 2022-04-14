import gbvision as gbv
import numpy as np
import settings as settings
threshold = settings.MULTIPLE_DUCKS_THRESHOLD + gbv.MedianBlur(5) + gbv.Dilate(7, 7
        ) + gbv.MedianBlur(9) + gbv.Erode(5, 7) + gbv.DistanceTransformThreshold(0.3)

pipe = threshold + gbv.find_contours + gbv.FilterContours(
    100) + gbv.contours_to_rotated_rects_sorted + gbv.filter_inner_rotated_rects
TARGET = settings.MULTIPLE_DUCKS

def main():
    cam = gbv.USBCamera(settings.CAMERA_PORT, gbv.LIFECAM_3000)
    cam.set_exposure(settings.EXPOSURE)
    
    ok, frame = cam.read()
    win = gbv.FeedWindow("window")
    thr = gbv.FeedWindow("threshold")
    raw = gbv.FeedWindow("raw")
    while win.show_frame(frame):
        ok, frame = cam.read()
        thr.show_frame(threshold(frame))
        raw.show_frame(settings.MULTIPLE_DUCKS_THRESHOLD(frame))
        cnts = pipe(frame)
        frame = gbv.draw_rotated_rects(frame, cnts, (255, 0, 0), thickness=5)
        
        if len(cnts) > 0:
            root = gbv.BaseRotatedRect.shape_root_area(cnts[0])
            center = gbv.BaseRotatedRect.shape_center(cnts[0])
            locals = TARGET.location_by_params(cam, root, center)
            print("distance:" + str(TARGET.distance_by_params(cam, root)))
            print("location:" + str(locals))
            print("angle:" + str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))
            #with open("D:/visionTest/angle.txt", "w") as file:
            #    file.write(str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))


if __name__ == '__main__':
    main()
