#!/usr/bin/env python3
"""
- Create a Cache class. In the __init__.
- Create a store method that takes a data argument and returns a string.
"""

import redis
from typing import Union
import uuid


class Cache:
    """
    This declares the class in redis for caching.
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        - This method takes a data argument and returns a string.
        - It generates a random key (using uuid).
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
