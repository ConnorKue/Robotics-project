from nanonav import BLE, NanoBot
import time



#takes in the two times which the sensors passed the white line, moves the opposite
#wheel by that amount of time
def adjust(robot, t, t2):
    if t  < t2:
        robot.m1_forward(25)
        print("dif: " + str(((t2-t)/1000000000)))
        time.sleep(((t2-t)/1000000000))
        robot.stop()
    elif t > t2:
        robot.m2_forward(25)
        print("dif: " + str(((t-t2)/1000000000)))
        time.sleep(((t-t2)/1000000000))
        robot.stop()


def moveForward(robot):
    #start moving forward
    robot.m1_forward(25)
    robot.m2_forward(25)
    t = 0.0
    t2 = 0.0
    left = False
    right = False
    #goes unil both sensors have been activated
    while not (left and right):

        if robot.ir_left() and not left:
            t = time.time_ns()
            left = True
            print("right: " + str(right) + " left: " + str(left))
        if robot.ir_right()and not right:
            t2 = time.time_ns()
            right = True
            print("right: " + str(right) + " left: " + str(left))
    print("t: " + str(t) + " t2: " + str(t2))

    robot.stop()
    #fixes orientation
    adjust(robot, t, t2)
    #keeps moving until it hopefully gets to the center of the square
    robot.m1_forward(25)
    robot.m2_forward(25)

    time.sleep(.8)

    robot.stop()



def turnLeft(robot):
    robot.m1_forward(20)
    time.sleep(.75)
    robot.stop()

def turnRight(robot):
    robot.m2_forward(20)
    time.sleep(.75)
    robot.stop()

def moveLeft(robot):
    turnLeft(robot)
    moveForward(robot)

def moveRight(robot):
    turnRight(robot)
    moveForward(robot)


### test motors and encoders ###

# Create a NanoBot object
robot = NanoBot()

# Move forward for 2 seconds
# print(f'encoder 1 start: {robot.get_enc1()}')
# robot.m1_forward(30)
# robot.m2_forward(30)
# time.sleep(2)
# print(f'encoder 1 end: {robot.get_enc1()}')

# # Stop
# robot.stop()
# time.sleep(2)

# # Move backward for 2 seconds
# print(f'encoder 2 start: {robot.get_enc2()}')
# robot.m1_backward(30)
# robot.m2_backward(30)
# time.sleep(2)
# print(f'encoder 2 end: {robot.get_enc2()}')

# # Stop
# robot.stop()

### test Bluetooth ###

# Create a Bluetooth object
# ble = BLE(name="Bram")

# ble.send(43)
# response = ble.read()
# # wait until something changes, indicating a response
# while response == 43:
#     response = ble.read()
#     time.sleep(0.5)

# print("Received: ", response)

### test ir sensors ###

moveForward(robot)
moveLeft(robot)
moveLeft(robot)
moveLeft(robot)

