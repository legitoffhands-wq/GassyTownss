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
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gassytown</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap" rel="stylesheet">

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>

<style>
body {
    margin:0;
    font-family:'Fredoka',sans-serif;
    background:linear-gradient(135deg,#0d5c0d,#2e8b57,#4caf50,#81c784);
    background-size:400% 400%;
    animation:bg 20s ease infinite;
}
@keyframes bg {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}
#loader {
    position:fixed;
    inset:0;
    background:#0b3d0b;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:3rem;
    z-index:9999;
}
#particles-js {
    position:fixed;
    inset:0;
    z-index:-1;
}
.container {
    background:white;
    border-radius:30px;
    padding:50px;
    margin:80px auto;
    max-width:1200px;
}
#gassy-big {
    display:block;
    margin:40px auto;
    max-width:80%;
    border-radius:20px;
    cursor:pointer;
}
.section {
    margin:40px 0;
}
.chat-box {
    height:350px;
    overflow:auto;
    background:#f5fff5;
    padding:20px;
    border-radius:15px;
}
.chat-msg {
    background:white;
    border:2px solid #4caf50;
    padding:12px;
    margin:10px 0;
    border-radius:14px;
}
</style>
</head>

<body>

<div id="loader">Loading Gassytown…</div>
<div id="particles-js"></div>

<div class="container" id="main" style="display:none">

<h1 class="text-center">Gassytown</h1>
<p class="text-center fs-4">Click the big pic for chaos</p>

<img id="gassy-big"
src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg">

<div class="section">
<h2>Origins</h2>
<p>Born from internet chaos and atomic gas.</p>
</div>

<div class="section">
<h2>Chat</h2>
<div class="chat-box" id="chat"></div>
<form id="form" class="mt-3">
<input id="input" class="form-control">
<button class="btn btn-success mt-2">Blast</button>
</form>
</div>

</div>

<script>
particlesJS("particles-js",{
particles:{
number:{value:100},
color:{value:"#4caf50"},
size:{value:5,random:true},
move:{enable:true,speed:3}
}
});

const socket = io({transports:["websocket"]});

socket.on("connect",()=>{
    document.getElementById("loader").style.display="none";
    document.getElementById("main").style.display="block";
});

socket.on("message",msg=>{
    const box=document.getElementById("chat");
    const div=document.createElement("div");
    div.className="chat-msg";
    div.textContent=msg;
    box.appendChild(div);
    box.scrollTop=box.scrollHeight;
});

document.getElementById("form").onsubmit=e=>{
    e.preventDefault();
    const input=document.getElementById("input");
    if(input.value.trim()){
        socket.emit("message",input.value.trim());
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
