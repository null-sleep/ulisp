import signal
import time
 
def sigint_handler(signum, frame):
    print(signum)
    print(frame.__repr__())
    print('Stop pressing the CTRL+C!')
 
signal.signal(signal.SIGINT, sigint_handler)
 
def main():
    while True:
       inp = input()
       print(inp)
 
##########
 
if __name__ == "__main__":
    main()