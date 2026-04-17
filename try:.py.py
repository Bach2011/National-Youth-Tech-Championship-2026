try:
    print("Starting challenge 2: Follow the line, then turn based on camera text input")
    #After picking up, move forward with line tracing until sees a T intersection, then stop.
    print("Following line until T intersection...")
    while True:
        line_type, _, _ = line_follow(mult=0.25, speed=15)
        if line_type in [0,2]:
            print("See the intersection, stopping.")
            got.mecanum_stop()
            break
    # see, intersection, move forward a bit to fully cross the intersection, then stop.
    got.mecanum_translate_speed_times(angle=0, speed=20, times=17, unit=1)
    

    # Read left or right and turn accordingly until see the line again, then stop.
    print("Looking for LEFT or RIGHT command...")
    while True:
        # Read any text currently visible in the camera frame.
        text = got.get_words_result()

        print("Text:", text)

        # React to specific command words
            # Turn counter-clockwise by ~45 degrees
        if text in ["LEFT", "RIGHT"]:
            turn = 2
            if(text == "RIGHT"): turn = 3
            while True:
                got.mecanum_turn_speed_times(turn=turn, speed=30, times=20, unit=2)
                line_type, _, _ = line_follow(mult=0.25, speed=0)
                if line_type == 1:
                    print("Turned and see line")
                    break
            break

    # Go the rest of the way to the end of the line and stop.
    print("Going to the end of the line...")
    while True:
        line_type, _, _ = line_follow(mult=0.25, speed=15)
        if line_type in [0,2]:
            while True:
                got.mecanum_turn_speed_times(turn=turn, speed=30, times=20, unit=2)
                line_type, _, _ = line_follow(mult=0.25, speed=0)
                if line_type == 1:
                    print("Turned and see line")
                    break
            print("can not see path anymore, stopping.")
            break

    got.mecanum_stop()
    time.sleep(5)
    #Challenge 3: Face Recognition and Personalized Greeting
    print("Starting challenge 3: Look for a registered face and greet them by name")
    #Pose recognition control: look for registered faces, and if see one, greet them by name on the screen.
    print("Starting pose recognition...")
    run_pose_control_inline(
        robot_ip="192.168.88.1",
        forward_speed=30,
        backward_speed=30,
        turn_speed=45,
        camera_index=1,
        model_path="yolov8n-pose.pt",
        up_margin_factor=0.6,
        down_margin_factor=0.6,
        min_conf=0.3,
        enable_robot=True,  # <-- Robot is ENABLED: it will now move!
        debounce_frames=2,
        max_frames=None,
        got=got,
    )

    # Looking for face and move towards box, release april tag
    print("Starting face recognition...")
    TARGET_NAME = input("Name of the person to find: ")
    face_find_and_approach(
        gap=13,
        target_name=TARGET_NAME,
        turn_spd=10,
        strafe_spd=10,
        fwd_spd=10,
        height=120,
        adjust_turn=10,
    )
    got.mecanum_move_speed_times(
        direction=1, speed=20, times=15, unit=1
    )  # Go backwards a bit to not hit face
    got.mechanical_joint_control(angle1=0, angle2=-30, angle3=-30, duration=500)
    time.sleep(1)
    got.mechanical_clamp_release()
    time.sleep(1)
    got.mechanical_joint_control(angle1=0, angle2=45, angle3=45, duration=500)
    got.mechanical_clamp_release()

except KeyboardInterrupt:
    # Safety stop if the cell is interrupted manually.
    print("Done")