import os, signal

class Responder:
    def __init__(self, mode):
        self.mode = mode

    def act(self, pid):
        if self.mode == "safe":
            return "Alert only"
        try:
            os.kill(pid, signal.SIGKILL)
            return "Process killed"
        except:
            return "Kill failed"
