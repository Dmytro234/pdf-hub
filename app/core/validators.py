from app.core.config import MAX_FILES_PER_JOB, MAX_UPLOAD_MB


def validate_upload_count(n: int):
    if n > MAX_FILES_PER_JOB:
        raise ValueError(f"Too many files. Max: {MAX_FILES_PER_JOB}")


def validate_upload_size(size_bytes: int):
    if size_bytes > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValueError(f"File too large. Max: {MAX_UPLOAD_MB}MB")


def parse_pages_expr(expr: str) -> list[int]:
    """
    "1,3,5-7" -> [1,3,5,6,7]
    """
    expr = (expr or "").replace(" ", "")
    if not expr:
        raise ValueError("pages expression is empty")

    pages: set[int] = set()
    for part in expr.split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            a_i, b_i = int(a), int(b)
            if a_i <= 0 or b_i <= 0:
                raise ValueError("pages must be >= 1")
            if a_i > b_i:
                a_i, b_i = b_i, a_i
            for p in range(a_i, b_i + 1):
                pages.add(p)
        else:
            p = int(part)
            if p <= 0:
                raise ValueError("pages must be >= 1")
            pages.add(p)
    return sorted(pages)
