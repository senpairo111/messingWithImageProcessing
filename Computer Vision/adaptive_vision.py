import struct
import cv2
import gbvision as gbv
import numpy as np
import settings as settings
import socket

default_vals = settings.default_vals
default_range = settings.default_range

TARGET = settings.MULTIPLE_DUCKS

sock = socket.socket

def main():
    cam = gbv.USBCamera(settings.CAMERA_PORT, gbv.LIFECAM_3000) 
    cam.set_exposure(settings.EXPOSURE)
    
    ok, frame = cam.read()
    win = gbv.FeedWindow("window")
    thr = gbv.FeedWindow("threshold")
    raw = gbv.FeedWindow("raw")
    cur_thr = settings.MAIN_DUCK_THRESHOLD
    hue = default_vals[0] 
    sat = default_vals[1] 
    val = default_vals[2] 
    
    range_hue = default_range[0] 
    range_sat = default_range[1] 
    range_val = default_range[2] 
        
    exposure = settings.EXPOSURE
    last_exposure_e = 0
    exposure_integral = 0
    
    hue_integral = 0
    hue_last_e = 0
    
    sat_integral = 0
    sat_last_e = 0
    
    
    while win.show_frame(frame):
        
        # hue PID
        hue_error = (hue - cur_thr.__getitem__(0)[0])
        hue_integral += hue_error
        hue_derivative = hue_error - hue_last_e
        hue += (hue_error * settings.HUE_KP
                ) + (hue_integral * settings.HUE_KI
                ) + (hue_derivative * settings.HUE_KD)
        hue_last_e = hue_error
        
        # sat PID
        sat_error = -(sat - cur_thr.__getitem__(1)[0])
        sat_integral += sat_error
        sat_derivative = sat_last_e - sat_error
        sat_last_e = sat_error
        sat += (sat_error * settings.SAT_KP
                ) + (sat_integral * settings.SAT_KI
                ) - (sat_derivative * settings.SAT_KD)
        print(sat)
        print(sat_error)
        
        # val PID
        exposure_error = -(val - cur_thr.__getitem__(2)[0])
        exposure_integral += exposure_error
        exposure_derivative = exposure_error - last_exposure_e
        val += (exposure_error * settings.VAL_KP
                ) + (exposure_integral * settings.VAL_KI
                ) - (exposure_derivative * settings.VAL_KD) 
        # exposure -= (exposure_error * settings.EXPOSURE_KP
        #                    ) + (exposure_integral * settings.EXPOSURE_KI
        #                     ) - (exposure_derivative * settings.EXPOSURE_KD)
        #print(exposure)
        #print(exposure_derivative)
        #cam.set_exposure(exposure)
        last_exposure_e = exposure_error
        
        
        
        final_thr = gbv.ColorThreshold([[hue - range_hue, hue + range_hue],
                                        [sat - range_sat, sat + range_sat],
                                        [val - range_val, val + range_val]],
                                       'HSV') or settings.MAIN_DUCK_THRESHOLD
        print(final_thr)
        print(cur_thr)
        
        # threshold
        threshold = final_thr + gbv.MedianBlur(5) + gbv.Dilate(13, 3
            ) + gbv.Erode(9, 3) + gbv.DistanceTransformThreshold(0.3)

        # pipe
        pipe = threshold + gbv.find_contours + gbv.FilterContours(
            100) + gbv.contours_to_rotated_rects_sorted + gbv.filter_inner_rotated_rects
        
        ok, frame = cam.read()
        thr.show_frame(threshold(frame))
        raw.show_frame(final_thr(frame))
        cnts = pipe(frame)
        
        if len(cnts) > 0:
            root = gbv.BaseRotatedRect.shape_root_area(cnts[0])
            center = gbv.BaseRotatedRect.shape_center(cnts[0])
            locals = TARGET.location_by_params(cam, root, center)
            # print("distance:" + str(TARGET.distance_by_params(cam, root)))
            # print("location:" + str(locals))
            # print("angle:" + str(np.arcsin(locals[0] / locals[2]) * 180 / np.pi))
            
            # the part where we adapt 
            bbox = cv2.boundingRect(threshold(frame))
            if (ok):
                cur_thr = gbv.median_threshold(frame, [0, 0, 0], bbox, 'HSV')
            frame = gbv.draw_rotated_rects(frame, cnts, (255, 0, 0), thickness=5)
            # with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            #     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #     sock.sendto(struct.pack('ddd', locals[0], locals[1], locals[2]),
            #         ("255.255.255.255", 5162))
        else:
            cur_thr = settings.MAIN_DUCK_THRESHOLD
            
            
                
                


if __name__ == '__main__':
    main()
