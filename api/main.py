#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from curses.ascii import NUL
from glob import glob
import json
from urllib.parse import _NetlocResultMixinStr
from flask import Flask, jsonify, request
import requests
from threading import Thread, Lock

app = Flask(__name__)

lock = Lock()


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"success": True}), 200


@app.route("/posts", methods=["GET", "POST"])
def get_posts():

    data = request.args

    tags = [
        f"https://api.hatchways.io/assessment/blog/posts?tag={tag}"
        for tag in data.get("tag").split(",")
    ]
    sortBy = data.get("sortBy")
    sortOrder = data.get("direction")

    def make_request(url: str):
        session = requests.session()
        request_results = session.get(url).json()["posts"]
        return request_results

    def process1(input_array, tags_array: list, thread_lock):
        for url in tags[: len(tags_array) // 2]:
            thread_lock.acquire()
            req_results = make_request(url)
            input_array.extend(req_results)
            thread_lock.release()

    def process2(input_array, tags_array: list, thread_lock):
        for url in tags[len(tags_array) // 2 :]:
            thread_lock.acquire()
            req_results = make_request(url)
            input_array.extend(req_results)
            thread_lock.release()

    def get_uniques(array):
        return [
            _value
            for _key, _value in enumerate(array)
            if _value not in array[_key + 1 :]
        ]

    def sort_array(array, sort_value, sort_direction):
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

    try:
        api_results = []

        thread1 = Thread(target=process1(api_results, tags, lock), args=())
        thread2 = Thread(target=process2(api_results, tags, lock), args=())

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        api_results = sort_array(get_uniques(api_results), sortBy, sortOrder)

        return jsonify({"posts": api_results}), 200
    except Exception as e:
        return e, api_results, 400


if __name__ == "__main__":
    app.run(debug=True)
