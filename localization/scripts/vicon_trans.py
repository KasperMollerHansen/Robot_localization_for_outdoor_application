import rospy
from geometry_msgs.msg import PoseStamped, TransformStamped

def callback(data):
    #loading position and orientation of Husky
    pos.header = data.header
    pos.pose.position.x = data.transform.translation.x
    pos.pose.position.y = data.transform.translation.y
    pos.pose.position.z = data.transform.translation.z
    pos.pose.orientation.x = data.transform.rotation.x
    pos.pose.orientation.y = data.transform.rotation.y
    pos.pose.orientation.z = data.transform.rotation.z
    pos.pose.orientation.w = data.transform.rotation.w    
    #publish position
    pub_frame.publish(pos)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    sub = rospy.Subscriber('/vicon/jon_kap_bsc/jon_kap_bsc', TransformStamped, callback)
    global pub_frame
    global pos
    pos = PoseStamped()
    pub_frame = rospy.Publisher('/vicon/jon_kap_bsc/pose', PoseStamped, queue_size=1)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
