import struct
import cv2
import gbvision as gbv
import numpy as np
import settings as settings
import socket

default_vals = [23, 231, 120]
default_range = [5, 30, 30]

TARGET = settings.MULTIPLE_DUCKS

sock = socket.socket

def main():
    cam = gbv.USBCamera(settings.CAMERA_PORT, gbv.LIFECAM_3000) 
    cam.set_exposure(settings.EXPOSURE)
    exposure = settings.EXPOSURE
    last_exposure_e = 0
    exposure_integral = 0
    ok, frame = cam.read()
    win = gbv.FeedWindow("window")
    thr = gbv.FeedWindow("threshold")
    raw = gbv.FeedWindow("raw")
    cur_thr = settings.SINGLE_DUCK_THRSESHOLD
    hue = default_vals[0] 
    sat = default_vals[1] 
    val = default_vals[2] 
    
    range_hue = default_range[0] 
    range_sat = default_range[1] 
    range_val = default_range[2] 
        
    hue_integral = 0
    while win.show_frame(frame):
        slight_denoise = gbv.MedianBlur(7)
        frame = slight_denoise(frame)
        
        hue_error = (hue - cur_thr.__getitem__(0)[0])
        hue_integral += hue_error
        hue += (hue_error * settings.HUE_KP + hue_integral * settings.HUE_KI)
        

        #print(cur_thr.__getitem__(2)[0])
        
        # exposure PID
        exposure_error = -(val - cur_thr.__getitem__(2)[0])
        exposure_integral += exposure_error
        exposure_derivative = exposure_error - last_exposure_e
        exposure -= (exposure_error * settings.EXPOSURE_KP
                           ) + (exposure_integral * settings.EXPOSURE_KI
                            ) - (exposure_derivative * settings.EXPOSURE_KD)
        print(exposure)
        print(exposure_error)
        #print(exposure_derivative)
        cam.set_exposure(exposure)
        last_exposure_e = exposure_error
        
        final_thr = gbv.ColorThreshold([[hue - range_hue, hue + range_hue],
                                        [sat - range_sat, sat + range_sat],
                                        [val - range_val, val + range_val]],
                                       'HSV')
        
        # threshold
        threshold =  final_thr + gbv.Dilate(13, 3
            )  + gbv.Erode(5, 2) + gbv.DistanceTransformThreshold(0.3)

        # pipe
        pipe = threshold + gbv.find_contours + gbv.FilterContours(
            100) + gbv.contours_to_rotated_rects_sorted + gbv.filter_inner_rotated_rects
        
        ok, frame = cam.read()
        thr.show_frame(threshold(frame))
        raw.show_frame(final_thr(frame))
        cnts = pipe(frame)
        frame = gbv.draw_rotated_rects(frame, cnts, (255, 0, 0), thickness=5)
        if len(cnts) > 0:
            root = gbv.BaseRotatedRect.shape_root_area(cnts[0])
            center = gbv.BaseRotatedRect.shape_center(cnts[0])
            locals = TARGET.location_by_params(cam, root, center)
            # print("distance:" + str(TARGET.distance_by_params(cam, root)))
            # print("location:" + str(locals))
            # print("angle:" + str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))
            
                
            bbox = cv2.boundingRect(threshold(frame))
            #print(bbox)
            
        else:
            bbox = None
        # where we adapt
        try:
            cur_thr = gbv.median_threshold(frame, [0, 0, 0], bbox, 'HSV')
        finally:
            pass
            
            
            # with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            #     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #     sock.sendto(struct.pack('ddd', locals[0], locals[1], locals[2]),
            #         ("255.255.255.255", 5162))
                
                


if __name__ == '__main__':
    main()
