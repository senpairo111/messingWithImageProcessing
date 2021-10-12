import gbvision as gbv

threshold = gbv.ColorThreshold([[17, 27], [95, 175], [99, 179]], 'HSV') + gbv.MedianBlur(5) + gbv.Dilate(5,
                                                                                                         2) + gbv.Erode(
    5, 2) + gbv.DistanceTransformThreshold(0.3)

pipe = threshold + gbv.find_contours + gbv.FilterContours(
    100) + gbv.contours_to_rotated_rects_sorted + gbv.filter_inner_rotated_rects

JOY_CON = gbv.GameObject(0.05916079783099616)


def main():
    cam = gbv.USBCamera(0, gbv.LIFECAM_3000)
    cam.set_exposure(-7)
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
            print(JOY_CON.distance_by_params(cam, root))
            print(JOY_CON.location_by_params(cam, root, center))


if __name__ == '__main__':
    main()
