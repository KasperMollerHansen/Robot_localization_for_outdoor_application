import rospy
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from tf.transformations import quaternion_multiply
from numpy import array

def callback(data):
    new_frame.header = data.header
    new_frame.header.frame_id = "map"
    new_frame.pose.pose = data.pose

    q_x = data.pose.orientation.x
    q_y = data.pose.orientation.y
    q_z = data.pose.orientation.z
    q_w = data.pose.orientation.w
    
    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z
    
    new_frame.pose.pose.orientation.x = q_z
    new_frame.pose.pose.orientation.y = -q_x
    new_frame.pose.pose.orientation.z = -q_y
    new_frame.pose.pose.orientation.w = q_w
    
    new_frame.pose.pose.position.x = z
    new_frame.pose.pose.position.y = -x
    new_frame.pose.pose.position.z = -y
    
    new_frame.pose.covariance = array([0.05, 0,    0,    0,    0,    0,
                                 	0,    0.05, 0,    0,    0,    0,    
                                 	0,    0,    0.05, 0,    0,    0,
                                 	0,    0,    0,    0.05, 0,    0,
                                 	0,    0,    0,    0,    0.05, 0,
                                 	0,    0,    0,    0,    0,    0.05])
    pub_pose.publish(new_frame)
    
    
def listener():
    rospy.init_node('orb_slam_repub', anonymous=True)
    sub_pose = rospy.Subscriber('/orb_slam3/camera_pose', PoseStamped, callback)
    global pub_pose
    global new_frame
    new_frame = PoseWithCovarianceStamped()
    pub_pose = rospy.Publisher('/orb_slam3/frame_pose', PoseWithCovarianceStamped, queue_size=3)
    rate = rospy.Rate(60)
    rate.sleep()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
