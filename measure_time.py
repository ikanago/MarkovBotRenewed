from functools import wraps
import time
import os


def measure_time(func):
    """
    measure time to execute function in the argument
    :param func: function to measure execution time
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print(str(func.__name__) + " took " + str(elapsed_time) + " seconds." + os.linesep)
        return result
    return wrapper
