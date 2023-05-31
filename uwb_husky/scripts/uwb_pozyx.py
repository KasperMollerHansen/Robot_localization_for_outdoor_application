import rospy
from numpy import float64, int64
from gtec_msgs.msg import Ranging
from pozyx_simulation.msg import uwb_data 
from std_msgs.msg import Float64

def callback(data):
    global sequence
    global save
    global uwb
    if (data.seq != sequence):
        pub.publish(uwb)
        uwb = uwb_data()
        for i in range(num_anchors):
            save[i] = False
        sequence = data.seq
    for i in range(num_anchors):   
        if ((data.anchorId == i) and (save[i] == False)):
            uwb.destination_id.append(int64(data.anchorId))
            uwb.distance.append(float64(data.range))
            uwb.stamp.append(rospy.get_rostime())
            save[i] = True

def listener():
    rospy.init_node('listener', anonymous=True)
    global uwb
    global pub
    uwb = uwb_data()
    sub = rospy.Subscriber('/gtec/toa/ranging', Ranging, callback, queue_size=10)
    pub = rospy.Publisher('/uwb_data_topic', uwb_data, queue_size=1)
    #initialize global variables
    rate = rospy.Rate(30*6)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    num_anchors = 8
    save = []
    for i in range(num_anchors):
        save.append(False)
    sequence = 0
    listener()

