# Base provided mc-rtc image
FROM gergondet/mc-rtc

# Add stuff to enable X11 forwarding to host
RUN apt-get update
RUN apt-get install -qqy x11-apps
ENV DISPLAY :0

# Fix for ROS commands not being available in container
RUN echo "source /opt/ros/noetic/setup.bash" > /root/.bashrc
