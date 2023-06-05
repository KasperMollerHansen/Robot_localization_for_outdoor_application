### Setup for UWB simulation
place gazebo folder in your home folder - This contaion world and model parameters

### Add model folder to Gazebo
In  ~/.bashrch insert the following line

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/$USER$/models
export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:/home/$USER$/gazebo/worlds

### Simulation
Run the simulation with the command:
roslaunch uwb_husky uwb_launch.launch 
