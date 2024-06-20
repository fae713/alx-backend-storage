#!/usr/bin/env python3
""" Module for Implementing an expiring web cache and tracker """

from functools import wraps
import redis
import requests
from typing import Callable

redis = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    This decorator counts the number of times a request has been made.
    """

    @wraps(method)
    def count_req_wrapper(url):
        """ Wrapper for decorator functionality """
        redis.incr(f"count:{url}, 0")
        cached_result = redis.get(f"cached:{url}")
        if cached_result:
            return cached_result.decode('utf-8')

        cached_result = method(url)
        redis.setex(f"cached_result:{url}", 10, cached_result)
        return cached_result

    return count_req_wrapper


@count_requests
def get_page(url: str) -> str:
    """
    This function uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    return requests.get(url).text
