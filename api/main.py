#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import requests
from threading import Thread, Lock
from api.tools.spool import *

app = Flask(__name__)

# lock for threads
lock = Lock()

# ping route, only returns success or fail
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"success": True}), 200


# posts route, gets data for api request
@app.route("/posts", methods=["GET", "POST"])
def get_posts():

    """
    Accepts query string params to make a request from blog post
    API endpoints. Creates multiple threads to make multiple API
    requests as fast as possible. Includes sorting where applicable.
    """

    # get query strings params from url
    data = request.args

    # create variables for holding params
    tags = [
        f"https://api.hatchways.io/assessment/blog/posts?tag={tag}"
        for tag in data.get("tag").split(",")
    ]
    sortBy = data.get("sortBy")
    sortOrder = data.get("direction")

    try:

        # list to hold api results
        api_results = []

        # list to hold threads
        threads = []

        # enumerate through tags, create thread for each tag and add to api_results
        for key, value in enumerate(tags):
            threads.append(Worker(key, make_request, value, api_results))

        # join each thread in threads, this allows all threads to finish
        for thread in threads:
            thread.join()

        # sort and de-duplicate api_results list
        api_results = sort_array(get_uniques(api_results), sortBy, sortOrder)

        return jsonify({"posts": api_results}), 200
    except Exception as e:
        return e, api_results, 400


if __name__ == "__main__":
    app.run(debug=True)
