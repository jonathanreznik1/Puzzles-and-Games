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


#Console output clear and then game instructions printed
cls = lambda: os.system('cls')
cls()

print("Hi, I made a game for you while you were away.")
print("(Updated rules)")
print("Here's the rules, utilize the small electronic kit with push button for the controls.")
print("The goal is to get the button registering in excess of 4 times per second for each trial.")
print("Watch out though, holding the button will register it for up to 3 times before you are forced to press it again.")
time.sleep(10)
print("Ready to play?",end="")
time.sleep(7)
print(' best of luck!')

trials = [5,10,15,25]

def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')
 
for seconds in trials:

    if seconds == 25:
        print("Those were just warmups, are you ready for the marathon? Press the push button to begin.")
        time.sleep(1)
        while True:
            sw = board.digital[10].read()
            if sw is True:
                 break

    press_count = 0
    time.sleep(2)
    print()
    print(seconds, "second trial, push button to begin")
    while True:
        sw = board.digital[10].read()
        if sw is False:
            continue
        else:
            print("Starting in: ", end="")
            break
    
    for remaining in range(3, 0, -1):
        # sys.stdout.write("\r")
        # sys.stdout.write(str(seconds)+" ") 
        # sys.stdout.write("second test starting in: {:2d}".format(remaining))
        sys.stdout.write("{:2d}".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


    print("\rNOW, GO GO GO! PRESS THE BUTTON QUICKLY")
    start_time = time.time()
    push_btn_off = False

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            # print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
            break
        sys.stdout.write("\t Elapsed Time: ")
        sys.stdout.write(str(int(elapsed_time)))
        sw = board.digital[10].read()
        progbar(press_count, seconds*4, 20)
        if sw is True: 
            if push_btn_off is True:
                press_count+=1      #consider moving this to end of the block
            progbar(press_count, seconds*4, 20)
            sys.stdout.flush()
            board.digital[13].write(1)
            if press_count % 3 == 0:
                push_btn_off = False
        else:
            board.digital[13].write(0)
            push_btn_off = True
        time.sleep(0.1)
        board.digital[13].write(0)            

    print('                   You did', press_count, 'of', seconds*4, 'which is ', end='')
    if press_count/(seconds*4) < 1:
        print('bad')
    else:
        print('good')


