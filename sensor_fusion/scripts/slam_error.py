import rospy
from numpy import array
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseStamped,PoseWithCovarianceStamped
from sensor_fusion.msg import Slam_error


def callback_slam(data):
    global slam_pos
    slam_pos = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])
    
def callback_zed(data):
    global zed_pos
    zed_pos = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])

def callback_slam_imu_fus(data):
    global slam_imu_fus_pos
    slam_imu_fus_pos = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])

def callback_gps(data):
    global gps_pos
    gps_pos = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])

def callback_gps_fused(data):
    global gps_pos_fused
    gps_pos_fused = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])
    vicon_pos = array([0,0,0])

    try:
        Slam_error.slam_pos_x = slam_pos[0]-vicon_pos[0]
        Slam_error.slam_pos_y = slam_pos[1]-vicon_pos[1]
        Slam_error.slam_pos_z = slam_pos[2]-vicon_pos[2]
        Slam_error.zed_pos_x = zed_pos[0]-vicon_pos[0]
        Slam_error.zed_pos_y = zed_pos[1]-vicon_pos[1]
        Slam_error.zed_pos_z = zed_pos[2]-vicon_pos[2]
        Slam_error.slam_imu_pos_x = slam_imu_fus_pos[0]-vicon_pos[0]
        Slam_error.slam_imu_pos_y = slam_imu_fus_pos[1]-vicon_pos[1]
        Slam_error.slam_imu_pos_z = slam_imu_fus_pos[2]-vicon_pos[2]
        Slam_error.gps_pos_x = gps_pos[0]-vicon_pos[0]
        Slam_error.gps_pos_y = gps_pos[1]-vicon_pos[1]
        Slam_error.gps_pos_z = gps_pos[2]-vicon_pos[2]
        Slam_error.gps_fused_pos_x = gps_pos_fused[0]-vicon_pos[0]
        Slam_error.gps_fused_pos_y = gps_pos_fused[1]-vicon_pos[1]
        Slam_error.gps_fused_pos_z = gps_pos_fused[2]-vicon_pos[2]
        Slam_error.vicon_pos_x = vicon_pos[0]
        Slam_error.vicon_pos_y = vicon_pos[1]
        Slam_error.vicon_pos_z = vicon_pos[2]
    except NameError:
        pass

    pub_slam.publish(slam_error)

def callback_vicon(data):
    global vicon_pos
    vicon_pos = array([data.pose.position.x, data.pose.position.y, data.pose.position.z])
    
    
def listener():
    rospy.init_node('listener', anonymous=True)

    global slam_error
    slam_error = Slam_error()

    sub_orb_slam = rospy.Subscriber('/orb_slam3/body_pose', PoseWithCovarianceStamped, callback_slam)

    sub_zed = rospy.Subscriber('/zedm/zed_node/body_pose', PoseWithCovarianceStamped, callback_zed)

    sub_sensor_fus = rospy.Subscriber('/orb_slam3/body_pose_fused', Odometry, callback_slam_imu_fus)
    
    sub_gps = rospy.Subscriber('/odometry/gps', Odometry, callback_gps)

    #sub_gps_fused = rospy.Subscriber('/odometry/gps_fused', Odometry, callback_gps_fused)
    sub_gps_fused = rospy.Subscriber('/odometry/gps_body_fused', Odometry, callback_gps_fused)
    
    #sub_vicon = rospy.Subscriber('/vicon/jon_kap_bsc/pose', PoseStamped, callback_vicon)

    global pub_slam
    pub_slam = rospy.Publisher('/slam_error', Slam_error, queue_size=5)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
