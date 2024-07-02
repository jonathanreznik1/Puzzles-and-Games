import pyfirmata
import time
import sys
import os

board = pyfirmata.Arduino('COM3')

# Version 2 has a progress bar implementation

# Warmup exercise - how many times can you press the button in 2 seconds, 5 seconds, 10 seconds, 15 seconds

it = pyfirmata.util.Iterator(board)

it.start()

board.digital[10].mode = pyfirmata.INPUT


cls = lambda: os.system('cls')
cls()

print("Hi Alejandra, I made a game for you while you were away.")
print("Here's the rules, it requires the small electronic kit with push button.")
print("The goal is to push the button as many times as you can in 2, 5, 10, and 15 seconds.")
time.sleep(5)
print("Ready to play?")
time.sleep(10)

trials = [2,5,10,15]

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')
 

for seconds in trials:
    press_count = 0

    print(seconds, "second test starting in: ", end="")

    for remaining in range(3, 0, -1):
        # sys.stdout.write("\r")
        # sys.stdout.write(str(seconds)+" ") 
        # sys.stdout.write("second test starting in: {:2d}".format(remaining))
        sys.stdout.write("{:2d}".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    print("\rNOW, GO GO GO! PRESS THE BUTTON QUICKLY")
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            # print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
            break
        sw = board.digital[10].read()
        progbar(press_count, seconds*4, 20)
        if sw is True: 
            press_count+=1      #consider moving this to end of the block
            progbar(press_count, seconds*4, 20)
            sys.stdout.flush()
            board.digital[13].write(1)
        else:
            board.digital[13].write(0)
        time.sleep(0.1)

    print(press_count)


# Quiz
print("That was just a warmup, are you ready for a real test? Press the push button to begin.")
time.sleep(1)
while True:
    sw = board.digital[10].read()
    if sw is True:
        #For each question you have
        print("Just kidding bye :-* . That was the quiz not the warmup.")
        break