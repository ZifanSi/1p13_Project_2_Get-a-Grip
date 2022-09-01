import random
import time
import sys
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)

## returns the pick-up location for a shape   
def get_pickup(shape):
        pick_up = [0.534, 0.0, 0.044]
        return pick_up


## returns the drop-off location for a shape
def get_dropoff(shape):
    if shape ==1:   # 01 small red
        drop_off = [-0.619, 0.244, 0.378]
        
    elif shape ==2: # 02 small green
        drop_off = [0.0, -0.661, 0.395]
        
    elif shape ==3: # 03 small blue
        drop_off = [-0.001, 0.668, 0.407]

    elif shape ==4: # 04 large Red
        drop_off = [-0.395, 0.144, 0.326]

    elif shape ==5: # 05 large green
        drop_off = [0.0, -0.426, 0.313]

    elif shape ==6: # 06 large blue
        drop_off = [0.0, 0.429, 0.325]
        
    return drop_off



## Move end-effector to pick up location
def move_end_effector_pickup(shape):
    while True:
        if arm.emg_left() > 0.5 and arm.emg_right() > 0.5:
            x,y,z = get_pickup(shape)
            arm.move_arm(x,y,z)
            break
      

        
## Move end-effector to drop off location      
def move_end_effector_dropoff(shape):            
    while True:
        if 0 < arm.emg_left() < 0.5 and 0 < arm.emg_right() < 0.5:
            x,y,z = get_dropoff(shape)
            arm.move_arm(x,y,z)
            break


## gripper close
def control_gripper_close():
    while True:
        if arm.emg_left() > 0.5 and arm.emg_right() == 0:
            arm.control_gripper(30)
            break
        
        
## gripper open       
def control_gripper_open():
    while True:
        if 0 < arm.emg_left() < 0.5 and arm.emg_right() == 0:
            arm.control_gripper(-30)
            break


## open Autoclave
def open_auto(shape):
    while True:
        if shape == 4:  # big red
            if arm.emg_left() == 0 and  arm.emg_right() > 0.5:  
                arm.open_red_autoclave(True)
                break
                
        elif shape == 5:  # big green
            if arm.emg_left() == 0 and  arm.emg_right() > 0.5:
                arm.open_green_autoclave(True)
                break
                
        elif shape == 6:  # big blue
            if arm.emg_left() == 0 and  arm.emg_right() > 0.5:
                arm.open_blue_autoclave(True)
                break
        else:
            break    # If shape is small(1 or 2 or 3), this loop will be terminatesd
                
               

## close Autoclave   
def close_auto(shape):
    while True:
        if shape == 4: # big red
            if arm.emg_left() == 0 and  0 <arm.emg_right() < 0.5:
                arm.open_red_autoclave(False)
                break

        elif shape == 5:  # big green
            if arm.emg_left() == 0 and  0 <arm.emg_right() < 0.5:
                arm.open_green_autoclave(False)
                break

        elif shape == 6:  # big blue
            if arm.emg_left() == 0 and  0 <arm.emg_right() < 0.5:
               arm.open_blue_autoclave(False)
               break
        else:
            break  # If shape is small(1 or 2 or 3), this loop will be terminatesd

    

## General Workflow
arm.home()
shapelist =random.sample(range(1,7), 6)
ctr=0
while ctr != 6: 
    for shape in shapelist:
        arm.spawn_cage(shape)
        print("The ID of the container is",shape)
        move_end_effector_pickup(shape)
        control_gripper_close()
        move_end_effector_dropoff(shape)
        open_auto(shape)  # if shape is 1,2,3, open_auto will be terminated. Control of the program flows to control_gripper_open() immediately. 
        control_gripper_open()
        close_auto(shape) # if shape is 1,2,3, close_auto will be terminated. Control of the program flows to arm.move_arm immediately. 
        time.sleep(1)
        arm.move_arm(0.4, 0, 0.48) # return to home position
        time.sleep(1)
        ctr+=1   
arm.home()  







    




