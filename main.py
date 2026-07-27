import tempfile
from pathlib import Path

import pdfplumber
import pytesseract
import requests
from bs4 import BeautifulSoup
from docx import Document
from fastapi import FastAPI, HTTPException
from pdf2image import convert_from_path
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _get_poppler_path() -> str | None:
    candidates = [
        Path(r"C:\Users\srinu\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"),
        Path(r"C:\Program Files\Poppler\Library\bin"),
        Path(r"C:\Program Files\poppler\bin"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None

app = FastAPI()


def _get_raw_text_dir() -> Path:
    raw_text_dir = Path.cwd() / "raw_text"
    raw_text_dir.mkdir(exist_ok=True)
    return raw_text_dir


def _clean_text(text: str) -> str:
    return "\n".join(line.strip() for line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines() if line.strip())


def _save_text_file(filename: str, text: str) -> Path:
    output_path = _get_raw_text_dir() / filename
    output_path.write_text(_clean_text(text), encoding="utf-8")
    return output_path


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/benefits-pdf/extract")
def extract_benefits_pdf(pdf_path: str):
    path = Path(pdf_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"PDF not found: {pdf_path}")

    try:
        with pdfplumber.open(path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
    except Exception as exc:  # pragma: no cover - defensive error path
        raise HTTPException(status_code=400, detail=f"Unable to read PDF: {exc}") from exc

    combined_text = "\n\n".join(pages)
    _save_text_file("benefits.txt", combined_text)

    return {"pdf_path": str(path), "pages": pages, "page_count": len(pages)}


@app.post("/claims-process-doc/extract")
def extract_claims_process_doc(docx_path: str):
    path = Path(docx_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"DOCX not found: {docx_path}")

    try:
        document = Document(path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
    except Exception as exc:  # pragma: no cover - defensive error path
        raise HTTPException(status_code=400, detail=f"Unable to read DOCX: {exc}") from exc

    combined_text = "\n".join(paragraphs)
    _save_text_file("claims_process.txt", combined_text)

    return {"docx_path": str(path), "paragraphs": paragraphs, "paragraph_count": len(paragraphs)}


def extract_text_from_images(image_paths):
    full_text = []

    for i, image_path in enumerate(image_paths):
        if isinstance(image_path, Image.Image):
            img = image_path
        else:
            img = Image.open(image_path)

        text = pytesseract.image_to_string(img)

        if text.strip():
            full_text.append(f"--- Page {i + 1} ---\n{text}")

    return "\n\n".join(full_text)


@app.post("/scrape-webpage")
def scrape_webpage(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=400, detail=f"Unable to fetch URL: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "img"]):
        tag.decompose()

    candidates = []
    for selector in ["article", "main", "[role='main']", "body"]:
        candidates.extend(soup.select(selector))

    content_node = None
    for node in candidates:
        if node.name in {"article", "main", "body"}:
            content_node = node
            break

    if content_node is None:
        content_node = soup.body or soup

    for tag in content_node(["nav", "header", "footer", "aside", "form", "button"]):
        tag.decompose()

    title = ""
    if soup.title and soup.title.get_text(strip=True):
        title = soup.title.get_text(strip=True)
    elif content_node.find(["h1", "h2"]):
        title = content_node.find(["h1", "h2"]).get_text(" ", strip=True)

    text_blocks = []
    for paragraph in content_node.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        text = " ".join(paragraph.get_text(" ", strip=True).split())
        if text:
            text_blocks.append(text)

    cleaned_text = "\n".join(text_blocks)
    _save_text_file("enrollment.txt", cleaned_text)

    return {"url": url, "title": title, "text": cleaned_text}


@app.post("/pdf-pages/convert")
def convert_pdf_pages(pdf_path: str):
    path = Path(pdf_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"PDF not found: {pdf_path}")

    try:
        output_root = Path.cwd() / "tmp"
        output_root.mkdir(exist_ok=True)
        output_dir = Path(tempfile.mkdtemp(prefix="pdf2image-", dir=str(output_root)))
        try:
            poppler_path = _get_poppler_path()
            images = convert_from_path(path, output_folder=str(output_dir), poppler_path=poppler_path)
            image_paths = [str(image_path) for image_path in images]
            extracted_text = extract_text_from_images(images)
            return {
                "pdf_path": str(path),
                "images": image_paths,
                "image_count": len(image_paths),
                "extracted_text": extracted_text,
            }
        finally:
            if output_dir.exists():
                for file_path in output_dir.glob("*"):
                    try:
                        file_path.unlink()
                    except OSError:
                        pass
                try:
                    output_dir.rmdir()
                except OSError:
                    pass
    except Exception as exc:  # pragma: no cover - defensive error path
        raise HTTPException(status_code=400, detail=f"Unable to convert PDF pages: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)