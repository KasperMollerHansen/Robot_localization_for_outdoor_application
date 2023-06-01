import rospy
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_matrix

from numpy import array

offset_vec = array([[0.0425],
                    [0],
                    [0.01],
                    [1]])

def callback_orb(data):
    #Position
    pos_orb = data

    pos_orb.header.frame_id = "camera_body"

    coor_vec_cali = array([[data.pose.pose.position.x],
                      [data.pose.pose.position.y],
                      [data.pose.pose.position.z],
                      [1]])
    
    coor_vec_cali += offset_vec

    ori_vec = array([data.pose.pose.orientation.x,
                      data.pose.pose.orientation.y,
                      data.pose.pose.orientation.z,
                      data.pose.pose.orientation.w])
    M_T = quaternion_matrix(ori_vec)

    coor_new = coor_vec_cali - M_T @ offset_vec

    pos_orb.pose.pose.position.x = coor_new[0]
    pos_orb.pose.pose.position.y = coor_new[1]
    pos_orb.pose.pose.position.z = coor_new[2]

    pub_frame_orb.publish(pos_orb)

def callback_orb_fused(data):
    #Position
    pos_orb_fused = data

    coor_vec_cali = array([[data.pose.pose.position.x],
                      [data.pose.pose.position.y],
                      [data.pose.pose.position.z],
                      [1]])
    
    coor_vec_cali += offset_vec

    ori_vec = array([data.pose.pose.orientation.x,
                      data.pose.pose.orientation.y,
                      data.pose.pose.orientation.z,
                      data.pose.pose.orientation.w])
    M_T = quaternion_matrix(ori_vec)

    coor_new = coor_vec_cali - M_T @ offset_vec

    pos_orb_fused.pose.pose.position.x = coor_new[0]
    pos_orb_fused.pose.pose.position.y = coor_new[1]
    pos_orb_fused.pose.pose.position.z = coor_new[2]

    pub_frame_orb_fused.publish(pos_orb_fused)

def callback_gps_fused(data):
    #Position
    pos_gps_body_fused = data

    coor_vec_cali = array([[data.pose.pose.position.x],
                      [data.pose.pose.position.y],
                      [data.pose.pose.position.z],
                      [1]])
    
    coor_vec_cali += offset_vec

    ori_vec = array([data.pose.pose.orientation.x,
                      data.pose.pose.orientation.y,
                      data.pose.pose.orientation.z,
                      data.pose.pose.orientation.w])
    M_T = quaternion_matrix(ori_vec)

    coor_new = coor_vec_cali - M_T @ offset_vec

    pos_gps_body_fused.pose.pose.position.x = coor_new[0]
    pos_gps_body_fused.pose.pose.position.y = coor_new[1]
    pos_gps_body_fused.pose.pose.position.z = coor_new[2]

    pub_frame_gps_body_fused.publish(pos_gps_body_fused)
    

def callback_zed(data):
    #Position
    pos_zed.header.frame_id = "camera_body"

    coor_vec_cali = array([[data.pose.pose.position.x],
                      [data.pose.pose.position.y],
                      [data.pose.pose.position.z],
                      [1]])
    
    coor_vec_cali += offset_vec


    ori_vec = array([data.pose.pose.orientation.x,
                      data.pose.pose.orientation.y,
                      data.pose.pose.orientation.z,
                      data.pose.pose.orientation.w])
    M_T = quaternion_matrix(ori_vec)

    coor_new = coor_vec_cali - M_T @ offset_vec

    pos_zed.pose.pose.position.x = coor_new[0]
    pos_zed.pose.pose.position.y = coor_new[1]
    pos_zed.pose.pose.position.z = coor_new[2]

    pub_frame_zed.publish(pos_zed)    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    sub_orb = rospy.Subscriber('/orb_slam3/frame_pose_repub', PoseWithCovarianceStamped, callback_orb)
    sub_orb_fused = rospy.Subscriber('/orb_slam3/frame_pose_fused', Odometry, callback_orb_fused)
    sub_gps_fused = rospy.Subscriber('/odometry/gps_fused', Odometry, callback_gps_fused)
    sub_zed = rospy.Subscriber('/zedm/zed_node/pose_with_covariance', PoseWithCovarianceStamped, callback_zed)
    global pub_frame_orb
    global pub_frame_orb_fused
    global pub_frame_gps_body_fused
    global pub_frame_zed
    global pos_orb
    global pos_orb_fused
    global pos_gps_body_fused
    global pos_zed

    pos_orb = PoseWithCovarianceStamped()
    pos_orb_fused = Odometry()
    pos_gps_body_fused = Odometry()
    pos_zed = PoseWithCovarianceStamped()
    
    pub_frame_orb = rospy.Publisher('/orb_slam3/body_pose', PoseWithCovarianceStamped, queue_size=1)
    pub_frame_orb_fused = rospy.Publisher('/orb_slam3/body_pose_fused', Odometry, queue_size=1)
    pub_frame_gps_body_fused = rospy.Publisher('/odometry/gps_body_fused', Odometry, queue_size=1)
    pub_frame_zed = rospy.Publisher('/zedm/zed_node/body_pose', PoseWithCovarianceStamped, queue_size=1)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
