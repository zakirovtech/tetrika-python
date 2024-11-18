def strict(func):
    def wrapper(*args, **kwargs):
        if not func.__annotations__:
            return func(*args, **kwargs)

        check = [*args]
        
        if kwargs:
            check = check + list(kwargs.values())
            
        types = list(func.__annotations__.values())
        print(types)
        for i, arg in enumerate(check):
            if not isinstance(arg, types[i]):
                raise TypeError

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> None:
    return a + b


def main():
    print(sum_two(True, True)) # Sample


if __name__ == "__main__":
    main()
