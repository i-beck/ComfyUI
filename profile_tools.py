import time
from line_profiler import LineProfiler
from functools import wraps
from contextlib import contextmanager
import inspect
import sys



def profile_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = LineProfiler()
        profiler.add_function(func)
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        profiler.print_stats()
        return result
    return wrapper





def profile_decorator2(func):
    unset = True
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = LineProfiler()
        profiler.add_function(func)
        profiler.enable()
        result = unset
        try:
            if inspect.iscoroutinefunction(func):
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(func(*args, **kwargs))
                loop.close()
            else:
                result = func(*args, **kwargs)
        except BaseException as _:
            raise
        finally:
            profiler.disable()
            profiler.print_stats()
        if result is not unset:
            return result
        return
    return wrapper




# Usage:
@profile_decorator
def my_function(no_recurs=False):
    print("ima function")
    time.sleep(3)
    if no_recurs:
        return
    # function code here
    inner_function()
    print("ima still a function")

def inner_function():
    # inner function code here
    inner_inner_function()
    time.sleep(1)
    print("cool man cool")
    my_function(no_recurs=True)
    inner_inner_function()

def inner_inner_function():
    # inner function code here
    time.sleep(4)
    print("cool man cool man cool X 2")
    my_function(no_recurs=True)
    


if __name__ == '__main__':
    my_function()