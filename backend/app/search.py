from typing import List, Dict
from rapidfuzz import fuzz, process

def _cand(faqs): return {f["id"]: (f["q"] + " " + " ".join(f.get("keywords", []))) for f in faqs}

def search_faq(query: str, faqs: List[Dict], topk: int = 3):
    if not query.strip(): return []
    mapping = _cand(faqs)
    scored = process.extract(query, mapping, scorer=fuzz.WRatio, limit=topk)
    results = []
    for (faq_id, _joined, score, _idx) in scored:
        item = next(f for f in faqs if f["id"] == faq_id)
        results.append({
            "id": item["id"], "title": item["q"], "answer": item["a"],
            "confidence": round(score/100.0, 2)
        })
    return results
