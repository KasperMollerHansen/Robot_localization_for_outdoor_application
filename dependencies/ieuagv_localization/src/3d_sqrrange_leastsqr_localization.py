#!/usr/bin/env python
'''
__author__ = "Bekir Bostanci"
__license__ = "BSD"
__version__ = "0.0.1"
__maintainer__ = "Bekir Bostanci"
__email__ = "bekirbostanci@gmail.com"
'''

import rospy
from pozyx_simulation.msg import  uwb_data
from geometry_msgs.msg import PoseStamped

import tf
import time
import math

import numpy as np
import matplotlib.pyplot as plt 
import math
from scipy.linalg import eigvals
import re

all_distance = []
all_destination_id = []
pose_x = 0 
pose_y = 0
pose_z = 0
global robot_pos
global sensor_pos
sensor_pos = []

rospy.init_node('localization_data_node', anonymous=True)
pub = rospy.Publisher('localization_data_topic_sqr', PoseStamped, queue_size=10)


def subscribe_data(uwb_data_cell):
    all_destination_id = uwb_data_cell.destination_id
    all_distance = uwb_data_cell.distance
    active_sensor_pos = []
    for i in range(len(all_destination_id)):
        active_sensor_pos.append(sensor_pos[all_destination_id[i]])
    active_sensor_pos = np.squeeze(active_sensor_pos)
    robot_pos = position_calculation(active_sensor_pos,all_distance) 
    publish_data(robot_pos[0],robot_pos[1],robot_pos[2])    


def publish_data(pose_x,pose_y,pose_z):
    robot_pos = PoseStamped()
    robot_pos.header.frame_id = 'uwb_sqr'
    robot_pos.header.stamp = rospy.Time.now()
    robot_pos.pose.position.x = float(pose_x*0.001)
    robot_pos.pose.position.y = float(pose_y*0.001)
    robot_pos.pose.position.z = float(pose_z*0.001)

    robot_pos.pose.orientation.x = 0.0
    robot_pos.pose.orientation.y = 0.0
    robot_pos.pose.orientation.z = 0.0
    robot_pos.pose.orientation.w = 0.0
    pub.publish(robot_pos)

    
#added => cagdas tekok 
def position_calculation(sensor_pos,dist): 
    flag_1 = False
    try:
        vertical=len(sensor_pos[0])
    except TypeError:
        print("ERROR! Not enough anchors available, move back to coverage area")
        flag_1 = True
    if (flag_1 == True):
        return robot_pos
    else:
        horizontal=len(sensor_pos)
        A=(-2*sensor_pos).transpose()
        B=np.ones([horizontal,1],dtype=float).transpose()
        A=np.append(A,B,axis=0)
        A=A.transpose()
        R=np.zeros([1,vertical],dtype=float).transpose() 
        b=np.zeros([1,horizontal],dtype=float)
        for i in range(horizontal):
            b[0][i]=dist[i]**2-(np.linalg.norm(sensor_pos[i]))**2
        D=np.eye(3)
        D=np.append(D,np.zeros([3,1],dtype=float),axis=1)
        D=np.append(D,np.zeros([1,4],dtype=float),axis=0)
        f=np.zeros([4,1],dtype=float)
        np.put(f,3,-0.5)
        AtrA=np.matmul(A.transpose(),A)
        eival=eigvals(D,AtrA)
        eival=np.real(np.sort(eival))
        eival=eival[::-1]
        lam=-(eival**-1)
        ub=10**7
        lb=lam[0]
        tolerance = 10**-4
        count=0
        while ub-lb>tolerance:
            count+=1
            midpo = (ub + lb)/2
            yhat=np.linalg.solve((AtrA+midpo*D),np.subtract(np.matmul(A.transpose(),b.transpose()).transpose(),(midpo*f).transpose()).transpose())
            #fun = yhat'*D*yhat + 2*f'*yhat;
            fun=np.matmul(np.matmul(yhat.transpose(),D),yhat)+np.matmul(2*f.transpose(),yhat)
            if fun>0:
                lb = midpo
            else:
                ub = midpo
        x=yhat[:3]
        if yhat[3]<0:
            x=-x
        return x 
     

def get_anchors_pos():
    max_anchor = 6
    sensor_pos = []   
    uwb_id = 'uwb_anchor'
    listener = tf.TransformListener()
    
    for i in range(max_anchor):
        try:
            time.sleep(0.3)
            (trans,rot) = listener.lookupTransform('/map', uwb_id+str(i), rospy.Time(0))
            sensor_pos.append(trans)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            break
    sensor_pos = np.dot(sensor_pos,1000)


    if sensor_pos == [] :
        rospy.logwarn("There is not found any anchors. Function is working again.")    
        get_anchors_pos()


    return sensor_pos


if __name__ == "__main__":
    #get uwb anchors postion
    sensor_pos = get_anchors_pos()
    robot_pos = [0,0,0]

    rospy.Subscriber('uwb_data_topic', uwb_data, subscribe_data)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
