import sys
import traceback
import ulispreadline

print("Unknown Lisp Version 0.0.1 - Dhruv Jauhar")
while True:
    try:
        line = ulispreadline.readline()
        if line in ["(exit)", "exit", None]:
            break
        if line == "":
            continue
        print(line)
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))