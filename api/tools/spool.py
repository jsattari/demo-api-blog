#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread, Lock
import requests

# create thread lock to avoid race condition
lock = Lock()


class Worker(Thread):
    """
    OOP style threading with additional parameters included
        {
            thread_id: unique thread identifier,
            func: function to apply within thread,
            url: url of api to access,
            result: list where results should be appended
        }
    """

    def __init__(self, thread_id, func, url: str, result: list):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.func = func
        self.url = url
        self.result = result
        self.daemon = True
        self.start()

    def run(self):
        """
        Thread run executable. Acquires lock then executes
        function on input, then extends result list with the output
        """
        lock.acquire()
        output = self.func(self.url)
        self.result.extend(output)
        lock.release()


def make_request(url: str):
    """
    Function that makes a request on a given url,
    it then accesses the response
    """
    session = requests.session()
    request_results = session.get(url).json()["posts"]
    return request_results


def get_uniques(array):
    """
    Deduplicates array of dictionaries
    """
    return [
        _value for _key, _value in enumerate(array) if _value not in array[_key + 1 :]
    ]


def sort_array(array, sort_value, sort_direction):
    """
    Sorts an array of dictionaries by a given value and direciton
    """
    if sort_value is None:
        return sorted(
            array,
            key=lambda x: x["id"],
            reverse=True if sort_direction == "desc" else False,
        )

    elif sort_value in ["id", "reads", "likes", "popularity"]:
        return sorted(
            array,
            key=lambda x: x[sort_value],
            reverse=True if sort_direction == "desc" else False,
        )

    else:
        return {"error": "sortBy parameter is invalid"}
