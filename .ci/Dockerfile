FROM osrf/ros:humble-desktop

# Install basic Python ML tools and git
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Kyutai dependencies
# RUN pip3 install --no-cache-dir torch numpy soundfile huggingface_hub
# RUN pip3 install --no-cache-dir torch "numpy<2.0.0" scipy soundfile huggingface_hub pocket-tts
RUN pip3 install --upgrade --no-cache-dir torch "numpy>=2.0.0" "scipy>=1.14.0" soundfile huggingface_hub pocket-tts
WORKDIR /ros2_ws
# Cyclonedds & Networking
RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*
COPY . src/ros2_kyutai_tts

# Clone audio_common from source to get audio_common_msgs
RUN git clone -b ros2 https://github.com/ros-drivers/audio_common.git src/audio_common

# Build the workspace
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build --packages-up-to ros2_kyutai_tts"

COPY .ci/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["ros2", "run", "ros2_kyutai_tts", "kyutai_tts_node"]