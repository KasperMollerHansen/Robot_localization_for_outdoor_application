import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry 

from numpy import array
from numpy.linalg import norm

def callback_gps(data):
    global gps_pose
    gps_pose = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])

def callback(data):
    global gps_pose
    global k
    global map_lost
    global previous_pose
    global reconnect
    global cov_pos
    global cov_ori
    current_pose = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])
    diff = norm(current_pose-previous_pose)
    test = norm(round(data.pose.pose.orientation.w - 1,5))
    if (k > 100) & (test == 0):
        map_lost = True
    if (map_lost == True) & (diff > 3):
        map_lost = False
        reconnect += 1
        gps_error = norm(gps_pose - current_pose)
        if gps_error < 10:
            reconnect = 0
        print(reconnect)
    if map_lost == True:
        cov_pos = 1000
        cov_ori = 10
    elif reconnect < 5:
        cov_pos = 0.1
        cov_ori = 0.05
    pos = data
    pos.header.frame_id = "camera_offset"
    pos.pose.covariance = [cov_pos, 0.0, 0.0, 0.0, 0.0, 0.0, 
                            0.0, cov_pos, 0.0, 0.0, 0.0, 0.0, 
                            0.0, 0.0, cov_pos, 0.0, 0.0, 0.0, 
                            0.0, 0.0, 0.0, cov_ori, 0.0, 0.0, 
                            0.0, 0.0, 0.0, 0.0, cov_ori, 0.0, 
                            0.0, 0.0, 0.0, 0.0, 0.0, cov_ori]
    
    pub_frame.publish(pos)
    k += 1
    previous_pose = array([data.pose.pose.position.x,data.pose.pose.position.y,data.pose.pose.position.z])
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    sub = rospy.Subscriber('/orb_slam3/frame_pose', PoseWithCovarianceStamped, callback)
    sub_gps = rospy.Subscriber('/odometry/gps', Odometry, callback_gps)
    global pub_frame
    global pos
    pos = PoseWithCovarianceStamped()
    pub_frame = rospy.Publisher('/orb_slam3/frame_pose_repub', PoseWithCovarianceStamped, queue_size=1)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    k = 0
    reconnect = 0
    previous_pose = array([0,0,0])
    map_lost = False
    listener()
