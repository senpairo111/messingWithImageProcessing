from email.mime import base
import struct
import cv2
import gbvision as gbv
import numpy as np
import settings as settings
import socket

default_vals = [25, 187, 180]
default_range = [5, 60, 60]

TARGET = settings.MULTIPLE_DUCKS
final_thr = settings.MULTIPLE_DUCKS_THRESHOLD
sock = socket.socket

def main():
    cam = gbv.USBCamera(settings.CAMERA_PORT, gbv.LIFECAM_3000) 
    cam.set_exposure(settings.EXPOSURE)
    
    ok, frame = cam.read()
    win = gbv.FeedWindow("window")
    thr = gbv.FeedWindow("threshold")
    raw = gbv.FeedWindow("raw")
    while win.show_frame(frame):
        # where we adapt
        cur_thr = gbv.median_threshold(frame, [0, 0, 0], None, 'HSV')
        hue = default_vals[0] - ((default_vals[0] - cur_thr.__getitem__(0)[0]) * settings.HUE_KP)
        sat = default_vals[1] - ((default_vals[1] - cur_thr.__getitem__(1)[0]) * settings.SAT_KP)
        val = default_vals[2] + ((default_vals[2] - cur_thr.__getitem__(2)[0]) * settings.VAL_KP)
        
        range_hue = default_range[0] + (hue - cur_thr.__getitem__(0)[0]) * settings.RANGE_HUE_KP
        range_sat = default_range[1] - (sat - cur_thr.__getitem__(1)[0]) * settings.RANGE_SAT_KP
        range_val = default_range[2] + (val - cur_thr.__getitem__(2)[0]) * settings.RANGE_VAL_KP
        
        cam.set_exposure(settings.EXPOSURE)
        
        final_thr.__setitem__(0, [hue - range_hue, hue + range_hue])
        final_thr.__setitem__(1, [sat - range_sat, sat + range_sat])
        final_thr.__setitem__(2, [val - range_val, val + range_val])
        
        threshold =  final_thr + gbv.MedianBlur(3) + gbv.Dilate(12, 9
            )  + gbv.Erode(5, 9) + gbv.DistanceTransformThreshold(0.3)

        
        pipe = threshold + gbv.find_contours + gbv.FilterContours(
            100) + gbv.contours_to_rotated_rects_sorted + gbv.filter_inner_rotated_rects
        ok, frame = cam.read()
        #thr.show_frame(threshold(frame))
        thr.show_frame(settings.MULTIPLE_DUCKS_THRESHOLD(frame))
        raw.show_frame(final_thr(frame))
        cnts = pipe(frame)
        frame = gbv.draw_rotated_rects(frame, cnts, (255, 0, 0), thickness=5)
        if len(cnts) > 0:
            root = gbv.BaseRotatedRect.shape_root_area(cnts[0])
            center = gbv.BaseRotatedRect.shape_center(cnts[0])
            locals = TARGET.location_by_params(cam, root, center)
            print("distance:" + str(TARGET.distance_by_params(cam, root)))
            print("location:" + str(locals))
            print("angle:" + str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))
            
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(struct.pack('ddd', locals[0], locals[1], locals[2]),
                    ("255.255.255.255", 5162))
                
                


if __name__ == '__main__':
    main()
