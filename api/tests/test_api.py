import requests


def test_ping(client):
    """Verify endpoint for all ping operates correctly"""
    output = client.get("http://localhost:5000/ping")
    assert output.status_code == 200


def test_single_tag(client):
    """Verify endpoint for all endpoint operates correctly with all query strings"""
    output = client.get(
        "http://localhost:5000/posts?tag=history&sortBy=likes&direction=desc"
    ).get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=history&sortBy=likes&direction=desc"
    ).json()

    assert output == expected


def test_mulyi_tag(client):
    """Verify endpoint for all endpoint operates correctly with all query strings"""
    output = client.get(
        "http://localhost:5000/posts?tag=history,tech&sortBy=likes&direction=desc"
    ).get_json()

    expected = requests.get(
        "https://api.hatchways.io/assessment/solution/posts?tags=history,tech&sortBy=likes&direction=desc"
    ).json()

    assert output == expected
