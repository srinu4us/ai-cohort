# FastAPI Health Check

A minimal FastAPI application exposing a `/health` endpoint plus document extraction endpoints for benefits PDFs and claims-process Word documents.

## Endpoints

- `GET /health` — returns `{ "status": "ok" }`
- `POST /benefits-pdf/extract?pdf_path=/path/to/file.pdf` — extracts text from each PDF page using pdfplumber and returns it as a list of page texts.
- `POST /claims-process-doc/extract?docx_path=/path/to/file.docx` — extracts paragraph text from a Word document using python-docx and returns it as a list of paragraph texts.
- `POST /pdf-pages/convert?pdf_path=/path/to/file.pdf` — converts each PDF page to an image using pdf2image and returns the generated image paths.

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- pdfplumber

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Then open `http://127.0.0.1:8000/health`.
