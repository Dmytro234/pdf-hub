import os
import uuid
from pathlib import Path

from app.core.config import OUTPUT_DIR, UPLOAD_DIR


def ensure_dirs():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def new_job_id() -> str:
    return uuid.uuid4().hex


def job_upload_dir(job_id: str) -> Path:
    d = UPLOAD_DIR / job_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def job_output_dir(job_id: str) -> Path:
    d = OUTPUT_DIR / job_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def safe_filename(name: str) -> str:
    # мінімальна санітизація
    name = os.path.basename(name).replace("..", ".")
    return "".join(c for c in name if c.isalnum() or c in "._- ").strip() or "file"
