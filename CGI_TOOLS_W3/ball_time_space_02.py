
''' Bouncing ball key frames script ''' 
import sys
import pymel.core as pm

# import pymel.core.nodetypes as nt
# import pymel.core.datatypes as dt

# from importlib import reload

# import scripts from current workspace
if pm.workspace(expandName='scripts') not in sys.path:
    sys.path.append(pm.workspace(expandName='scripts'))


def test(obj_name='ball_geo'):
    '''test ball code

       obj_name: string, name of the ball geometry
    '''
    # read ball geometry object as PyNode instance
    ball_geo = pm.PyNode(obj_name)

    # spacing --
    f_val = 0.2  # friction with ground - scale of bounce
    pos_y = 12  # ball y-coord
    rest_y = 0.01  # can't be zero
    pos_list = [12, 0]  # store the ball's max height and ground positions
    while pos_y > rest_y:
        pos_y *= (1 - f_val)  # apply friction
        if pos_y >= rest_y:
            pos_list.append(pos_y)
            pos_list.append(0)

    for i, p in enumerate(pos_list):
        print(f'position number {i+1:#>2} position coordinate {p:#>7.3f}')

    # timing --
    cur_time = 1  # frame
    intr_time = 10  # number of frames it takes the ball to fall.
    fg_val = 0.1  # % reduction in frames it takes to fall - ball timing

    time_list = [1]  # we start at frame 1
    cur_time += intr_time  # ball falls and hits the ground

    for i, p in enumerate(pos_list):
        # ball on the ground and at its minuum Y-coord position and now rising
        cur_time = round(cur_time)  # keys at integer values
        time_list.append(cur_time)  # set/store key at rest ground position
        intr_time *= (1-(fg_val))  # decrease time interval
        cur_time += intr_time  # update current time
        # ball at maximum Y-coord position and now falling
        cur_time = round(cur_time)  # keys at integer values
        time_list.append(cur_time)  # set/store key at maximum highest position
        # up and down movent for each bounce is the same
        # intr_time *= (1-(fg_val)) we don't the decrease time interval again!
        cur_time += intr_time  # update current time

    for i, pt in enumerate(zip(pos_list, time_list)):
        text = f'List number {i+1:#>2} position coordinate '
        text += f'{pt[0]:#>7.3f} at time {pt[1]:#>3}.'
        print(text)

    # seting keys --
    pm.select(ball_geo, r=True)
    for i, pt in enumerate(zip(pos_list, time_list)):
        text = f'List number {i+1:#>2} position coordinate '
        text += f'{pt[0]:#>7.3f} at time {pt[1]:#>3}.'
        print(text)
        pm.currentTime(pt[1])
        ball_geo.ty.set(pt[0])
        pm.setKeyframe()

    # adjust key tangents --
    pm.keyTangent(ball_geo, lock=False)  # unlock key tangents
    for i, pt in enumerate(zip(pos_list, time_list)):
        text = f'List number {i+1:#>2} position coordinate '
        text += f'{pt[0]:#>7.3f} at time {pt[1]:#>3}.'
        print(text)
        if i % 2 != 0:
            pm.selectKey(ball_geo, clear=True) # clear selection of keys
            # specify tangent angle as a function of time
            if pt[1] < 59:
                angle = 69
            elif pt[1] >= 59 and pt[1] < 100:
                angle = 63
            elif pt[1] >= 100 and pt[1] <133:
                angle = 45
            elif pt[1] >= 133 and pt[1] <153:
                angle = 35            
            else:
                angle = 15

            # select the out tangent (ot) for this anim curve at the
            # specified time
            pm.selectKey(ball_geo, attribute='translateY',
                         ot=True, r=True, t=(pt[1],))
            pm.keyTangent(ball_geo, e=True, attribute='translateY',
                          t=(pt[1],), outAngle=angle, outWeight=1)
            # select the in tangent (it) for this anim curve at the
            # specified time
            pm.selectKey(ball_geo, attribute='translateY',
                         it=True, r=True, t=(pt[1],))
            pm.keyTangent(ball_geo, e=True, attribute='translateY',
                          t=(pt[1],), inAngle=-angle, inWeight=1)

    pm.keyTangent(ball_geo, lock=True)
    pm.selectKey(ball_geo, clear=True)

if __name__ == '__main__':
    test()
