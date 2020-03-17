import functools
import time 
import types

class TimeItCritical:
    def __init__(self, obj=None, * , critical_time=0.5):
        self._cls = None
        self._func = None
        self.critical_time = critical_time
        functools.update_wrapper(self, obj)
        # если обворачиваемый объект является классом, вызывается при декорировании без параметров
        # decorator(obj=class|function)
        if isinstance(obj, type(TimeItCritical)):
            self._cls = obj            
        # если обворачиваемый объект является функцией, вызывается при декорировании без параметров
        if isinstance(obj, types.FunctionType):
            self._func = obj
        

    def __call__(self, *args, **kwargs):
        # arg = ', '.join(map(str,args))
        # kwarg = ', '.join([f", {k}:{v}" for k,v in kwargs.items()])
        # print(f"__call__({arg}{kwarg})")
        
        if len(args) == 1 and callable(args[0]):
            # вызывается, когда декоратор был определен с параметрами
            # decorator(arg1='', arg2='',...)(class|function)
            obj = args[0]            
            functools.update_wrapper(self, obj)
            if isinstance(obj, type(TimeItCritical)):
                self._cls = obj
                return self.wrap_all_methods() 
            if isinstance(obj, types.FunctionType):                
                self._func = obj
                return self.timeit(obj)
        else:            
            if self._cls:
                return self.wrap_all_methods()(*args, **kwargs)
            elif self._func:
                return self.timeit(self._func)(*args, **kwargs)
            else:
                raise NotImplementedError("Use case not defined")
                
    def timeit(self, method):
        """
        замеряет время выполнения метода и 
        если оно превышает пороговое значение в self.critical_time выводит сообщение
        """
        @functools.wraps(method)
        def timeit_wrapper(*args, **kwargs):
            ts = time.time()            
            res = method(*args, **kwargs)
            te = time.time()
            delta = te - ts
            if delta > self.critical_time:
                cls_name = str((self._cls.__name__))+'.' if self._cls else ''
                print(f"{cls_name}<{type(method).__name__} {method.__name__!r}> executed slow: {delta:2.2f} sec")
            return res
        return timeit_wrapper
    
    def wrap_all_methods(self):
        class FakeCls():
            def __init__(cls, *cls_args, **cls_kwargs):
                # проксируем конструктор                 
                cls.obj = self._cls(*cls_args, **cls_kwargs)

            def __getattribute__(cls, atr):
                try:
                    # ищем атрибут в родительском классе
                    attrib = super().__getattribute__(atr)                    
                except AttributeError:                    
                    pass
                else:
                    # если находим то ничего не делаем, просто возвращаем его
                    return attrib
                
                # Ищем атрибут в задикарируемом объекте
                attrib = cls.obj.__getattribute__(atr)                

                # Проверка на принадлежность атрибута методу
                if isinstance(attrib, type(cls.__init__)):                    
                    return self.timeit(attrib)
                else:
                    return attrib
        return FakeCls


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


# @TimeItCritical(critical_time=0.3)
@TimeItCritical
def foofoo(name):
    time.sleep(1.0)
    print(f"Hello, {name}")

def main():
    print('\n\nclass test')
    f = Foo()
    f.a()
    f.b()

    print()
    print(type(f))
    print(f.__class__.__name__)
    print(f.a)

    print('\n\nfunction test')
    foofoo('Peter')    
    print()
    print(foofoo)

if __name__=='__main__':
    main()



