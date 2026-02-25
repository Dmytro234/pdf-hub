import subprocess
from pathlib import Path

_LEVEL_MAP = {
    "light": "/prepress",
    "medium": "/ebook",
    "strong": "/screen",
}


def compress_pdf(input_pdf: Path, output_pdf: Path, level: str = "medium"):
    profile = _LEVEL_MAP.get(level, "/ebook")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={profile}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={str(output_pdf)}",
        str(input_pdf),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Ghostscript failed: {r.stderr.strip()}")
