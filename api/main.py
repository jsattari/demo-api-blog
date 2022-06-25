#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from curses.ascii import NUL
from flask import Flask, jsonify, request
import requests
from api.tools.spool import *

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"success": True}), 200


@app.route("/posts", methods=["GET", "POST"])
def get_posts():

    data = request.args

    tags = data.get("tag").split(",")
    sortBy = data.get("sortBy")
    sortOrder = data.get("direction")

    def multi_threader(tag_list: list, pool_size: int, function):
        results = []
        urls = [
            f"https://api.hatchways.io/assessment/blog/posts?tag={tag}"
            for tag in tag_list
        ]
        pool = ThreadPool(pool_size)
        pool.map(function, urls)
        pool.wait_completion()
        return results

    def make_request(url: str):
        session = requests.session()
        request_results = session.get(url).json()["posts"]
        return api_results.append(request_results)

    def json_sort(json_array, sort_value, sort_direction):
        return (
            sorted(json_array[0], key=lambda x: x[sort_value], reverse=True)
            if sort_direction == "desc"
            else sorted(json_array[0], key=lambda x: x[sort_value])
        )

    try:
        api_results = []

        multi_threader(tags, 3, make_request)

        api_results = json_sort(api_results, sortBy, sortOrder)

        return jsonify({"posts": api_results}), 200
    except requests.ConnectionError:
        return "Connection Error"


if __name__ == "__main__":
    app.run(debug=True)
