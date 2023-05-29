#!/usr/bin/env bash

# Build custom container
docker build . -t mc_rtc

# Run it by passing host display socket and variable
xhost +local:
docker run -ti --rm \
   -e DISPLAY=$DISPLAY \
   -v /tmp/.X11-unix:/tmp/.X11-unix \
   -v ./controller:/controller \
   -v ./mc_rtc.yaml:/root/.config/mc_rtc/mc_rtc.yaml \
   mc_rtc
