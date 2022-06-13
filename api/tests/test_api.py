def test_ping(client):
    """Verify endpoint for all ping operates correctly"""
    output = client.get("/ping")
    assert output.status_code == 200

def test_endpoint(client):
    """Verify endpoint for all endpoint operates correctly with all query strings"""
    output = client.get("/api/posts?tags=history,tech&sortBy=likes&sortOrder=desc")
    assert output.status_code == 200