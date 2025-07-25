#!/usr/bin/bash
function clean_up {
    echo "Clean up"
    kill $APP_PID
}
trap clean_up EXIT

DISPLAY=:0 LD_PRELOAD=$PWD/../build/intercept.so glmark2 -b terrain:duration=60 -s 1920x1080 &
APP_PID=$!
echo glmark2 is started with pid [$APP_PID].

# Delay several seconds for warm-up
sleep 2

sudo ./fps-monitor.py $APP_PID
