from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

users_online = set()
blocks = {}            # {user: set(blocked_users)}
rooms_messages = {}    # {room_id: [messages]}

HARASSMENT_PATTERNS = [
    r"\bkill\b", r"\bdie\b", r"\bstupid\b", r"\buseless\b",
    r"\bidiot\b", r"\bworthless\b", r"\bslap\b", r"\bbeat\b",
    r"\bhate\b", r"\bshut\s*up\b", r"\bgo\s*to\s*hell\b"
]

def detect_harassment(text):
    t = text.lower()
    matches = []
    severity = 0
    for p in HARASSMENT_PATTERNS:
        if re.search(p, t):
            matches.append(p)
            severity = 2
    label = "harassment" if matches else "safe"
    return {"label": label, "severity": severity, "matches": matches}

def room_id_for(a, b):
    return "::".join(sorted([a, b]))

# ---------------- Routes ----------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

# ---------------- Socket.IO ----------------
@socketio.on("register")
def handle_register(data):
    username = data.get("username", "").strip()
    if not username:
        emit("register_response", {"ok": False, "error": "Username required"})
        return
    users_online.add(username)
    blocks.setdefault(username, set())
    emit("register_response", {"ok": True, "username": username, "users": sorted(users_online)})
    socketio.emit("users_update", {"users": sorted(users_online)})

@socketio.on("start_chat")
def handle_start_chat(data):
    a = data.get("from")
    b = data.get("to")
    if not a or not b or a == b:
        emit("system", {"msg": "Choose a different user to chat."})
        return
    rid = room_id_for(a, b)
    join_room(rid)
    history = rooms_messages.get(rid, [])
    emit("chat_started", {"room": rid, "history": history})

@socketio.on("send_message")
def handle_send_message(data):
    sender = data.get("from")
    receiver = data.get("to")
    text = data.get("text", "").strip()
    if not sender or not receiver or not text:
        return

    if sender in blocks.get(receiver, set()):
        emit("system", {"msg": f"You are blocked by {receiver}. Cannot send message."}, room=request.sid)
        return

    analysis = detect_harassment(text)
    rid = room_id_for(sender, receiver)
    msg = {
        "from": sender,
        "to": receiver,
        "text": text,
        "status": analysis["label"],
        "ts": datetime.utcnow().strftime("%H:%M:%S")
    }

    rooms_messages.setdefault(rid, []).append(msg)
    socketio.emit("new_message", {"room": rid, "message": msg}, room=rid)

@socketio.on("block_user")
def handle_block_user(data):
    me = data.get("me")
    who = data.get("who")
    if not me or not who:
        return
    blocks.setdefault(me, set()).add(who)
    emit("system", {"msg": f"You have blocked {who}."}, room=request.sid)

@socketio.on("unblock_user")
def handle_unblock_user(data):
    me = data.get("me")
    who = data.get("who")
    if not me or not who:
        return
    blocks.setdefault(me, set()).discard(who)
    emit("system", {"msg": f"You have unblocked {who}."}, room=request.sid)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
