from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse

from app.core.validators import (
    parse_pages_expr,
    validate_upload_count,
    validate_upload_size,
)
from app.services.pdf_compress import compress_pdf
from app.services.pdf_convert import docx_to_pdf, images_to_pdf, pdf_to_docx
from app.services.pdf_encrypt import decrypt_pdf, encrypt_pdf
from app.services.pdf_merge import merge_pdfs
from app.services.pdf_split import split_by_pages, split_custom, split_range
from app.services.storage import (
    ensure_dirs,
    job_output_dir,
    job_upload_dir,
    new_job_id,
    safe_filename,
)

router = APIRouter(prefix="/api/pdf", tags=["pdf"])


def _save_upload(upl: UploadFile, dest: Path):
    content = upl.file.read()
    validate_upload_size(len(content))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)


@router.post("/merge")
async def api_merge(files: list[UploadFile] = File(...)):
    ensure_dirs()
    validate_upload_count(len(files))
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inputs = []
    for f in files:
        p = udir / safe_filename(f.filename or "file.pdf")
        _save_upload(f, p)
        inputs.append(p)

    out = odir / "merged.pdf"
    merge_pdfs(inputs, out)
    return FileResponse(out, filename="merged.pdf")


@router.post("/split")
async def api_split(
    file: UploadFile = File(...),
    mode: str = Form("range"),  # range|by_pages|custom
    from_page: int = Form(1),
    to_page: int = Form(1),
    pages: str = Form(""),
):
    ensure_dirs()
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inp = udir / safe_filename(file.filename or "input.pdf")
    _save_upload(file, inp)

    if mode == "by_pages":
        out = odir / "split.zip"
        split_by_pages(inp, out)
        return FileResponse(out, filename="split.zip")
    if mode == "custom":
        out = odir / "split.pdf"
        split_custom(inp, out, parse_pages_expr(pages))
        return FileResponse(out, filename="split.pdf")

    out = odir / "split.pdf"
    split_range(inp, out, from_page, to_page)
    return FileResponse(out, filename="split.pdf")


@router.post("/compress")
async def api_compress(file: UploadFile = File(...), level: str = Form("medium")):
    ensure_dirs()
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inp = udir / safe_filename(file.filename or "input.pdf")
    _save_upload(file, inp)

    out = odir / "compressed.pdf"
    compress_pdf(inp, out, level=level)
    return FileResponse(out, filename="compressed.pdf")


@router.post("/convert/docx-to-pdf")
async def api_docx_to_pdf(file: UploadFile = File(...)):
    ensure_dirs()
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inp = udir / safe_filename(file.filename or "input.docx")
    _save_upload(file, inp)

    out = odir / "converted.pdf"
    docx_to_pdf(inp, out)
    return FileResponse(out, filename="converted.pdf")


@router.post("/convert/pdf-to-docx")
async def api_pdf_to_docx(file: UploadFile = File(...)):
    ensure_dirs()
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inp = udir / safe_filename(file.filename or "input.pdf")
    _save_upload(file, inp)

    out = odir / "converted.docx"
    pdf_to_docx(inp, out)
    return FileResponse(out, filename="converted.docx")


@router.post("/convert/images-to-pdf")
async def api_images_to_pdf(files: list[UploadFile] = File(...)):
    ensure_dirs()
    validate_upload_count(len(files))
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    images = []
    for f in files:
        p = udir / safe_filename(f.filename or "image")
        _save_upload(f, p)
        images.append(p)

    out = odir / "images.pdf"
    images_to_pdf(images, out)
    return FileResponse(out, filename="images.pdf")


@router.post("/encrypt")
async def api_encrypt(
    file: UploadFile = File(...),
    user_password: str = Form(...),
    owner_password: str | None = Form(None),
    allow_print: bool = Form(True),
    allow_copy: bool = Form(True),
    allow_edit: bool = Form(True),
    allow_annotate: bool = Form(True),
):
    ensure_dirs()
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inp = udir / safe_filename(file.filename or "input.pdf")
    _save_upload(file, inp)

    out = odir / "protected.pdf"
    encrypt_pdf(
        inp,
        out,
        user_password,
        owner_password,
        allow_print,
        allow_copy,
        allow_edit,
        allow_annotate,
    )
    return FileResponse(out, filename="protected.pdf")


@router.post("/decrypt")
async def api_decrypt(
    file: UploadFile = File(...),
    password: str = Form(...),
):
    ensure_dirs()
    job = new_job_id()
    udir = job_upload_dir(job)
    odir = job_output_dir(job)

    inp = udir / safe_filename(file.filename or "input.pdf")
    _save_upload(file, inp)

    out = odir / "unlocked.pdf"
    decrypt_pdf(inp, out, password)
    return FileResponse(out, filename="unlocked.pdf")
