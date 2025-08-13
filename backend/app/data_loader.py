import os, pandas as pd
from typing import Dict, List

SUPPORTED = ("ja", "en", "zh", "ko")

def _norm_keywords(v) -> List[str]:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return []
    s = str(v).replace("，", ",")
    sep = ";" if ";" in s else ","
    return [w.strip() for w in s.split(sep) if w.strip()]

def _df_to_list(df: pd.DataFrame) -> List[dict]:
    cols = {c.lower(): c for c in df.columns}
    need = {"id", "q", "a"}
    if not need.issubset(set(cols.keys())):
        raise ValueError("Columns must include: id,q,a")
    out = []
    for _, row in df.iterrows():
        rid = str(row[cols["id"]]).strip()
        if not rid:
            continue
        q = str(row[cols["q"]]).strip()
        a = str(row[cols["a"]]).strip()
        kw = []
        if "keywords" in cols:
            kw = _norm_keywords(row[cols["keywords"]])
        out.append({"id": rid, "q": q, "a": a, "keywords": kw})
    return out

def _load_csvs(folder: str) -> Dict[str, List[dict]]:
    faqs = {}
    for lang in SUPPORTED:
        path = os.path.join(folder, f"faq_{lang}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            faqs[lang] = _df_to_list(df)
    return faqs

def _load_excel(path: str) -> Dict[str, List[dict]]:
    if not os.path.exists(path):
        return {}
    faqs = {}
    xls = pd.ExcelFile(path)
    for lang in SUPPORTED:
        if lang in xls.sheet_names:
            df = pd.read_excel(path, sheet_name=lang)
            faqs[lang] = _df_to_list(df)
    return faqs

def load_all(data_dir: str) -> Dict[str, List[dict]]:
    faqs = _load_csvs(data_dir)
    if not faqs:
        faqs = _load_excel(os.path.join(data_dir, "faq.xlsx"))
    for lang in SUPPORTED:
        faqs.setdefault(lang, [])
    return faqs
