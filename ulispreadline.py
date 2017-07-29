import os
import sys
import logging
import readline as rl


logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

prompt = "ulisp> "
history_loaded = False

if sys.version_info[0] >= 3:
    input = input
else:
    input = raw_input

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
            logger.info("No history file found.")
    try:
        line = input(prompt)
        rl.add_history(line)
        with open(history_file, "a") as hf:
            hf.write(line + '\n')
    except IOError:
        pass
    except EOFError:
        return None
    return line

