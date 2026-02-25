import subprocess
from pathlib import Path

import img2pdf


def docx_to_pdf(input_docx: Path, output_pdf: Path):
    outdir = output_pdf.parent
    outdir.mkdir(parents=True, exist_ok=True)

    # LibreOffice створить pdf з тією ж назвою в outdir
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(outdir),
        str(input_docx),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"LibreOffice failed: {r.stderr.strip()}")

    produced = outdir / (input_docx.stem + ".pdf")
    if not produced.exists():
        raise RuntimeError("LibreOffice did not produce PDF")

    produced.replace(output_pdf)


def pdf_to_docx(input_pdf: Path, output_docx: Path):
    outdir = output_docx.parent
    outdir.mkdir(parents=True, exist_ok=True)

    # LibreOffice: pdf -> docx (best effort)
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "docx",
        "--outdir",
        str(outdir),
        str(input_pdf),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"LibreOffice failed: {r.stderr.strip()}")

    produced = outdir / (input_pdf.stem + ".docx")
    if not produced.exists():
        raise RuntimeError("LibreOffice did not produce DOCX")

    produced.replace(output_docx)


def images_to_pdf(images: list[Path], output_pdf: Path):
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert([str(p) for p in images]))
