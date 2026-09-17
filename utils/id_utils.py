"""Local demo account store; userInfo.csv stays outside Git."""
import csv
import hashlib
import hmac
import os
from pathlib import Path

_ACCOUNT_FILE = Path(__file__).resolve().parents[1] / "userInfo.csv"
_ITERATIONS = 200_000


def sava_id_info(user, pwd):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", pwd.encode("utf-8"), salt, _ITERATIONS)
    record = f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"
    with _ACCOUNT_FILE.open("a", encoding="utf-8", newline="") as fp:
        csv.writer(fp).writerow([user, record])


def get_id_info():
    if not _ACCOUNT_FILE.exists():
        return {}
    with _ACCOUNT_FILE.open("r", encoding="utf-8", newline="") as fp:
        return {row[0]: row[1] for row in csv.reader(fp) if len(row) >= 2}


def verify_password(password, record):
    try:
        algorithm, rounds, salt, expected = record.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), int(rounds)
        )
        return hmac.compare_digest(digest, bytes.fromhex(expected))
    except (ValueError, TypeError):
        return False
