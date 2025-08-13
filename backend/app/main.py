import os
BASE_DIR = os.path.dirname(__file__)                # .../backend/app
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
DB_PATH  = os.path.abspath(os.path.join(BASE_DIR, "..", "app.db"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from .models import init_db, add_ticket, TicketIn, log_query
from .data_loader import load_all
from .search import search_faq
from .nlu_rules import detect_intent

app = FastAPI(title="WAKON Concierge (Local)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080","http://127.0.0.1:8080"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

#DB = init_db("./app.db")
DATA_DIR = "./data"
#FAQS = load_all(DATA_DIR)
FAQS = load_all(DATA_DIR)
SUPPORTED_LANGS = set(FAQS.keys())
DB = init_db(DB_PATH)

class ChatIn(BaseModel):
    session_id: Optional[str] = None
    lang: str = Field(default="ja")
    text: str

class ChatOut(BaseModel):
    reply_type: str
    payload: Dict[str, Any]

class FaqHit(BaseModel):
    id: str
    title: str
    answer: str
    confidence: float

class TicketOut(BaseModel):
    id: int
    status: str

@app.post("/api/admin/reload")
def reload_faq():
    global FAQS, SUPPORTED_LANGS
    FAQS = load_all(DATA_DIR)
    SUPPORTED_LANGS = set(FAQS.keys())
    return {"status":"ok","langs":list(SUPPORTED_LANGS)}

@app.get("/api/faq/search", response_model=Dict[str, List[FaqHit]])
def faq_search(q: str, lang: str = "ja"):
    if lang not in SUPPORTED_LANGS: raise HTTPException(400, "unsupported lang")
    hits = search_faq(q, FAQS[lang], topk=3)
    return {"hits":[FaqHit(**h) for h in hits]}

@app.post("/api/tickets", response_model=TicketOut)
def tickets_create(ticket: TicketIn):
    tid = add_ticket(DB, ticket)
    return {"id": tid, "status": "accepted"}

@app.post("/api/chat/message", response_model=ChatOut)
def chat_message(msg: ChatIn):
    lang = msg.lang if msg.lang in SUPPORTED_LANGS else "ja"
    intent, entities = detect_intent(msg.text, lang)

    if intent in ("hours","location","faq_generic"):
        hits = search_faq(msg.text, FAQS[lang], topk=3)
        log_query(DB, msg.session_id, lang, msg.text, intent, resolved=bool(hits))
        if hits:
            return {"reply_type":"faq","payload":{"top_hit":hits[0],"alternatives":hits[1:]}}
        return {"reply_type":"fallback","payload":{"message":"関連情報が見つかりませんでした。"}}

    if intent == "request_ticket":
        sample_ticket = TicketIn(
            type=entities.get("category","general"),
            room_no=entities.get("room_no"),
            note=msg.text
        )
        tid = add_ticket(DB, sample_ticket)
        log_query(DB, msg.session_id, lang, msg.text, intent, resolved=True)
        return {"reply_type":"ticket","payload":{"ticket_id":tid,"message":"ご要望を受け付けました。"}}

    log_query(DB, msg.session_id, lang, msg.text, intent, resolved=False)
    return {"reply_type":"fallback","payload":{"message":"すみません、よく分かりませんでした。"}}
