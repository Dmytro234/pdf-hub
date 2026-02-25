from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
TMP_DIR = BASE_DIR / "tmp"
UPLOAD_DIR = TMP_DIR / "uploads"
OUTPUT_DIR = TMP_DIR / "outputs"

MAX_UPLOAD_MB = 50
MAX_FILES_PER_JOB = 20
