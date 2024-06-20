#!/usr/bin/env python3
"""
- Create a Cache class.
- Create a store method that takes a data argument and returns a string.
"""

import redis
from typing import Union, Callable, Optional
import uuid


class Cache:
    """
    This declares the class in redis for caching.
    """
    def __init__(self):
        """constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb

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
            fn: Optional[Callable] = None) -> Union[str, int, float, bytes]:
        """
        - method that take a key str and an optional Callable(fn).

        - params:
          key -> The key of the data to retrieve.
          fn: -> An optional callable to convert the retrieved data.
          return -> The retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            try:
                if fn is not None:
                    return fn(data)
                else:
                    return data
            except Exception as e:
                print(f"Error converting data: {e}")
                return None
        else:
            return None

    def get_str(self, key: str) -> str:
        """
        This is a method that will automatically parametrize Cache.get
        with the correct conversion function.
        """
        return self.get(key, lambda b: b.decode("utf-8"))

    def get_int(self, key: int) -> int:
        """
        This is a method that will automatically parametrize Cache.get
        with the correct conversion function.
        """
        return self.get(key, int)


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
