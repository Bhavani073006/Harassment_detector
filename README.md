# Silent Guardian – Live Chat with Harassment Detector

A minimal two-user chat demo that **auto-detects harassment** and offers **Ignore / Block** actions.

## ✨ Features
- Real-time chat using Socket.IO
- Harassment detection (keyword/regex demo with mild vs severe)
- Per-user block list
- Ignore on the client side
- Simple, clean UI

> For a student project, this clearly demonstrates "message → detector → action".

## 🧰 Tech
- Python 3.9+
- Flask + Flask-SocketIO
- Eventlet (for the Socket.IO server)

## ▶️ Run locally

```bash
# 1) Create & activate a virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Start the app
python app.py
```
Now open **(https://harassment-detector2.onrender.com)** in two browser windows/tabs.
- In one, login as `Alice`
- In the other, login as `Bob`
- Pick each other from the user list and start chatting

Try messages like:
- `hi` → Safe
- `you are useless` → Harassment (severe)
- `I will kill you` → Harassment (severe)
- `dumb idea` → Harassment (mild)
- `kill the process` → Safe (whitelisted context)

## 🧪 What happens on harassment?
- The message is delivered but **flagged** (red border & badge).
- The receiver sees **Ignore** and **Block** buttons below that message.
- If **Block** is pressed, future messages from that sender are not delivered.

## 📦 Project Structure
```
silent_guardian_chat/
├─ app.py                # Flask + Socket.IO server
├─ requirements.txt
├─ templates/
│  └─ index.html         # UI
└─ static/
   ├─ style.css          # Styling
   └─ client.js          # Front-end logic
```

## 🚀 Ideas to extend
- Replace keyword rules with a small ML model (e.g., scikit-learn or a tiny transformer)
- Persist chats and blocks in SQLite
- Add auto-reply suggestions ("This message violates our policy")
- Add admin dashboard for reports
- Integrate with Telegram bot API (simpler than WhatsApp)
```

