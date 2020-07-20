# # # # 
# # # # Term Project for Me478 Class, by Görkem Seçkin
# # # # Course Instructor: İlker Tarı

import math
import random
import sys
import numpy as numpy


def solar_angle_calc_degree(elevation_d, azimuth_d):
    elevation_d = float(elevation_d)
    azimuth_d = float(azimuth_d)

    azimuth_r = math.radians(azimuth_d)
    elevation_r = math.radians(elevation_d)

    numerator_abs_val = math.sin(azimuth_r)
    if math.sin(azimuth_r) < 0:
        numerator_abs_val = - numerator_abs_val


    theta_t = math.atan( numerator_abs_val / math.tan(elevation_r) )

    theta_i = math.asin( math.cos(azimuth_r) * math.cos(elevation_r) )


    theta_t_d = math.degrees(theta_t)
    theta_i_d = math.degrees(theta_i)

    result_list = [theta_t_d , theta_i_d]


    return result_list






def solar_angle_calc_radian(elevation_r, azimuth_r):
    elevation_r = float(elevation_r)
    azimuth_r = float(azimuth_r)


    numerator_abs_val = math.sin(azimuth_r)
    if math.sin(azimuth_r) < 0:
        numerator_abs_val = - numerator_abs_val


    theta_t = math.atan( numerator_abs_val / math.tan(elevation_r) )

    theta_i = math.asin( math.cos(azimuth_r) * math.cos(elevation_r) )


    theta_t_d = math.degrees(theta_t)
    theta_i_d = math.degrees(theta_i)

    result_list = [theta_t_d , theta_i_d]


    return result_list




input_file = open("C:\Me478_Project\input_solar_angle1.txt", "r")
input_data_list = input_file.read().split()




incidence_angle_list = []
counter1 = 0

while counter1 < len(input_data_list):
    incidence_angle_list.append(solar_angle_calc_degree(input_data_list[counter1],input_data_list[counter1+1]))
    counter1 += 2

print(input_data_list)
print(len(input_data_list))
print(incidence_angle_list)
print(len(incidence_angle_list))