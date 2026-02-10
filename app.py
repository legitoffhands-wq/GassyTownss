from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "gassytown-secret"

socketio = SocketIO(app, cors_allowed_origins="*")

messages = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gassytown</title>

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>

<style>
body{
margin:0;
font-family:Arial;
background:linear-gradient(135deg,#0d5c0d,#4caf50);
overflow-x:hidden;
}

/* mouse trail particles */
.trail{
position:fixed;
width:6px;
height:6px;
background:#4caf50;
border-radius:50%;
pointer-events:none;
animation:fade 1s linear forwards;
}
@keyframes fade{
to{opacity:0; transform:scale(2);}
}

/* container */
.container{
background:white;
max-width:1100px;
margin:60px auto;
padding:40px;
border-radius:30px;
box-shadow:0 20px 60px rgba(0,0,0,0.3);
}

/* big image */
#gassy{
display:block;
margin:auto;
max-width:70%;
border-radius:20px;
transition:0.4s;
box-shadow:0 0 0px #4caf50;
}
#gassy:hover{
transform:scale(1.05);
box-shadow:0 0 30px #4caf50;
}

/* chaos overlay */
#overlay{
position:fixed;
inset:0;
background:black;
opacity:0;
pointer-events:none;
transition:2s;
}
#overlay.active{
opacity:0.95;
}

/* sections */
.section{
margin-top:40px;
padding:20px;
background:#e8f5e9;
border-radius:20px;
}

/* chat */
#chatbox{
height:300px;
overflow:auto;
background:#f4fff4;
padding:20px;
border-radius:20px;
}
.msg{
background:white;
padding:10px;
margin:10px 0;
border-radius:12px;
}
</style>
</head>

<body>

<div id="overlay"></div>

<div class="container">

<h1>Gassytown</h1>

<img id="gassy"
src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg">

<div class="section">
<h2>Origins</h2>
<p>Started as commission animation meme lore.</p>
</div>

<div class="section">
<h2>Rise</h2>
<p>Became viral meme across platforms.</p>
</div>

<div class="section">
<h2>Chat</h2>

<div id="chatbox"></div>

<form id="form">
<input id="input" autocomplete="off">
<button>Send</button>
</form>

</div>

</div>

<script>

/* mouse trail */
document.addEventListener("mousemove",e=>{
let t=document.createElement("div");
t.className="trail";
t.style.left=e.clientX+"px";
t.style.top=e.clientY+"px";
document.body.appendChild(t);
setTimeout(()=>t.remove(),1000);
});

/* socket chat */
const socket=io();

socket.on("message",m=>{
let d=document.createElement("div");
d.className="msg";
d.textContent=m;
chatbox.appendChild(d);
chatbox.scrollTop=chatbox.scrollHeight;
});

form.onsubmit=e=>{
e.preventDefault();
if(input.value){
socket.emit("message",input.value);
input.value="";
}
};

/* chaos click */
const img=document.getElementById("gassy");
const overlay=document.getElementById("overlay");

img.onclick=()=>{
overlay.classList.add("active");

document.querySelectorAll("*").forEach(el=>{
el.style.transition="4s";
el.style.transform=
"translate("+ (Math.random()*500-250)+"px,"+
(Math.random()*400-200)+"px) rotate("+ (Math.random()*360)+"deg)";
});

setTimeout(()=>{
document.body.innerHTML=
'<img src="'+img.src+'" style="position:fixed;inset:0;margin:auto;max-width:90%">';
},4000);

};

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("message")
def handle(msg):
    emit("message", msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
