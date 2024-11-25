previous_steering = 0

def reward_function(params):
    '''
    Reward function for AWS DeepRacer with penalties for steering changes and high-speed reckless driving.
    '''
 

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    speed = params['speed']
    steering_angle = params['steering_angle']
    steps = params['steps']
    progress = params['progress']
   

    # Reward logic for staying close to center
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if not params['all_wheels_on_track']:
        return 0.0000000001

    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1

    # Reward for being on the left side of the track
    if is_left_of_center:
        reward += 1.5

    # Reward for speed in straight parts
    if abs(steering_angle) < 7:
        if speed > 2:
                reward += 2
        elif speed > 2.5:
                reward += 4
       

    # Reward for progress milestones
    TOTAL_STEPS = 160
    if (steps % 30) == 0 and progress >= (steps / TOTAL_STEPS) * 100:
        reward += 3.0
    elif (steps % 30) == 0 and progress < (steps / TOTAL_STEPS) * 100:
        reward += 0.5

    if abs(steering_angle) - abs(previous_steering ) > 25:
        reward *= 0.3
    if abs(steering_angle) - abs(previous_steering ) > 20:
            reward *= 0.5
    if abs(steering_angle) - abs(previous_steering ) > 12:
        reward *= 0.8



    # Penalize high-speed reckless driving
    if speed > 2.5 and abs(steering_angle) > 25:
        reward *= 0.5
    if speed > 2.0 and abs(steering_angle) > 20:
        reward *= 0.7  # Reduce reward significantly for high speed and high steering angle


    # Add big reward for completing the track
    if progress == 100:
        reward += 150  # Big reward for completing the track

    # Return reward as a float
    return float(reward)



