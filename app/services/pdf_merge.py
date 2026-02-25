from pathlib import Path

from pypdf import PdfReader, PdfWriter


def merge_pdfs(inputs: list[Path], output: Path):
    writer = PdfWriter()
    for f in inputs:
        reader = PdfReader(str(f))
        if reader.is_encrypted:
            raise ValueError(f"Encrypted PDF: {f.name}")
        for page in reader.pages:
            writer.add_page(page)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "wb") as out:
        writer.write(out)
