import subprocess
import pickle
import re
from datetime import datetime
from itertools import tee
from itertools import izip_longest as zip_longest

def process(msgstr):
    uni = msgstr.decode("utf-8")
    today = datetime.today()
    date_format = today.strftime("%Y-%m-%d")
    stripped = re.sub(r'/tmp/.*?/|-' + date_format + r'-\d+', '', uni)
    msg_starts = [match.start() for match in re.finditer(r'.*\.(cpp|c): |In file included from .*\.', stripped)]
    if len(msg_starts) == 0: return [stripped]
    start, end = tee(msg_starts)
    next(end)
    return [stripped[i:j] for i, j in zip_longest(start, end) if "style of line directive is a GCC extension" not in stripped[i:j]]

class Success:
    def __init__(self, warnings):
        self.msgs = process(warnings)

class Error:
    def __init__(self, msgs):
        self.msgs = process(msgs)

def compile(source_path, object_path, compiler_name='g++', flags=''):
    print("compiling " + source_path + " to " + object_path + " using " + compiler_name)
    cargs = [compiler_name, "-c", source_path, "-o", object_path] + flags.split(" ")
    print("running: " + " ".join(cargs))
    # if this succeeds we wrap the result up in a Success object
    try:
        return True, pickle.dumps(Success(subprocess.check_output([arg for arg in cargs if arg != ""], stderr=subprocess.STDOUT)))
    # otherwise we return an Error object
    except subprocess.CalledProcessError as e:
        return False, pickle.dumps(Error(e.output))
