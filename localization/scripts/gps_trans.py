import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_multiply, quaternion_inverse

from numpy import array
global k
k = 0

def callback(data):
    #loading position and orientation of Husky
    pos = data
    global k
    global x_0
    global y_0 
    global z_0
    global q_r
    if k == 0:
        x_0 = data.pose.position.x
        y_0 = data.pose.position.y
        z_0 = data.pose.position.z
        q_x_0 = data.pose.orientation.x
        q_y_0 = data.pose.orientation.y
        q_z_0 = data.pose.orientation.z
        q_w_0 = data.pose.orientation.w
        q_r = quaternion_inverse([q_x_0,q_y_0,q_z_0,q_w_0])
        k = 1
    
    q_x = data.pose.orientation.x
    q_y = data.pose.orientation.y
    q_z = data.pose.orientation.z
    q_w = data.pose.orientation.w
    q_new = quaternion_multiply(array([q_x,q_y,q_z,q_w]),array([q_r[0],q_r[1],q_r[2],q_r[3]]))
    pos.pose.orientation.x = q_new[0]
    pos.pose.orientation.y = q_new[1]
    pos.pose.orientation.z = q_new[2]
    pos.pose.orientation.w = q_new[3]

    pos.pose.position.x = data.pose.position.x - x_0
    pos.pose.position.y = data.pose.position.y - y_0
    pos.pose.position.z = data.pose.position.z - z_0
    
    #publish position
    pub_frame.publish(pos)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    sub = rospy.Subscriber('/mavros_node/local_position/pose', PoseStamped, callback)
    global pub_frame
    global pos
    pos = PoseStamped()
    pub_frame = rospy.Publisher('/mavros_node/local_position/map_pose', PoseStamped, queue_size=20)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
