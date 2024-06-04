"""Tien xu ly van ban tieng Viet cho Admission AI.

Nguyen tac: chuan hoa ve dang khong dau, chu thuong de mo hinh TF-IDF khop
duoc ca cau co dau, khong dau va viet tat pho bien cua hoc sinh.
"""
import re
import unicodedata

# Viet tat pho bien trong hoi thoai tuyen sinh (mo rong sau khi chuan hoa khong dau)
ABBR = {
    "dh": "dai hoc",
    "cntt": "cong nghe thong tin",
    "ktx": "ky tuc xa",
    "sv": "sinh vien",
    "hs": "hoc sinh",
    "thpt": "thpt",
    "dgnl": "danh gia nang luc",
    "bn": "bao nhieu",
    "ko": "khong",
    "k": "khong",
    "dc": "duoc",
    "ad": "",          # 'ad' = admin, la tu dem hoi thoai -> bo
    "mn": "",
    "j": "gi",
}

_PUNCT = re.compile(r"[^a-z0-9\s]")


def strip_accents(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize(text: str) -> str:
    """Chuan hoa: thuong -> bo dau -> bo dau cau -> thay viet tat -> gon khoang trang."""
    if not text:
        return ""
    t = strip_accents(str(text).lower())
    t = _PUNCT.sub(" ", t)
    tokens = [ABBR.get(tok, tok) for tok in t.split()]
    return " ".join(tok for tok in tokens if tok)


def tokenize(text: str) -> list:
    return normalize(text).split()
