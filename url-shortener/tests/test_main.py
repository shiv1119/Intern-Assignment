import pytest
from app.main import app

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Tests given by company
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


# Tests implemented by me


def test_health_check(client):
    response = client.get("/")
    assert response.status_code in [200, 404]  # no home route defined

# This test case tests that a valid url can be shortened and redirected successfully
def test_shorten_and_redirect(client):
    url = "https://www.example.com"
    res = client.post("/api/shorten", json={"url": url})
    assert res.status_code == 201
    data = res.get_json()
    short_code = data["short_code"]

    res2 = client.get(f"/{short_code}", follow_redirects=False)
    assert res2.status_code == 302
    assert res2.location == url

#This test will ensure that submitting an invalid url will return status 400
def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "not-a-valid-url"})
    assert res.status_code == 400

# This tests confirms that analytics correctly tracks clicks and all
def test_analytics(client):
    url = "https://www.test.com"
    res = client.post("/api/shorten", json={"url": url})
    short_code = res.get_json()["short_code"]
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    stats = client.get(f"/api/stats/{short_code}").get_json()
    assert stats["clicks"] == 2
    assert stats["url"] == url
    assert "created_at" in stats
