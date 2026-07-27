from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

import main

client = TestClient(main.app)


def test_extract_text_from_images_joins_page_text(tmp_path, monkeypatch):
    image_path = tmp_path / "page1.png"
    Image.new("RGB", (10, 10), color="white").save(image_path)

    calls = []

    def fake_image_to_string(image):
        calls.append(image)
        return "Sample OCR text"

    monkeypatch.setattr(main.pytesseract, "image_to_string", fake_image_to_string)

    result = main.extract_text_from_images([str(image_path)])

    assert result == "--- Page 1 ---\nSample OCR text"
    assert len(calls) == 1
    assert isinstance(calls[0], Image.Image)


def test_convert_pdf_pages_returns_image_paths(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(
        b"%PDF-1.4\n1 0 obj<< /Type /Catalog /Pages 2 0 R>>endobj\n"
        b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1>>endobj\n"
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n"
        b"4 0 obj<< /Length 44 >>stream\nBT /F1 18 Tf 72 72 Td (Hello PDF) Tj ET\nendstream\nendobj\n"
        b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\nxref\n0 6\n0000000000 65535 f \n"
        b"0000000010 00000 n \n0000000062 00000 n \n0000000119 00000 n \n0000000207 00000 n \n0000000305 00000 n \ntrailer<< /Size 6 /Root 1 0 R>>\nstartxref\n0\n%%EOF\n"
    )

    response = client.post("/pdf-pages/convert", params={"pdf_path": str(pdf_path)})

    assert response.status_code == 200
    payload = response.json()
    assert payload["pdf_path"] == str(pdf_path)
    assert payload["image_count"] >= 0
    assert isinstance(payload["images"], list)
