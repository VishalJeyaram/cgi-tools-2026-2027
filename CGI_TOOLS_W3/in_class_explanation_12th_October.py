import pymel.core as pm

ball_geo = pm.polySphere(name='ball_geo')[0]
ball_geo.ty.set(1)
pm.makeIdentity(ball_geo, apply=True, t=True, r=True, s=True )

# Height variables 
fr_ground = 0.2 # 20% ground friction to reduce height points by 20% everytime the ball hits the ground
rest_y = 0.0001 # Rest position
pos = 12.0 # Starting position of the ball when it is dropped from a height
pos_list = [pos] # List of heights points after each bounce

# Time variables
time_interval = 11 # Original time interval between each max and min point. Not between each full bounce. It is in frames. 
fr_air = 0.1 # Reduction in number frames for each time interval due to friction. Time interval decreases by 10% each time. 
curr_time = 1
time_list = [1] # List of time points after each bounce
curr_time += time_interval # Updating current_time to be to the next 

# While loop to create height points and update pos_list
while pos >= rest_y:
    pos_list.append(0.0)
    pos *= (1 - fr_ground) # Updating maximum height point that ball will bounce to after accounting for friction
    if pos >= rest_y:
        pos_list.append(pos) # Updating pos_list with the latest height if it is above the ground rest point
pos_list.append(0.0)
        
ro = range(1, len(pos_list))
for i in ro:
    if i % 2 != 0:
        continue
    # min position and rising 
    curr_time = round(curr_time)
    time_list.append(curr_time)
    time_interval *= (1 - fr_air)
    curr_time += time_interval
    # Max position and ball is falling
    curr_time = round(curr_time)
    time_list.append(curr_time)
    curr_time += time_interval


print(time_list)
print(pos_list)
print(len(time_list))
print(len(pos_list))

for i in range(0, len(time_list)):
    pm.currentTime(time_list[i])
    ball_geo.ty.set(pos_list[i])  # position the ball
    pm.setKeyframe(ball_geo.ty)  # set key

    
            
    
    
    
