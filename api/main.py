#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from curses.ascii import NUL
from flask import Flask, jsonify, request
import requests as r
from api.tools.spool import ThreadPool

app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({"success": True}), 200

@app.route("/api/posts", methods=["GET", "POST"])
def get_posts():
    data = request.form
    
    tags = data["tags"].split(",")
    sortBy = data["sortBy"] if "sortBy" in data.keys() else "id"
    sortOrder = data["sortOrder"] if "sortOrder" in data.keys() else "asc"

    def make_request(url):
        r = session.get(url).json()["posts"]
        results.append(r)
    
    if len(tags) < 1 or tags[0] == "":
        return jsonify({"error": "Tags parameter is required"}), 400
    
    if sortBy not in ["id", "reads", "likes", "popularity", ""]:
        return jsonify({"error": "sortBy parameter is invalid"}), 400
    
    if sortOrder not in ["asc", "desc", ""]:
        return jsonify({"error": "sortBy parameter is invalid"}), 400

    try:
        urls = [f"https://api.hatchways.io/assessment/blog/posts?tag={i}" for i in tags]
        pool = ThreadPool(5)
        results = []
        session = r.session()
        pool.map(make_request, urls)
        pool.wait_completion()

        if sortOrder =='asc':
            results = sorted(results[0], key=lambda x: x[sortBy])
        elif sortOrder == 'desc':
            results = sorted(results[0], key=lambda x: x[sortBy], reverse=True)
        
        return jsonify(results), 200
    except r.ConnectionError:
        return "Connection Error"

if __name__ == '__main__':
    app.run(debug=True)