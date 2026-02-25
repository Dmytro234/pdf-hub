import subprocess
from pathlib import Path


def encrypt_pdf(
    input_pdf: Path,
    output_pdf: Path,
    user_password: str,
    owner_password: str | None = None,
    allow_print: bool = True,
    allow_copy: bool = True,
    allow_edit: bool = True,
    allow_annotate: bool = True,
):
    if not owner_password:
        owner_password = user_password + "_owner"

    print_level = "full" if allow_print else "none"
    modify_level = "all" if allow_edit else "none"
    extract_flag = "y" if allow_copy else "n"
    annotate_flag = "y" if allow_annotate else "n"

    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "qpdf",
        "--encrypt",
        user_password,
        owner_password,
        "256",
        f"--print={print_level}",
        f"--modify={modify_level}",
        f"--extract={extract_flag}",
        f"--annotate={annotate_flag}",
        "--",
        str(input_pdf),
        str(output_pdf),
    ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"qpdf encrypt failed: {r.stderr.strip()}")


def decrypt_pdf(input_pdf: Path, output_pdf: Path, password: str):
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "qpdf",
        f"--password={password}",
        "--decrypt",
        str(input_pdf),
        str(output_pdf),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"qpdf decrypt failed: {r.stderr.strip()}")
