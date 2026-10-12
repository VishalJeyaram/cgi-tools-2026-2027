import sys
import math
import pymel.core as pm  # import pyMel

# import scripts from current workspace
sys.path.append(pm.workspace(expandName='scripts'))


# create the ball geometry
ball_geo = pm.polySphere(name='ball_geo')[0]


time = 1  # staring time
time_interval = 8  # from starting height to the ground
ball_height = 12  # starting height of the ball
ground_height = 1  # ground height
friction = 0.2  # 20% friction with the ground


def rise_fall_keys():
    '''set the keys for a rising and falling ball'''
    # set key as ball falls from height
    global time
    global time_interval
    global ball_height
    pm.currentTime(math.floor(time))  # move to correct frame
    ball_geo.ty.set(ball_height)  # position the ball
    pm.setKeyframe(ball_geo.ty)  # set the key
    time += time_interval  # update the time interval

    # set keys as ball hits ground
    pm.currentTime(math.floor(time)) # Move to the new frame
    ball_geo.ty.set(ground_height) # POsition ball to ground height
    pm.setKeyframe(ball_geo.ty) # Set ground keyframe
    ball_height -= ball_height * friction # Changing new max height to 80% of original height
    if ball_height < 1.0: # If ball height is less than 1 unit, we just set ball height to 1 unit itself
        ball_height = 1.0
    time_interval -= time_interval * friction # Time interval is also decreased now to become 80% of original to account for friction
    if time_interval < 0: # If time interval decreases beyond a certain point, then it just becomes zero and the ball ceases to bounce
        time_interval = 0
    time += time_interval  # update the time interval for when we call the function nex
    # TIme interval has been updated to 80% of original
    # Ball height has been updated to 80% of original
    # Current time to set next keyframe has been updated as well   

for i in range(0, 21):
    # print(f'{ball_height}, {i}')
    rise_fall_keys()