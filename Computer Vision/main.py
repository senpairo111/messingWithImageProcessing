import gbvision as gbv
import numpy as np

threshold = gbv.ColorThreshold([[12, 22], [199, 255], [56, 136]], 'HSV') + gbv.MedianBlur(9) + gbv.Dilate(5,
                                                                                                         15) + gbv.Erode(
    5, 2) + gbv.DistanceTransformThreshold(0.3)

pipe = threshold + gbv.find_contours + gbv.FilterContours(
    100) + gbv.contours_to_rotated_rects_sorted + gbv.filter_inner_rotated_rects
TARGET = gbv.GameObject(0.039633272976)

def main():
    cam = gbv.USBCamera(1, gbv.LIFECAM_3000)
    cam.set_exposure(12)
    
    ok, frame = cam.read()
    win = gbv.FeedWindow("window")
    thr = gbv.FeedWindow("threshold")
    while win.show_frame(frame):
        ok, frame = cam.read()
        thr.show_frame(threshold(frame))
        cnts = pipe(frame)
        frame = gbv.draw_rotated_rects(frame, cnts, (255, 0, 0), thickness=5)
        if len(cnts) > 0:
            root = gbv.BaseRotatedRect.shape_root_area(cnts[0])
            center = gbv.BaseRotatedRect.shape_center(cnts[0])
            locals = TARGET.location_by_params(cam, root, center)
            #print("distance:" + str(TARGET.distance_by_params(cam, root)))
            #print("location:" + str(locals))
            print("angle:" + str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))
            with open("D:/visionTest/angle.txt", "w") as file:
                file.write(str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))


if __name__ == '__main__':
    main()
