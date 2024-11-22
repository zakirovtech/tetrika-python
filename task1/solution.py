def strict(func):
    def wrapper(*args, **kwargs):
        if not func.__annotations__:
            return func(*args, **kwargs)

        if args:
            types = list(func.__annotations__.values())
            check_args = [*args]

            for i, arg in enumerate(check_args):
                if type(arg) != types[i]:
                    raise TypeError
        
        if kwargs:
            types = func.__annotations__
            check_kwargs = {**kwargs}
            
            for key, value in check_kwargs.items():
                if type(value) != types[key]:
                    raise TypeError

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_int(a: int, b: int) -> int:
    return a + int(b)


@strict
def sum_intchar_str(a: int, b: str):
    return a + int(b)


@strict
def sum_bool(a: bool, b: bool):
    return a + b


@strict
def sum_bool_int(a: bool, b: bool):
    return a + b


@strict
def concat(a: str, b: str):
    return str(a) + str(b)
