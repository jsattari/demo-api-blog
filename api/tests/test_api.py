import requests


def test_ping(client):
    """Verify endpoint for is operating"""
    output = client.get("http://localhost:5000/ping")
    assert output.status_code == 200


def test_single_tag_sorted(client):
    """Verify single tag with sorting"""
    output = client.get(
        "http://localhost:5000/posts?tag=history&sortBy=likes&direction=desc"
    ).get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=history&sortBy=likes&direction=desc"
    ).json()

    assert output == expected


def test_multi_tag_sorted(client):
    """Verify multi tag with sorting"""
    output = client.get(
        "http://localhost:5000/posts?tag=history,tech&sortBy=likes&direction=desc"
    ).get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=history,tech&sortBy=likes&direction=desc"
    ).json()

    assert output == expected


def test_multi_tag2_sorted(client):
    """Verify multi tag with sorting"""
    output = client.get(
        "http://localhost:5000/posts?tag=politics,art&sortBy=likes&direction=desc"
    ).get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=politics,art&sortBy=likes&direction=desc"
    ).json()

    assert output == expected


def test_single_tag(client):
    """Verify single tag with sorting"""
    output = client.get("http://localhost:5000/posts?tag=history").get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=history"
    ).json()

    assert output == expected


def test_multi_tag(client):
    """Verify multi tag with sorting"""
    output = client.get("http://localhost:5000/posts?tag=history,tech").get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=history,tech"
    ).json()

    assert output == expected
