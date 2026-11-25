# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       eeeng                                                        #
# 	Created:      9/25/2026, 7:35:37 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #



from vex import *


#ignore this line--just for my pc bug to push code to github through terminal: git push origin dr4b-scoring-updates
# Library imports

# Brain
brain = Brain()
drive_control = Controller(PRIMARY)

# Drivetrain motors/groups defined
motor_rf = Motor(Ports.PORT1,GearSetting.RATIO_18_1, False)
motor_lb = Motor(Ports.PORT10,GearSetting.RATIO_18_1, True)
motor_lf = Motor(Ports.PORT2,GearSetting.RATIO_18_1, True)
motor_rb = Motor(Ports.PORT9,GearSetting.RATIO_18_1, False)
Ldrivetrain = MotorGroup(motor_rf, motor_rb)
Rdrivetrain = MotorGroup(motor_lf, motor_lb)
drivetrain = DriveTrain(Ldrivetrain,Rdrivetrain)

# Mechanics/Elevator motor/groups defined
elevator_motorR = Motor(Ports.PORT3,GearSetting.RATIO_18_1,False)
elevator_motorL = Motor(Ports.PORT4,GearSetting.RATIO_18_1,True)
elevator_full = MotorGroup(elevator_motorL,elevator_motorR)

claw_angle_motor = Motor(Ports.PORT20)
piston = Pneumatics(brain.three_wire_port.a)

claw_closed = True

 #auton
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    drivetrain.set_stopping(BRAKE)
    
    #example:
    drivetrain.drive(FORWARD, 100, PERCENT)
    wait(200, MSEC)
    drivetrain.stop()

    #forwards

    #turn right 90

    #forwards

    #open claw

    #reverse

    #turn left 90

    #forwards slow + intake

    #close + intake still running short time after + lift up 

    #drive forward lil bit until middle of 4 mats

    #turn right 135

    #lift up + forwards

    #score

    #reverse 1/2 of forward in line 74

    #turn left 90

    #forwards slow 1/2 of forward in line 74 + intake

    #close + intake still running short time after + lift up

    #forward lil bit until middle of 4 mats

    #turn right 45

    #forwards half distance

    #lift up, lift up + forwards 

    #score

        




    

    

    



# driving
def deadband(value, threshold=5):
    return 0 if abs(value) < threshold else value

# Helper function to ease the current value towards the target
def slew(current, target, step):
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return target

def driving_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    
    # Store the current speeds outside the loop
    current_forward = 0
    current_turn = 0
    
    # Maximum change per 20ms loop (lower = smoother/slower acceleration)
    accel_step = 5 
    turn_accel_step = 15
    while True:
        # Get target speeds from the controller
        target_forward = deadband(drive_control.axis3.position())
        target_turn = deadband(drive_control.axis1.position())


        #I thought turn speed to fast, lowering by % to make allighning easier
        target_turn *= 0.4


        # Crawl Mode if Lift is above Stage 1 (180 degrees currently)
        if current_level > 1:
            target_forward *= 0.2
            target_turn *= 0.25

        if drive_control.buttonR2.pressing() and current_level < 1:
            target_forward *= 0.25
            target_turn *= 0.25

        if current_forward < 0 and current_level < 1 and claw_closed == True:
            level_up()


        # Ease current speeds toward the target speeds
        current_forward = slew(current_forward, target_forward, accel_step)
        current_turn = slew(current_turn, target_turn, turn_accel_step)

        # Apply the eased speeds to the motors
        Ldrivetrain.spin(FORWARD, (current_forward + current_turn), PERCENT)
        Rdrivetrain.spin(FORWARD, (current_forward - current_turn), PERCENT)
        
        wait(20, MSEC)

# elevator
def elevator_up():
    elevator_full.spin(FORWARD, 100, PERCENT)
def elevator_down():
    elevator_full.spin(REVERSE, 100, PERCENT)
def elevator_stop():
    elevator_full.stop()



# claw intake wheel spin
def rotate_up():
    claw_angle_motor.spin(FORWARD, 100, PERCENT)
def rotate_down():
    claw_angle_motor.spin(REVERSE, 100, PERCENT)
def rotate_stop():
    claw_angle_motor.stop()

# claw grip
def close_grip():
    global claw_closed
    claw_closed = False
    piston.open()
    #claw_angle_motor.spin(FORWARD, 70, PERCENT)

def open_grip():
    global claw_closed
    claw_closed = True
    piston.close()
    #claw_angle_motor.stop()

