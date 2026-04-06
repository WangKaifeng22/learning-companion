#!/usr/bin/env python3
"""
MinerU Caller for Study Workspace

Python wrapper around the mineru-open-api CLI.
Designed to be copied into user project directories.

Usage:
    python scripts/mineru_caller.py --file "文献.pdf"
    python scripts/mineru_caller.py --file "文献.pdf" --mode extract --ocr
    python scripts/mineru_caller.py --file "文献.pdf" --output-dir ./output

Requires: mineru-open-api CLI installed globally.
    Install: npm i -g mineru-open-api  OR  uv tool install mineru-open-api
"""

import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def check_mineru_installed():
    if shutil.which("mineru-open-api") is None:
        print("Error: mineru-open-api CLI not found.", file=sys.stderr)
        print("Install with one of:", file=sys.stderr)
        print("  npm i -g mineru-open-api", file=sys.stderr)
        print("  uv tool install mineru-open-api", file=sys.stderr)
        print("  Windows: irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex", file=sys.stderr)
        sys.exit(1)


def check_auth():
    result = subprocess.run(
        ["mineru-open-api", "auth", "--check"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode == 0


def auto_select_mode(file_path: str):
    p = Path(file_path)
    if not p.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    size_mb = p.stat().st_size / (1024 * 1024)

    if size_mb > 10:
        return "extract"

    if p.suffix.lower() == ".pdf":
        try:
            import fitz
            doc = fitz.open(str(p))
            pages = len(doc)
            doc.close()
            if pages > 20:
                return "extract"
        except ImportError:
            pass

    return "flash-extract"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="MinerU document extraction for study workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/mineru_caller.py --file "文献.pdf"
  python scripts/mineru_caller.py --file "文献.pdf" --mode extract --ocr
  python scripts/mineru_caller.py --file "文献.pdf" --output-dir ./output --language en
        """,
    )

    parser.add_argument("--file", required=True, help="Path to document (PDF, image, DOCX, etc.)")
    parser.add_argument(
        "--mode",
        choices=["flash-extract", "extract", "auto"],
        default="auto",
        help="Extraction mode (default: auto-select based on file size/pages)",
    )
    parser.add_argument("--output-dir", "-o", help="Output directory (default: stdout)")
    parser.add_argument("--ocr", action="store_true", help="Force OCR for scanned documents (extract mode only)")
    parser.add_argument("--language", default="ch", help="Language code (default: ch for Chinese+English)")
    parser.add_argument("--timeout", type=int, default=300, help="Request timeout in seconds (default: 300)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show HTTP request/response details")

    args = parser.parse_args()

    check_mineru_installed()

    mode = args.mode
    if mode == "auto":
        mode = auto_select_mode(args.file)
        print(f"Auto-selected mode: {mode}", file=sys.stderr)

    if mode == "extract":
        if not check_auth():
            print("Error: extract mode requires authentication.", file=sys.stderr)
            print("Run: mineru-open-api auth", file=sys.stderr)
            sys.exit(3)

    cmd = ["mineru-open-api", mode, args.file]

    if args.output_dir:
        cmd.extend(["-o", args.output_dir])

    if args.ocr and mode == "extract":
        cmd.append("--ocr")

    cmd.extend(["--language", args.language])
    cmd.extend(["--timeout", str(args.timeout)])

    if args.verbose:
        cmd.append("-v")

    print(f"Running: {' '.join(cmd)}", file=sys.stderr)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout + 30)
    except subprocess.TimeoutExpired:
        print(f"Error: Extraction timed out after {args.timeout + 30}s.", file=sys.stderr)
        sys.exit(4)

    if result.returncode != 0:
        print(f"Error: mineru-open-api exited with code {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        sys.exit(result.returncode)

    if args.output_dir:
        print(f"Output saved to: {args.output_dir}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    else:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
