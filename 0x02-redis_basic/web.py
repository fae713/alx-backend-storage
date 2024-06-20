#!/usr/bin/env python3
""" Module for Implementing an expiring web cache and tracker """

from functools import wraps
import redis
import requests
from typing import Callable

r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    This decorator counts the number of times a request has been made.
    """

    @wraps(method)
    def count_req_wrapper(url):
        """ Wrapper for decorator functionality """
        r.incr(f"count:{url}")
        cached_html = r.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return count_req_wrapper


@count_requests
def get_page(url: str) -> str:
    """
    This function uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    request = requests.get(url)
    return request.text
