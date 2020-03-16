import functools
import time 

class TimeItCritical:
    def __init__(self, obj=None, * , critical_time=0.1):
        functools.update_wrapper(self, obj)
        self._cls = None
        self._func = None
        self.critical_time = critical_time
        # если обворачиваемый объект является классом
        if isinstance(obj, type(TimeItCritical)):
            self._cls = obj
            # obj = self.wrap_all_methods()  
        # если обворачиваемый объект является функцией
        if isinstance(obj, type(self.__init__)):
            self._func = obj
        

    def __call__(self, *args, **kwargs):
        arg = ', '.join(map(str,args))
        kwarg = ', '.join([f", {k}:{v}" for k,v in kwargs.items()])
        print(f"__call__({arg}{kwarg})")
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
            if self._cls:
                return self.wrap_all_methods()(*args, **kwargs)
            else:
                # return self.timeit
                ts = time.time()
                res = self._func(*args, **kwargs)
                te = time.time()
                print(f"{self._func.__name__!r} executed by {te-ts:2.2f} sec")
                return self.timeit

    def timeit(self, method):
        def timeit_wrapper(*args, **kwargs):
            ts = time.time()
            res = method(*args, **kwargs)
            te = time.time()
            delta = te - ts
            if delta > self.critical_time:
                print(f"{method.__name__!r} executed slow: {delta:2.2f} sec")
            return res
        return timeit_wrapper
    
    def wrap_all_methods(self):
        class FakeCls():
            def __init__(cls, *cls_args, **cls_kwargs):
                cls.obj = self._cls(*cls_args, **cls_kwargs)

            def __getattribute__(cls, atr):
                try:
                    # ищем атрибут в родительском классе
                    attrib = super().__getattribute__(atr)                    
                except AttributeError as e:
                    # print(e)
                    pass
                else:
                    # если нажодим то ничего не делаем, просто возвращаем его
                    return attrib
                
                # Ищем атрибут в задикарируемом объекте
                attrib = cls.obj.__getattribute__(atr)                

                # Проверка на принадлежность атрибута методу
                if isinstance(attrib, type(cls.__init__)):
                    return self.timeit(attrib)
                else:
                    return attrib
        return FakeCls    

# @TimeItCritical
# def foo(name):
#     print("Hello ", end="")
#     for i in list(name):
#         time.sleep(0.8)
#         print(i, end="")


# @TimeItCritical(critical_time=0.3)
@TimeItCritical
class Foo:
    # def __init__(self, num=1):
    #     self.num = num
    def __init__(self):
        pass

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

@TimeItCritical(critical_time=0.3)
def foofoo(name):
    time.sleep(1.0)
    print(f"Hello, {name}")

foofoo('Peter')
