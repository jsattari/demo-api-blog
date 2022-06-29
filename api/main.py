#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from threading import Lock
from api.tools.tools import *
from api.tools.spool import *

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

    try:
        api_results = []

        """ for url in tags:
            thread = Thread(
                target=threadify(api_results, url, lock, make_request), args=()
            )
            thread.start() """

        pool = ThreadPool(5)
        pool.map(threadify(api_results, tags, lock, make_request), tags)
        pool.wait_completion()

        api_results = sort_array(get_uniques(api_results), sortBy, sortOrder)

        return jsonify({"posts": api_results}), 200
    except Exception as e:
        return e, api_results, 400


if __name__ == "__main__":
    app.run(debug=True)
