import rospy
from numpy import array
from nav_msgs.msg import Odometry 
from pozyx_simulation.msg import  uwb_data

def calback_uwb_odom(data):
    global uwb_odom_pos
    uwb_odom_pos = data

def callback_gps_odom(data):
    global gps_odom_pos
    gps_odom_pos = data

def callback_uwb_gps(data):
    numid = len(data.destination_id)
    if numid < 4:
        try:
            uwb_odom_pos.pose.pose.position = gps_odom_pos.pose.pose.position
            uwb_odom_pos.pose.covariance = gps_odom_pos.pose.covariance
        except NameError:
             pass
    pub.publish(uwb_odom_pos)    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    global uwb_odom_pos
    uwb_odom_pos = Odometry()

    global gps_odom_pos
    gps_odom_pos = Odometry()

    rospy.Subscriber('/odometry/uwb/', Odometry, calback_uwb_odom)
    rospy.Subscriber('/odometry/gps', Odometry, callback_gps_odom)
    rospy.Subscriber('uwb_data_topic', uwb_data, callback_uwb_gps)

    global pub
    pub = rospy.Publisher('/odometry/fused', Odometry, queue_size=5)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
