"""FastAPI app: chat, tra cuu, admin CRUD + thong ke. Phuc vu frontend tinh."""
import os
import secrets

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import db
from .chatbot import Chatbot
from .knowledge import KnowledgeBase
from .train import load_model

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = os.path.join(BASE, "frontend")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "admin-demo-123")  # chi la token DEMO

kb = KnowledgeBase()
bot = Chatbot(kb, load_model())
app = FastAPI(title="Admission AI Chatbot (ACU – dữ liệu minh họa)", version="1.0")


class ChatIn(BaseModel):
    message: str
    session_id: str = "anon"


@app.get("/health")
def health():
    return {"status": "ok", "majors": len(kb.majors),
            "intents": len(bot.model.classes_), "data_note": "Dữ liệu tuyển sinh MINH HỌA (ACU giả định)"}


@app.post("/chat")
def chat(payload: ChatIn):
    if not payload.message.strip():
        raise HTTPException(422, "message không được rỗng")
    res = bot.reply(payload.session_id, payload.message.strip())
    # Luu ca intent/confidence/fallback len dong user de thong ke admin dung duoc
    db.save_message(payload.session_id, "user", payload.message.strip(), res["intent"],
                    res["confidence"], res["fallback"])
    db.save_message(payload.session_id, "assistant", res["reply"], res["intent"],
                    res["confidence"], res["fallback"])
    return res


@app.get("/api/majors")
def list_majors():
    return {"majors": kb.majors}


@app.get("/api/majors/{code}")
def get_major(code: str):
    m = kb.get_major(code)
    if not m:
        raise HTTPException(404, "Không tìm thấy ngành")
    return m


@app.get("/api/methods")
def list_methods():
    return {"methods": kb.methods}


@app.get("/api/history/{session_id}")
def get_history(session_id: str):
    return {"session_id": session_id, "messages": db.history(session_id)}


def require_admin(x_admin_token: str = Header(default="")):
    if not secrets.compare_digest(x_admin_token, ADMIN_TOKEN):
        raise HTTPException(401, "Thiếu/sai X-Admin-Token (demo: admin-demo-123)")
    return True


@app.get("/api/admin/stats", dependencies=[Depends(require_admin)])
def admin_stats():
    return db.stats()


@app.post("/api/admin/majors", dependencies=[Depends(require_admin)])
def admin_upsert_major(major: dict):
    if not major.get("code") or not major.get("name"):
        raise HTTPException(422, "Ngành cần có code và name")
    return kb.upsert_major(major)


@app.delete("/api/admin/majors/{code}", dependencies=[Depends(require_admin)])
def admin_delete_major(code: str):
    if not kb.delete_major(code):
        raise HTTPException(404, "Không tìm thấy ngành")
    return {"deleted": code}


@app.post("/api/admin/faqs", dependencies=[Depends(require_admin)])
def admin_upsert_faq(faq: dict):
    if not faq.get("id") or not faq.get("answer"):
        raise HTTPException(422, "FAQ cần có id và answer")
    return kb.upsert_faq(faq)


@app.delete("/api/admin/faqs/{faq_id}", dependencies=[Depends(require_admin)])
def admin_delete_faq(faq_id: str):
    if not kb.delete_faq(faq_id):
        raise HTTPException(404, "Không tìm thấy FAQ")
    return {"deleted": faq_id}


@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND, "index.html"))


@app.get("/admin")
def admin_page():
    return FileResponse(os.path.join(FRONTEND, "admin.html"))


app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