# create competition instance
comp = Competition(driving_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

elevator_motorR.set_stopping(HOLD)
elevator_motorL.set_stopping(HOLD)
claw_angle_motor.set_stopping(HOLD)

#drive_control.buttonL1.pressed(elevator_up)
#drive_control.buttonL1.released(elevator_stop)

#drive_control.buttonL2.pressed(elevator_down)
#drive_control.buttonL2.released(elevator_stop)

drive_control.buttonR1.pressed(rotate_up)
drive_control.buttonR1.released(rotate_stop)

drive_control.buttonR2.pressed(rotate_down)
drive_control.buttonR2.released(rotate_stop)

drive_control.buttonA.pressed(open_grip)  # this closes it, its named wrong
drive_control.buttonB.pressed(close_grip) # this opens it, its named wrong


# DR4B ELEVATOR HEIGHT PRESETS


# 0 = bottom of elevator

#LEVEL_POSITIONS = [0, 180, 360, 540, 720, 900] #for geared drivetrain - will costomize later - test trial degrees
LEVEL_POSITIONS = [0, 130, 310, 490, 680, 850] #for non-geared drivetrain
# CUSTOMIZE ELEVATOR SPEED
PRESET_SPEED = 70  # Percent

DOWN_PRESET_SPEED = 50
# Tracks the requested scoring level
current_level = 0

# Maximum available level
MAX_LEVEL = len(LEVEL_POSITIONS) - 1

NEXT_LEVEL = 1
# ELEVATOR POSITION RESET

# Only start the program with the elevator at the bottom.
elevator_motorR.set_position(0, DEGREES)
elevator_motorL.set_position(0, DEGREES)

# PRESET MOVEMENT

def move_to_level():
    target = LEVEL_POSITIONS[current_level]

    elevator_full.spin_to_position(
        target, DEGREES, PRESET_SPEED, PERCENT,
        wait=False
    )


def level_up():
    global current_level

    if current_level < MAX_LEVEL:
        current_level += 1
        move_to_level()


# scores and lower back to stage 0-claw is left open for intake
def score():
    global current_level
    global NEXT_LEVEL

    # Prevent scoring at Level 0
    if current_level < 1:

        return

    

    # Step 1: Calculate the lowering position for ANY level
    gap = LEVEL_POSITIONS[current_level] - LEVEL_POSITIONS[current_level - 1]
    target = LEVEL_POSITIONS[current_level] - (gap * 0.45)

    if current_level == 4 or current_level == 5:
        claw_angle_motor.spin_for(
        FORWARD, 95, DEGREES, 70, PERCENT,
        wait=True
        )
        claw_angle_motor.spin_for(
        FORWARD, 95, DEGREES, 70, PERCENT,
        wait=False
        )
        wait(100, MSEC)

    # Step 2: Lower elevator
    elevator_full.spin_to_position(
        target, DEGREES, DOWN_PRESET_SPEED, PERCENT,
        wait=True
    )


    # Step 3: Opens claw
    close_grip()
    wait(150, MSEC)

    #dont need anymore--it didn't work to begin with lol--
    #add drive backwards to clear the scoring area
    #drivetrain.drive(REVERSE, 20, PERCENT)
    #wait(200, MSEC)


    #dont need anymore w/ new claw design, can no longer rotate the claw downwards- maybe later someday, but with different
    # Step 4: Rotate claw downward
    #claw_angle_motor.spin_for(
     #   REVERSE, 450, DEGREES, 70, PERCENT,
      #  wait=True
    #)
    # rename and use claw_angle_motor.spin--> for the wheels to intake

    # Step 5: Return elevator to Level 1

    NEXT_LEVEL = min(current_level + 1, MAX_LEVEL)

    current_level = 0

    elevator_full.spin_to_position(
        LEVEL_POSITIONS[0], DEGREES, PRESET_SPEED, PERCENT,
        wait=True
    )

def last_level_plus_one():
    global current_level

    current_level = NEXT_LEVEL
    move_to_level()


def level_bottom():
    global current_level

    current_level = 0
    move_to_level()


def level_top():
    global current_level

    current_level = MAX_LEVEL
    move_to_level()

# CONTROLLER ARROW BUTTONS

# UP: Move one scoring level higher
drive_control.buttonUp.pressed(level_up)

# DOWN: Scores and returns to bottom + 1--current is going to level_bottom
drive_control.buttonDown.pressed(level_bottom)

# LEFT: Return to bottom if switch to level_bottom-- current --> if driver wants : Scores and returns to bottom + 1
drive_control.buttonLeft.pressed(score)

# RIGHT: Move to highest level
drive_control.buttonRight.pressed(level_top)

# X: Moves to the next level of the previous scored pin
drive_control.buttonX.pressed(last_level_plus_one)
