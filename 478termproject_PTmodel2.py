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

print("input_data_list \n{}".format(input_data_list))
print(len(input_data_list))
print("incidence_angle_list \n{}".format(incidence_angle_list))
print(len(incidence_angle_list))



# # # # # # # # # # # # # # # # Model for Parabolic Trough 
# # # # # # # # # # # # # # # # Parameters for calculations

# # # Units of l_focal and l_coll are m
l_focal = 1.71
l_coll = 150
eta_opt_pt = 0.75

# # # factor_cl_x is the multiplication of Cl (average cleanliness) and xfield (field availability)
factor_cl_x = 0.96

# # # DNI (irradiation) has the unit of  kW*h / (m2*a)
DNI = 2791

# # # ASF, aperture area of the solar field
# # # ASF = length of collector * aperture width of collector
# # # For Parabolic Trough Collectors, mirror surface is about 10% larger than aperture area.[page6,Morin]
# # # mirror_width, mirror width per collector, unit is m
mirror_width = 5.77
mirror_area = l_coll * mirror_width 
# # # mirror_area = l_coll * mirror_width * number_of_collectors
ASF = mirror_area * (10/11)

# # # b1, b2 values are from Riffelmann,2005
# # # unit of b1: W/(m2*K)
# # # unit of b2: W/(m2*K2)
b1 = 0
b2 = 0.00047

# # # unit of q_pipeloss_pt: W/m2
q_pipeloss_pt = 10

# # # unit of Tf_in, Tf_out and T_amb: degree celcius
Tf_in = 280
Tf_out = 411
# # # I may use different T_amb values for different months. For now, it is constant
T_amb = 20



list_K_pt = []
list_eta_endloss = []
list_eta_shadow = []
list_delta_T = []
list_Qinc = []
list_Qloss = []
list_Qfield = []



def pt_K_calc_degree(theta_i_d):
    theta_i_r = math.radians(theta_i_d)
    K_pt = math.cos(theta_i_r) - 0.000525 * theta_i_d - 0.0000286 * theta_i_d**2

    list_K_pt.append(K_pt)
    return K_pt


def pt_eta_endloss_calc_degree(theta_i_d):
    theta_i_r = math.radians(theta_i_d)

    eta_endloss = 1 - ( (l_focal * math.tan(theta_i_r)) / (l_coll) )

    list_eta_endloss.append(eta_endloss)
    return eta_endloss


def pt_eta_shadow_calc_degree(theta_t_d):
    RW = 3
    theta_t_r = math.radians(theta_t_d)
    value1 = RW * math.cos(theta_t_r)

    if 0 <= value1 and value1 < 1:
        list_eta_shadow.append(value1)
        return value1
    elif value1 >= 1:
        list_eta_shadow.append(1)
        return 1
    elif value1 < 0:
        list_eta_shadow.append(0)
        return 0


def pt_temp_diff_calc():

    delta_T = ( (Tf_in + Tf_out) / 2 ) - T_amb

    list_delta_T.append(delta_T)
    return delta_T



# # # calculate Qinc, total power absorbed from the solar field
def pt_Qinc_calc(theta_t_d, theta_i_d):

    eta_shadow = pt_eta_shadow_calc_degree(theta_t_d)
    eta_endloss = pt_eta_endloss_calc_degree(theta_i_d)
    K_pt = pt_K_calc_degree(theta_i_d)

    Qinc = eta_opt_pt * eta_shadow * eta_endloss * K_pt * factor_cl_x * DNI * ASF

    list_Qinc.append(Qinc)
    return Qinc


# # # calculate Qloss, thermal loss of the solar field
def pt_Qloss_calc():

    delta_T = pt_temp_diff_calc()

    Qloss = ( (b1 * delta_T + b2 * delta_T**2) + q_pipeloss_pt) * ASF

    list_Qloss.append(Qloss)
    return Qloss


# # # calculate Qfield, useful thermal output of the solar field
def pt_Qfield_calc(theta_t_d, theta_i_d):

    Qinc = pt_Qinc_calc(theta_t_d, theta_i_d)
    Qloss = pt_Qloss_calc()

    Qfield = Qinc - Qloss

    list_Qfield.append(Qfield)
    return Qfield 



Qfield_list = []
counter2 = 0

for a in incidence_angle_list:
    if a[0] > 0:
        Qfield_list.append(pt_Qfield_calc(a[0],a[1]))


Qfield_for_day = 0
for a in Qfield_list:
    Qfield_for_day += a


print("list_K_pt \n{}".format(list_K_pt))
print("list_eta_endloss \n{}".format(list_eta_endloss))
print("list_eta_shadow \n{}".format(list_eta_shadow))
print("list_delta_T \n{}".format(list_delta_T))
print("list_Qinc \n{}".format(list_Qinc))
print("list_Qloss \n{}".format(list_Qloss))
print("list_Qfield \n{}".format(list_Qfield))


print("Qfield_list \n{}".format(Qfield_list))

print(len(list_K_pt), len(list_eta_endloss), len(list_eta_shadow), len(list_delta_T), len(list_Qinc), len(list_Qloss), len(list_Qfield), len(Qfield_list))

print("Qfield_for_day \n{}".format(Qfield_for_day))

print("Qfield_for_month \n{}".format(Qfield_for_day*30))


# # # print("Qfield_for_year \n{}".format(Qfield_for_day*365))

