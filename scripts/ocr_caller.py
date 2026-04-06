#!/usr/bin/env python3
"""
PaddleOCR Caller for Study Workspace

Standalone wrapper for PaddleOCR text extraction.
Designed to be copied into user project directories.

Usage:
    python scripts/ocr_caller.py --file-path "文献.pdf" --pretty
    python scripts/ocr_caller.py --file-url "https://example.com/doc.pdf" --pretty

Environment variables:
    PADDLEOCR_OCR_API_URL   - API endpoint
    PADDLEOCR_ACCESS_TOKEN  - Access token
    PADDLEOCR_OCR_TIMEOUT   - Request timeout in seconds (optional, default: 30)
"""

import base64
import io
import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import fitz
except ImportError:
    fitz = None


def check_env():
    api_url = os.environ.get("PADDLEOCR_OCR_API_URL")
    token = os.environ.get("PADDLEOCR_ACCESS_TOKEN")
    timeout = int(os.environ.get("PADDLEOCR_OCR_TIMEOUT", "30"))

    if not api_url:
        print("Error: PADDLEOCR_OCR_API_URL not configured.", file=sys.stderr)
        sys.exit(2)
    if not token:
        print("Error: PADDLEOCR_ACCESS_TOKEN not configured.", file=sys.stderr)
        sys.exit(2)

    return api_url, token, timeout


def pdf_to_images(pdf_path: str, dpi: int = 150):
    if fitz is None:
        print("Error: 'PyMuPDF' (fitz) is required for PDF-to-image conversion. Install with: pip install PyMuPDF", file=sys.stderr)
        sys.exit(3)

    doc = fitz.open(pdf_path)
    images = []
    for i in range(len(doc)):
        page = doc[i]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        images.append((f"page_{i+1}", img_bytes))
    doc.close()
    return images


def ocr_image(api_url: str, token: str, timeout: int, image_bytes: bytes, file_type: int = 1):
    file_data = base64.b64encode(image_bytes).decode("ascii")

    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "file": file_data,
        "fileType": file_type,
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False,
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout}s. Try increasing PADDLEOCR_OCR_TIMEOUT.", file=sys.stderr)
        return {"ok": False, "text": "", "error": {"message": f"Timeout after {timeout}s"}, "result": None}
    except requests.exceptions.RequestException as e:
        print(f"Error: Network error: {e}", file=sys.stderr)
        return {"ok": False, "text": "", "error": {"message": str(e)}, "result": None}

    if response.status_code == 200:
        try:
            data = response.json()
            result = data.get("result", {})
            texts = []
            for res in result.get("layoutParsingResults", []):
                texts.append(res.get("markdown", {}).get("text", ""))
            full_text = "\n\n".join(t for t in texts if t)
            return {"ok": True, "text": full_text, "error": None, "result": result}
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error: Failed to parse response: {e}", file=sys.stderr)
            return {"ok": False, "text": "", "error": {"message": f"Parse error: {e}"}, "result": None}
    elif response.status_code == 403:
        print("Error: Authentication failed (403). Check your PADDLEOCR_ACCESS_TOKEN.", file=sys.stderr)
        return {"ok": False, "text": "", "error": {"message": "Authentication failed (403)"}, "result": None}
    elif response.status_code == 429:
        print("Error: API rate limit exceeded (429). Daily quota exhausted.", file=sys.stderr)
        return {"ok": False, "text": "", "error": {"message": "Rate limit exceeded (429)"}, "result": None}
    else:
        print(f"Error: API returned status {response.status_code}: {response.text[:500]}", file=sys.stderr)
        return {"ok": False, "text": "", "error": {"message": f"HTTP {response.status_code}: {response.text[:500]}"}, "result": None}


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="PaddleOCR text extraction for study workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/ocr_caller.py --file-path "文献.pdf" --pretty
  python scripts/ocr_caller.py --file-url "https://example.com/doc.pdf" --pretty
  python scripts/ocr_caller.py --file-path "image.png" --output result.json
        """,
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file-url", help="URL to image or PDF")
    input_group.add_argument("--file-path", help="Local path to image or PDF")

    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--output", "-o", metavar="FILE", help="Save result to JSON file")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for PDF-to-image conversion (default: 150)")

    args = parser.parse_args()

    api_url, token, timeout = check_env()

    file_path = Path(args.file_path) if args.file_path else None
    is_pdf = file_path and file_path.suffix.lower() == ".pdf" if file_path else False

    if args.file_url and args.file_url.lower().endswith(".pdf"):
        is_pdf = True

    if is_pdf and args.file_path:
        if fitz is None:
            print("Error: PDF processing requires PyMuPDF. Install with: pip install PyMuPDF", file=sys.stderr)
            sys.exit(3)
        images = pdf_to_images(str(file_path), dpi=args.dpi)
        print(f"Processing {len(images)} pages from PDF...", file=sys.stderr)

        all_texts = []
        for page_name, img_bytes in images:
            print(f"  OCR: {page_name}...", file=sys.stderr)
            result = ocr_image(api_url, token, timeout, img_bytes)
            if result["ok"]:
                all_texts.append(f"--- {page_name} ---\n{result['text']}")
            else:
                all_texts.append(f"--- {page_name} ---\n[OCR failed: {result.get('error', {}).get('message', 'unknown')}]")

        combined = {"ok": True, "text": "\n\n".join(all_texts), "error": None, "result": {"pages": len(images)}}
    elif args.file_url:
        print(f"Fetching from URL: {args.file_url}", file=sys.stderr)
        try:
            resp = requests.get(args.file_url, timeout=timeout)
            resp.raise_for_status()
            img_bytes = resp.content
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch URL: {e}", file=sys.stderr)
            sys.exit(4)
        result = ocr_image(api_url, token, timeout, img_bytes)
        combined = result
    else:
        img_bytes = file_path.read_bytes()
        result = ocr_image(api_url, token, timeout, img_bytes)
        combined = result

    indent = 2 if args.pretty else None
    json_output = json.dumps(combined, indent=indent, ensure_ascii=False)

    if args.stdout:
        print(json_output)
    elif args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json_output, encoding="utf-8")
        print(f"Result saved to: {out_path}", file=sys.stderr)
    else:
        print(combined["text"])

    sys.exit(0 if combined["ok"] else 1)


if __name__ == "__main__":
    main()
