#!/usr/bin/env python3
"""
- Create a Cache class.
- Create a store method that takes a data argument and returns a string.
"""

import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator to count the number of times a method is called.
    param method: The method to decorate.
          return
    """
    key = method.__qualname__
    """creates a unique key"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):

        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs and outputs for a function.
    """
    # Construct keys for inputs and outputs based on the method's qualified name
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def history_wrapper(self, *args, **kwargs):
        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))

        return result
    return history_wrapper

def replay(fn: Callable):
    """
    Display the history of calls of a particular function.
    This function connects to Redis, retrieves the history of inputs and outputs for the given function,
    and prints them out in a readable format.
    """
    try:
        redis = redis.Redis()
        
        f_name = fn.__qualname__
        
        num_calls = redis.get(f_name)
        num_calls = int(num_calls.decode('utf-8')) if num_calls else 0
        print(f'{f_name} was called {num_calls} times:')

        inputs = redis.lrange(f_name + ":inputs", 0, -1)
        outputs = redis.lrange(f_name + ":outputs", 0, -1)

        for in_key, out_key in zip(inputs, outputs):

            in_key = in_key.decode('utf-8')
            out_key = out_key.decode('utf-8')
            print(f'{f_name}(*{in_key}) -> {out_key}')
    except Exception as e:
        print(f'An error occurred while processing {f_name}: {e}')


class Cache:
    """
    This declares the class in redis for caching.
    """
    def __init__(self):
        """constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb
        self.count_calls = {}

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        - This method takes a data argument and returns a string.
        - It generates a random key (using uuid).

            param: data -> The data to be strored in redis.
                   return -> A string representing the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes], Union[str, bytes, int, float]]] =
            None) -> Union[str, bytes, int, float]:
        """
        - method that take a key str and an optional Callable(fn).

        - params:
          key -> The key of the data to retrieve.
          fn: -> An optional callable to convert the retrieved data.
          return -> The retrieved data.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Method that will automatically parametrize Cache.get
        with the correct conversion function for strings
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> Optional[int]:
        """
        Method that will automatically parametrize Cache.get
        with the correct conversion function for integers
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value

if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
    print("All tests passed successfully.")

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    replay(cache.store)