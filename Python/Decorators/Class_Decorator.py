# print("Hello, world!!")
import functools
import time 

class TimeItCritical:
    def __init__(self, obj=None,* , critical_time=0.5):
        functools.update_wrapper(self, obj)
        self._cls = None
        self._func = None
        if isinstance(obj, type(TimeItCritical)):
            self._cls = obj
            self.wrap_all_methods()
        if isinstance(obj, type(self.__init__)):
            self._func = obj
        self.critical_time = critical_time

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            obj = args[0]
            functools.update_wrapper(self, obj)
            if isinstance(obj, type(TimeItCritical)):
                self._cls = obj
                return self.wrap_all_methods()
            if isinstance(obj, type(self.__init__)):
                self._func = obj
                return self
        else:
            # ts = time.time()
            # res = self.func(*args, **kwargs)
            # te = time.time()
            # print(f"{self.func.__name__!r} executed by {te-ts:2.2f} sec")
            return self.timeit_wrapper

    def timeit_wrapper(self, *args, **kwargs):
        ts = time.time()
        res = self.func(*args, **kwargs)
        te = time.time()
        delta = te - ts
        if delta > self.critical_time:
            print(f"{self.func.__name__!r} executed slow: {delta:2.2f} sec")
        return res
    
    def wrap_all_methods(self):
        class FakeCls():
            def __init__(cls, *args, **kwargs):
                self.obj = self._cls(*args, **kwargs)

            def __getattribute__(self, stuff):
                try:
                    # ищем атрибут в родительском классе
                    attrib = super().__getattribute__(stuff)
                except AttributeError:
                    pass
                else:
                    # если нажодим то ничего не делаем, просто возвращаем его
                    return attrib
                
                # Ищем атрибут в задикарируемом объекте
                attrib = self.obj.__getattribute__(stuff)

                # Проверка на принадлежность атрибута методу
                if isinstance(attrib, type(self.__init__)):
                    return self.timeit_wrapper(attrib)
                else:
                    return attrib
        return FakeCls    

# @TimeItCritical
# def foo(name):
#     print("Hello ", end="")
#     for i in list(name):
#         time.sleep(0.8)
#         print(i, end="")


@TimeItCritical(critical_time=0.3)
class Foo:
    def a(self):
        print("медленный метод начался")
        time.sleep(1.0)
        print("медленный метод кончился")
    def b(self):
        time.sleep(0.1)
        print('быстрый метод')
f = Foo()
f.a()
f.b()
