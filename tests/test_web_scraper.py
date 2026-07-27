from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_scrape_public_page_returns_main_body_text(monkeypatch):
    class FakeResponse:
        def __init__(self):
            self.text = "<html><body><header>Header</header><main><article><h1>Sample Title</h1><p>Body text here.</p></article></main><footer>Footer</footer></body></html>"

        def raise_for_status(self):
            return None

    monkeypatch.setattr(main.requests, "get", lambda url, timeout=10: FakeResponse())

    response = client.post("/scrape-webpage", params={"url": "https://example.com"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["url"] == "https://example.com"
    assert payload["title"] == "Sample Title"
    assert "Body text here." in payload["text"]
    assert "Header" not in payload["text"]
    assert "Footer" not in payload["text"]
