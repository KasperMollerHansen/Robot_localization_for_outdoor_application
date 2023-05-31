import rospy
from numpy import array
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
from uwb_husky.msg import Error


def callback_uwb(data):
    global uwb
    uwb = array([data.pose.pose.position.x,data.pose.pose.position.y])    

def calback_uwb_odom(data):
    global uwb_odom
    uwb_odom = array([data.pose.pose.position.x,data.pose.pose.position.y])

def callback_gps(data):
    global gps_odom
    gps_odom = array([data.pose.pose.position.x,data.pose.pose.position.y])

def callback_fused(data):
    global uwb_imu_gps
    uwb_imu_gps = array([data.pose.pose.position.x,data.pose.pose.position.y])  

def callback_gt(data):
    global gt_pos
    gt_pos = array([data.pose.pose.position.x, data.pose.pose.position.y])
    
    try:
        error.uwb_x = uwb[0]-gt_pos[0]
        error.uwb_y = uwb[1]-gt_pos[1]
        error.uwb_odom_x = uwb_odom[0]-gt_pos[0]
        error.uwb_odom_y = uwb_odom[1]-gt_pos[1]
        error.gps_odom_x = gps_odom[0]-gt_pos[0]
        error.gps_odom_y = gps_odom[1]-gt_pos[1]
        error.uwb_imu_gps_x = uwb_imu_gps[0]-gt_pos[0]
        error.uwb_imu_gps_y = uwb_imu_gps[1]-gt_pos[1]
        error.gt_x = gt_pos[0]
        error.gt_y = gt_pos[1]
    except NameError:
            pass
    pub.publish(error)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    global error
    error = Error()
    sub_uwb = rospy.Subscriber('/localization_data_topic', PoseWithCovarianceStamped, callback_uwb)
    sub_uwb_odom = rospy.Subscriber('/odometry/uwb/', Odometry, calback_uwb_odom)
    sub_gps = rospy.Subscriber('/odometry/gps', Odometry, callback_gps)
    sub_uwb_imu_gps = rospy.Subscriber('/odometry/fused', Odometry, callback_fused)
    sub_gt = rospy.Subscriber('/husky_ground_truth', Odometry, callback_gt)

    global pub
    pub = rospy.Publisher('/husky_error', Error, queue_size=5)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
