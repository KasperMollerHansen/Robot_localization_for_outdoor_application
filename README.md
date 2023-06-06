# Robot_localization_for_outdoor_application
Bachelor's Thesis Respository

- Place everything in your catkin_ws, except the uwb_sim_docs folder
- Instructions for the uwb_sim_docs are found in the README.md file inside the folder

- Install ORB-SLAM3 with all dependencies from source. Follow installation guide here, and make sure to install OpenCV version 4.4.0: https://olayasturias.github.io/ros/slam/survey/2022/03/01/slam-surveying-install.html 
- Instructions for localization are located in the README.md file inside the folder

- For the ZED Mini make sure to set the image quality to 720p and the compression ratio to 1, to have the best possible image. The video publish rate should be set to 60 as well. If there are troubles publishing at this rate, lower the publishing rate of other topics such as the pointcloud to 10 or lower to increase performance.
