import functools
import time
from Class_Decorator import TimeItCritical as timeit

def slow_down(_func=None, *, rate=1):
    """Sleep given amount of seconds before calling the function"""
    def decorator_slow_down(func):
        @functools.wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(rate)
            return func(*args, **kwargs)
        return wrapper_slow_down

    if _func is None:
        return decorator_slow_down
    else:
        return decorator_slow_down(_func)


def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def _singleton(*args, **kwargs):
        if not _singleton.instance:
            _singleton.instance = cls(*args, **kwargs)
        return _singleton.instance
    _singleton.instance = None
    return _singleton


@singleton
class Foo:
    def __init__(self, init=321):
        self.init = init


def cache(func):
    """Keep a cache of previous function calls"""
    @functools.wraps(func)
    def _cache(*args, **kwargs):
        arg_key = args + tuple(kwargs.items())
        if arg_key not in _cache.cache:
            _cache.cache[arg_key] = func(*args, **kwargs)
        return _cache.cache[arg_key]
    _cache.cache = dict()
    return _cache

# @count_calls
@slow_down
def countdown(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1)




@count_calls
def fibonacci_1(num):
    if num < 2:
        return num
    return fibonacci_1(num - 1) + fibonacci_1(num - 2)



@cache
@count_calls
def fibonacci_2(num):
    if num < 2:
        return num
    return fibonacci_2(num - 1) + fibonacci_2(num - 2)


if __name__ == '__main__':
    
    # тест декоратора с засыпанием
    # countdown(3)

    # тест декоратора с паттерном singleton
    # f = Foo(5)
    # print(f, f.init)
    # ff = Foo(105)
    # print(ff, ff.init)
    # print("Foo(5) == Foo(125):", Foo(5)==Foo(125))

    # тест рекурсивного вывода на примере расчета числа фибоначи
    print("Фибоначи 10:", fibonacci_1(10), fibonacci_1.num_calls)
    print("Фибоначи 8:", fibonacci_2(8))
    print("Фибоначи 10:", fibonacci_2(10))
    
    
    

    


    