import pyfirmata
import time

board = pyfirmata.Arduino('COM3')


it = pyfirmata.util.Iterator(board)

it.start()


board.digital[10].mode = pyfirmata.INPUT

while True:
    sw = board.digital[10].read()
    if sw is True:
        board.digital[13].write(0)
    else:
        board.digital[13].write(1)
    time.sleep(0.1)

# Test of blinking light
# while True:
#     board.digital[13].write(1)
#     time.sleep(5)
#     board.digital[13].write(0)
#     time.sleep(1)