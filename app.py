from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import os
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(24).hex())

socketio = SocketIO(
    app,
    async_mode="eventlet",
    cors_allowed_origins="*"
)

messages = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gassytown</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<style>
body {
    margin:0;
    font-family:sans-serif;
    background:#1e7d32;
    color:white;
}
.container {
    max-width:900px;
    margin:50px auto;
    background:white;
    color:black;
    padding:40px;
    border-radius:20px;
}
.chat {
    height:300px;
    overflow:auto;
    background:#f3fff3;
    padding:15px;
    border-radius:10px;
}
.msg {
    background:white;
    border:2px solid #4caf50;
    padding:10px;
    margin:8px 0;
    border-radius:10px;
}
</style>
</head>

<body>

<div class="container">
<h1>Gassytown</h1>

<div id="chat" class="chat"></div>

<form id="form">
<input id="input" class="form-control mt-3">
<button class="btn btn-success mt-2">Blast</button>
</form>

</div>

<script>
const socket = io({ transports: ["websocket"] });

socket.on("message", msg => {
    const box = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = "msg";
    div.textContent = msg;
    box.appendChild(div);
});

document.getElementById("form").onsubmit = e => {
    e.preventDefault();
    const input = document.getElementById("input");
    if(input.value.trim()){
        socket.emit("message", input.value.trim());
        input.value="";
    }
};
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@socketio.on("message")
def handle_message(msg):
    messages.append(msg)
    emit("message", msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
