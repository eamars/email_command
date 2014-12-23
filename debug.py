#define debug log levels
RELEASE = 0
DEBUG = 1
ERROR = 2

DEBUG_SYMBOL = {
    RELEASE: "RELEASE",
    DEBUG: "DEBUG",
    ERROR: "ERROR"
}

class Debugger:
    def __init__(self, level):
        self.DEBUG_LEVEL = level

    def log(self, level, message, s_end='\n'):
        if level >= self.DEBUG_LEVEL:
            print("{}: {}".format(DEBUG_SYMBOL[level], message), end=s_end)
