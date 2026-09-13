"""
server.py  –  SecureChat Flask-SocketIO backend
Run:  python server.py
Then open  http://127.0.0.1:5000  in multiple browser tabs (one per user).
"""

from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "securechat-dev-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

# sid -> {username, public_key}
clients = {}
# username -> sid
username_to_sid = {}


def broadcast_userlist():
    users = [v["username"] for v in clients.values()]
    socketio.emit("userlist", {"users": users})


@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


@socketio.on("connect")
def on_connect():
    pass


@socketio.on("register")
def on_register(data):
    sid = request.sid
    username = data.get("username", "").strip()
    public_key = data.get("public_key", "")

    if not username:
        return

    # Remove old session with same name
    if username in username_to_sid:
        old_sid = username_to_sid[username]
        clients.pop(old_sid, None)

    clients[sid] = {"username": username, "public_key": public_key}
    username_to_sid[username] = sid

    # Send all existing keys to the new user
    for other_sid, info in list(clients.items()):
        if other_sid != sid:
            emit("peer_key", {
                "username": info["username"],
                "public_key": info["public_key"]
            })

    # Broadcast new user's key to everyone else
    emit("peer_key", {
        "username": username,
        "public_key": public_key
    }, broadcast=True, include_self=False)

    broadcast_userlist()


@socketio.on("send_message")
def on_message(data):
    receiver = data.get("to")
    if receiver not in username_to_sid:
        emit("error_msg", {"msg": f"User '{receiver}' not found"})
        return
    target_sid = username_to_sid[receiver]
    socketio.emit("receive_message", data, to=target_sid)


@socketio.on("disconnect")
def on_disconnect(reason=None):
    sid = request.sid
    if sid in clients:
        username = clients[sid]["username"]
        del clients[sid]
        if username_to_sid.get(username) == sid:
            del username_to_sid[username]
        broadcast_userlist()


if __name__ == "__main__":
    print("=" * 52)
    print("  SecureChat  →  http://127.0.0.1:5000")
    print("  Open in multiple browser tabs for multi-user")
    print("=" * 52)
    socketio.run(app, host="127.0.0.1", port=5000, debug=False)