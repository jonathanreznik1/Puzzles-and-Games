import pyfirmata
import time
import sys

board = pyfirmata.Arduino('COM3')


# Warmup exercise - how many times can you press the button in 2 seconds, 5 seconds, 10 seconds, 15 seconds


it = pyfirmata.util.Iterator(board)

it.start()

board.digital[10].mode = pyfirmata.INPUT

print("Push the button faster and try 2, 5, 10, and 15 seconds length.")
time.sleep(1)
print("Ready to play?")
time.sleep(3)

trials = [2,5,10,15]

for seconds in trials:
    press_count = 0
    print(seconds, " second test starting...")
    time.sleep(1)
    print("now, GO GO GO")
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            # print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
            break
        sw = board.digital[10].read()
        if sw is True:
            sys.stdout.write(".")
            press_count+=1
            board.digital[13].write(1)
        else:
            board.digital[13].write(0)
        time.sleep(0.1)

    print(press_count)


# Quiz
print("That was just a warmup, now you are ready for the Quiz - press button to begin")
while True:
    sw = board.digital[10].read()
    if sw is True:
        #For each question you have
        print("thanks")