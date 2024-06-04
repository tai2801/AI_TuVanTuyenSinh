"""Trich xuat entity: nganh hoc (tu dien + fuzzy), to hop mon, nam."""
import difflib
import re

from .preprocess import normalize

# Ten goi tat / cach goi khac cua tung nganh (theo ma nganh trong majors.json)
ALIASES = {
    "CNTT": ["cong nghe thong tin", "cntt", "it", "cong nghe thong tin ung dung"],
    "KHMT": ["khoa hoc may tinh", "khmt", "computer science"],
    "TTNT": ["tri tue nhan tao", "ttnt", "ai", "hoc may"],
    "ATTT": ["an toan thong tin", "attt", "an ninh mang", "bao mat"],
    "QTKD": ["quan tri kinh doanh", "qtkd", "quan tri", "kinh doanh"],
    "MKT": ["marketing", "mkt", "truyen thong marketing"],
    "KETO": ["ke toan", "keto", "kiem toan"],
    "TCNH": ["tai chinh ngan hang", "tcnh", "tai chinh", "ngan hang"],
    "NNA": ["ngon ngu anh", "nna", "tieng anh"],
    "TKDH": ["thiet ke do hoa", "tkdh", "do hoa", "thiet ke"],
    "DTVT": ["dien tu vien thong", "dtvt", "ky thuat dien tu vien thong", "dien tu"],
    "LOG": ["logistics", "log", "chuoi cung ung", "quan ly chuoi cung ung"],
}

_COMBO_RE = re.compile(r"\b([abcdhv])\s?(\d{2})\b")
_YEAR_RE = re.compile(r"\b(20\d{2})\b")


def _norm_major_names(kb):
    table = {}
    for m in kb.majors:
        table[normalize(m["name"])] = m["code"]
        for a in ALIASES.get(m["code"], []):
            table[normalize(a)] = m["code"]
    return table


def extract_majors(text, kb, limit=2):
    """Tim nganh trong cau: khop chinh xac truoc, fuzzy (catoff 0.82) sau."""
    t = " " + normalize(text) + " "
    table = _norm_major_names(kb)
    found = []
    # Khop dai truoc (tranh 'tai chinh' an mat 'tai chinh ngan hang'...)
    for name in sorted(table, key=len, reverse=True):
        if f" {name} " in t and table[name] not in found:
            found.append(table[name])
            if len(found) >= limit:
                return found
    if found:
        return found
    # Fuzzy tren tung cum 2-4 tu
    words = t.split()
    names = list(table.keys())
    for n in (4, 3, 2):
        for i in range(len(words) - n + 1):
            chunk = " ".join(words[i:i + n])
            close = difflib.get_close_matches(chunk, names, n=1, cutoff=0.86)
            if close and table[close[0]] not in found:
                found.append(table[close[0]])
                if len(found) >= limit:
                    return found
    return found


def extract_combo(text):
    m = _COMBO_RE.search(normalize(text))
    return m.group(1).upper() + m.group(2) if m else None


def extract_year(text):
    m = _YEAR_RE.search(text or "")
    return int(m.group(1)) if m else None
