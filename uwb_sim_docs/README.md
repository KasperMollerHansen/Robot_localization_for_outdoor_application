### Setup for UWB simulation
- place models folder in your home folder - This contains the model parameters
- place UWB.world in folder usr/share/gazebo-11/worlds
- 

### Add model folder to Gazebo
In  ~/.bashrc insert the following line

export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/$USER$/models

### Simulation
Run the simulation with the command:
roslaunch uwb_husky uwb_launch.launch 
