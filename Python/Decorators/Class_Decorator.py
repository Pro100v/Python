import functools
import time
import types


class TimeItCritical:
    DEFAULT_CRITICAL_TIME = 0.5

    def __new__(cls, obj=None, *, critical_time=DEFAULT_CRITICAL_TIME):
        """
        Вызывается до __init__, поэтому мы можем посмотреть, что у нас
        фунция или класс, если класс – то продолжим создание класса, а если функция, то
        сразу обернем ее и вернем уже не класс, а функцию
        """
        if obj:
            # случай без параметра @TimeItCritical
            if isinstance(obj, types.FunctionType):
                # print("Вызываем статическую функцию return cls.timeit(obj, critical_time)")
                return cls.timeit(obj, critical_time)
            else:
                # print("Вызываем статическую функцию return return cls.wrap_all_methods(obj, critical_time)")
                return cls.wrap_all_methods(obj, critical_time)
        else:
            # случай с параметром @TimeItCritical(critical_time=0.3)
            # print("Вызываем конструктор TimeItCritical")
            # return super().__new__(cls)
            return super(TimeItCritical, cls).__new__(cls) 
            

    def __init__(self, critical_time=DEFAULT_CRITICAL_TIME):
        """
        Нужен только, чтобы задать critical_time при вызове с параметром!
        """
        # print("TimeItCritical.__init__", self, critical_time)
        self.critical_time = critical_time

    def __call__(self, obj):
        """
        Вызывается в случае вызова с параметром!
        """
        if isinstance(obj, types.FunctionType):
            return self.timeit(obj, self.critical_time)
        else:
            return self.wrap_all_methods(obj, self.critical_time)

    @staticmethod
    def timeit(method, critical_time, desc=''):
        """
        замеряет время выполнения метода и
        если оно превышает пороговое значение в self.critical_time выводит сообщение
        """
        @functools.wraps(method)
        def timeit_wrapper(*args, **kwargs):
            ts = time.monotonic()
            res = method(*args, **kwargs)
            te = time.monotonic()
            delta = te - ts
            # timeit_wrapper.time_exec = delta
            if delta > critical_time:
                print(f"{desc}{method.__name__} executed slow: {delta:2.2f} sec")
            return res

        # timeit_wrapper.time_exec = 0
        return timeit_wrapper

    @staticmethod
    def wrap_all_methods(obj, critical_time):
        @functools.wraps(obj, updated=[])
        class FakeCls():
            def __init__(cls, *cls_args, **cls_kwargs):
                # проксируем конструктор
                cls.obj = obj(*cls_args, **cls_kwargs)

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
                    return TimeItCritical.timeit(attrib, critical_time, f"Method {obj!r}.")
                else:
                    return attrib

        return FakeCls


# @TimeItCritical(critical_time=0.8)
@TimeItCritical
class Foo:
    def a(self):
        print("медленный метод начался")
        time.sleep(1.0)
        print("медленный метод кончился")

    def b(self):
        time.sleep(0.1)
        print('быстрый метод')


@TimeItCritical(critical_time=0.3)
# @TimeItCritical
def foofoo(name):
    """
    декорированная ф-ция
    :param name:
    :return:
    """
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
    print(type(foofoo))
    print(foofoo)


if __name__ == '__main__':
    main()
