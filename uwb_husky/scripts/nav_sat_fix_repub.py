import rospy
from sensor_msgs.msg import NavSatFix
from math import sin
from random import uniform
x = 0

def callback_gps(data):
    global x
    x += uniform(-0.5,2)

    cov = 2
    pos = data
    pos.latitude = pos.latitude * (0.0000003*sin(0.005*x)+1)
    pos.longitude = pos.longitude * (0.000003*sin(0.005*x)+1)
    pos.position_covariance = [cov, 0.0, 0.0, 0.0, cov, 0.0, 0.0, 0.0, 3*cov]
    pub.publish(pos)


def listener():
    rospy.init_node('listener', anonymous=True)

    sub_gps = rospy.Subscriber('navsat/fix', NavSatFix, callback_gps)

    global pub
    global pos
    pos = NavSatFix()

    pub = rospy.Publisher('navsat/fix_co', NavSatFix, queue_size=5)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
