# Michelin + LIRMM thesis technical test

## Setup instructions

Open 3 terminals. In the first one, run `./run.sh`. In the two other ones, run `docker exec -it <ID> bash` by replacing `<ID>` with the container ID running from the first terminal (can be seen with `docker ps`).

Then:

```bash
# Terminal 1
roscore
# Terminal 2
PYTHONPATH=/controller:$PYTHONPATH roslaunch mc_rtc_ticker control_display.launch
# Terminal 3
PYTHONPATH=/controller:$PYTHONPATH rosrun mc_rtc_ticker mc_rtc_ticker
```

## Documentation

Self-made documentation by reverse-engineering the library since vscode cannot infer the bindings.

It was useful to me so I'll leave it here.

### `self.*`

```python
['addAnchorFrameCallback', 'addCollisions', 'addContact', 'config', 'contactConstraint', 'contacts', 'create', 'dynamicsConstraint', 'env', 'gui', 'hasContact', 'hasObserverPipeline', 'hasRobot', 'kinematicsConstraint', 'logger', 'observerPipeline', 'observerPipelines', 'postureTask', 'qpsolver', 'removeAnchorFrameCallback', 'removeCollisions', 'removeContact', 'reset', 'reset_callback', 'robot', 'robots', 'run', 'run_callback', 'selfCollisionConstraint', 'supported_robots', 'switch_target', 'timeStep']
```

### `self.robot()`

> Some properties of the C++ documentation are missing here, such as `frames()`, not making it possible to implement some stuff. Maybe there are other ways I don't know of yet?

```python
['alpha', 'alphaD', 'bodyAccB', 'bodyBodySensor', 'bodyForceSensor', 'bodyHasBodySensor', 'bodyHasForceSensor', 'bodyIndexByName', 'bodyPosW', 'bodySensor', 'bodySensors', 'bodyTransform', 'bodyVelB', 'bodyVelW', 'collisionTransform', 'com', 'comAcceleration', 'comVelocity', 'convex', 'convexes', 'cop', 'copW', 'copySurface', 'flexibility', 'forceSensor', 'forwardAcceleration', 'forwardKinematics', 'forwardVelocity', 'hasBody', 'hasBodySensor', 'hasForceSensor', 'hasJoint', 'hasSurface', 'jointIndexByName', 'jointTorque', 'loadRSDFFromDir', 'mb', 'mbc', 'mbg', 'module', 'name', 'posW', 'q', 'ql', 'qu', 'stance', 'surface', 'surfacePose', 'surfaceWrench', 'surfaces', 'tl', 'tu', 'vl', 'vu', 'zmp']
```

### Available joints

> Even though `l_wrist` and `r_wrist` are not available in this list, they are valid properties to `mc_tasks.EndEffectorTask()` so I think that "joints" and "frames" must be different in some way, but frames are not mentionned in the source code of the JVRC-1 robot.
> 
> I was looking for a `neck` frame that controls both 3 axes (`neck_y`, `neck_r` and `neck_p`) but could not, so I approximated the head movement using only `neck_p` instead of using manually all 3 axes and doing manual projections on their respective axes.

```python
- b'R_HIP_P'
- b'R_HIP_R'
- b'R_HIP_Y'
- b'R_KNEE'
- b'R_ANKLE_R'
- b'R_ANKLE_P'
- b'L_HIP_P'
- b'L_HIP_R'
- b'L_HIP_Y'
- b'L_KNEE'
- b'L_ANKLE_R'
- b'L_ANKLE_P'
- b'WAIST_Y'
- b'WAIST_P'
- b'WAIST_R'
- b'NECK_Y'
- b'NECK_R'
- b'NECK_P'
- b'R_SHOULDER_P'
- b'R_SHOULDER_R'
- b'R_SHOULDER_Y'
- b'R_ELBOW_P'
- b'R_ELBOW_Y'
- b'R_WRIST_R'
- b'R_WRIST_Y'
- b'R_UTHUMB'
- b'R_LTHUMB'
- b'R_UINDEX'
- b'R_LINDEX'
- b'R_ULITTLE'
- b'R_LLITTLE'
- b'L_SHOULDER_P'
- b'L_SHOULDER_R'
- b'L_SHOULDER_Y'
- b'L_ELBOW_P'
- b'L_ELBOW_Y'
- b'L_WRIST_R'
- b'L_WRIST_Y'
- b'L_UTHUMB'
- b'L_LTHUMB'
- b'L_UINDEX'
- b'L_LINDEX'
- b'L_ULITTLE'
- b'L_LLITTLE'
```
