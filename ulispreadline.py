import os
import sys
import logging
import readline as rl

PROMPT = "ulisp> "

history_loaded = False

def readline():
    global prompt
    global history_loaded
    history_file = os.path.expanduser("~/.ulisp_history")
    if not history_loaded:
        history_loaded = True
        try:
            with open(history_file, "r") as hf:
                for hist_line in hf.readlines():
                    rl.add_history(hist_line.rstrip("\r\n"))
        except IOError:
            print("No history file found. Creating at {}".format(history_file))
    try:
        line = input(PROMPT)
        rl.add_history(line)
        with open(history_file, "a") as hf:
            hf.write(line + '\n')
    except IOError:
        pass
    except EOFError:
        # Ctrl + D handler
        return None
    return line

