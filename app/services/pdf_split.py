from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from pypdf import PdfReader, PdfWriter


def split_by_pages(input_pdf: Path, output_zip: Path):
    reader = PdfReader(str(input_pdf))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDF")
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output_zip, "w", ZIP_DEFLATED) as z:
        for i, page in enumerate(reader.pages, start=1):
            w = PdfWriter()
            w.add_page(page)
            name = f"page_{i:03d}.pdf"
            tmp = output_zip.parent / name
            with open(tmp, "wb") as f:
                w.write(f)
            z.write(tmp, arcname=name)
            tmp.unlink(missing_ok=True)


def split_range(input_pdf: Path, output_pdf: Path, from_page: int, to_page: int):
    reader = PdfReader(str(input_pdf))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDF")
    n = len(reader.pages)
    if from_page < 1 or to_page < 1 or from_page > n or to_page > n:
        raise ValueError("Page out of range")
    if from_page > to_page:
        from_page, to_page = to_page, from_page

    w = PdfWriter()
    for i in range(from_page - 1, to_page):
        w.add_page(reader.pages[i])

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as f:
        w.write(f)


def split_custom(input_pdf: Path, output_pdf: Path, pages: list[int]):
    reader = PdfReader(str(input_pdf))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDF")
    n = len(reader.pages)
    for p in pages:
        if p < 1 or p > n:
            raise ValueError(f"Page {p} out of range")

    w = PdfWriter()
    for p in pages:
        w.add_page(reader.pages[p - 1])

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as f:
        w.write(f)
