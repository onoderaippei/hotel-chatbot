import re
from typing import Tuple, Dict
HOURS = {"ja":["営業時間","何時","open","閉"],"en":["hour","open","close"],"zh":["营业","开","关"],"ko":["영업","시간","오픈","마감"]}
LOC   = {"ja":["どこ","場所","フロア"],"en":["where","location","floor"],"zh":["在哪","位置","楼层"],"ko":["어디","위치","층"]}
REQ   = {"ja":["花束","アレルギー","貸出","依頼","お願い","記念日"],"en":["bouquet","allergy","borrow","request","anniversary"],
         "zh":["花束","过敏","借用","请求","纪念日"],"ko":["꽃다발","알레르기","대여","요청","기념일"]}
ROOM_RE = re.compile(r"(?:部屋|room)\s*(\d{3,4})")

def detect_intent(text: str, lang: str) -> Tuple[str, Dict]:
    t = text.lower(); entities={}
    m = ROOM_RE.search(text)
    if m: entities["room_no"] = m.group(1)
    if any(w in text for w in HOURS.get(lang, [])): return "hours", entities
    if any(w in text for w in LOC.get(lang, [])):   return "location", entities
    if any(w in text for w in REQ.get(lang, [])):
        if "花束" in text or "bouquet" in t: entities["category"]="bouquet"
        elif "アレルギ" in text or "allergy" in t: entities["category"]="allergy"
        elif "貸出" in text or "borrow" in t: entities["category"]="rental"
        else: entities["category"]="general"
        return "request_ticket", entities
    if "?" in text or any(k in t for k in ["wifi","spa","bath","onsen","大浴場","レストラン","チェックアウト"]):
        return "faq_generic", entities
    return "fallback", entities
