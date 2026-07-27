from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
PDF_PATH = Path(r"c:\Users\srinu\OneDrive\Desktop\CMS_Sample_Completed_SBC.pdf")


def test_extract_benefits_pdf_returns_text_per_page():
    if not PDF_PATH.exists():
        pytest.skip(f"PDF not found at {PDF_PATH}")

    response = client.post("/benefits-pdf/extract", params={"pdf_path": str(PDF_PATH)})

    assert response.status_code == 200
    payload = response.json()
    assert "pages" in payload
    assert len(payload["pages"]) >= 1
    assert any(page_text.strip() for page_text in payload["pages"])
