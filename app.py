from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "gassy-chaos"
socketio = SocketIO(app, cors_allowed_origins="*")

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gassytown</title>
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<style>
body{
margin:0;
background:radial-gradient(circle at center,#1b5e20,#000);
font-family:Arial;
color:#111;
}

/* SCROLL SMOOTH */
html{
scroll-behavior:smooth;
}

/* GAS TRAIL */
.gas{
position:fixed;
width:12px;
height:12px;
background:radial-gradient(circle,#7CFF7C,transparent);
border-radius:50%;
pointer-events:none;
filter:blur(4px);
opacity:0.8;
animation:gasfade 2s forwards;
}
@keyframes gasfade{
to{
opacity:0;
transform:translate(
    calc(-40px + 80px * var(--x)),
    calc(-40px + 80px * var(--y))
) scale(2);
}
}

/* MAIN CONTAINER */
.container{
position:relative;
max-width:1100px;
margin:60px auto;
padding:40px;
background:rgba(255,255,255,0.95);
border-radius:30px;
box-shadow:0 0 80px rgba(0,255,0,0.6);
text-align:center;
}

/* IMAGE */
#gassy{
max-width:65%;
border-radius:25px;
transition:0.3s;
cursor:pointer;
box-shadow:0 0 0px #7CFF7C;
}
#gassy:hover{
transform:scale(1.08);
box-shadow:0 0 40px #7CFF7C;
}

/* INFO SECTION */
.info-section{
max-width:1000px;
margin:120px auto;
padding:50px;
background:rgba(255,255,255,0.95);
border-radius:30px;
box-shadow:0 0 50px rgba(0,255,0,0.4);
}

.info-section h2{
color:#1b5e20;
font-size:40px;
margin-bottom:20px;
}

.info-grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
gap:30px;
margin-top:40px;
}

.info-card{
background:#e8ffe8;
padding:25px;
border-radius:20px;
box-shadow:0 0 20px rgba(0,255,0,0.2);
transition:0.3s;
}

.info-card:hover{
transform:translateY(-10px);
box-shadow:0 0 30px rgba(0,255,0,0.5);
}

/* CHAT SECTION */
.chat-section{
max-width:900px;
margin:150px auto 80px;
padding:40px;
background:rgba(0,0,0,0.85);
border-radius:30px;
box-shadow:0 0 60px rgba(0,255,0,0.6);
color:#7CFF7C;
}

#messages{
height:300px;
overflow-y:auto;
background:#111;
padding:20px;
border-radius:15px;
margin-bottom:20px;
font-size:14px;
}

.chat-input{
display:flex;
gap:10px;
}

.chat-input input{
flex:1;
padding:12px;
border-radius:10px;
border:none;
outline:none;
}

.chat-input button{
padding:12px 20px;
border-radius:10px;
border:none;
background:#1b5e20;
color:white;
cursor:pointer;
}

.chat-input button:hover{
background:#2e7d32;
}

/* CHAOS */
.shake{
animation:shake 0.1s infinite;
}
@keyframes shake{
0%{transform:translate(0,0)}
25%{transform:translate(5px,-5px)}
50%{transform:translate(-5px,5px)}
75%{transform:translate(5px,5px)}
}

/* BLACKOUT */
#blackout{
position:fixed;
inset:0;
background:black;
opacity:0;
pointer-events:none;
transition:2s;
z-index:999;
display:flex;
align-items:center;
justify-content:center;
flex-direction:column;
color:#7CFF7C;
font-size:32px;
}
#blackout.show{
opacity:1;
pointer-events:auto;
}
</style>
</head>

<body>

<div id="blackout">
<img src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg" style="max-width:50%;border-radius:20px">
<p>hey there gasser.</p>
<p>do you want to escape?</p>
</div>

<div class="container">
<h1>GASSYTOWN</h1>
<p>do not click the gassy.</p>

<img id="gassy"
src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg">
</div>

<!-- INFO SECTION -->
<div class="info-section">
<h2>The Legend of Incredible Gassy</h2>
<p>
Incredible Gassy is not just a meme. It is a movement. A symbol of chaos. 
A mysterious green aura that appears when the internet least expects it.
</p>

<div class="info-grid">
<div class="info-card">
<h3>🌪 Origin</h3>
<p>Born from internet absurdity and amplified by pure chaotic energy.</p>
</div>

<div class="info-card">
<h3>💨 Powers</h3>
<p>Reality distortion, sonic gas waves, psychological intimidation.</p>
</div>

<div class="info-card">
<h3>🧠 Lore</h3>
<p>Some say clicking him awakens the final phase of Gassytown.</p>
</div>

<div class="info-card">
<h3>🔥 Status</h3>
<p>Currently spreading across servers worldwide.</p>
</div>
</div>
</div>

<!-- CHAT SECTION -->
<div class="chat-section">
<h2>Gassy Live Chat</h2>
<div id="messages"></div>
<div class="chat-input">
<input id="username" placeholder="Name">
<input id="message" placeholder="Message">
<button onclick="sendMessage()">Send</button>
</div>
</div>

<audio id="fart" src="https://www.myinstants.com/media/sounds/fart-with-reverb.mp3"></audio>
<audio id="voice1" src="https://www.myinstants.com/media/sounds/hey-stinky.mp3"></audio>
<audio id="voice2" src="https://www.myinstants.com/media/sounds/oh-no.mp3"></audio>

<script>

/* SOCKET CHAT */
const socket = io();
const messages = document.getElementById("messages");

function sendMessage(){
let user = document.getElementById("username").value || "Anonymous";
let msg = document.getElementById("message").value;
if(msg.trim() !== ""){
socket.emit("message", user + ": " + msg);
document.getElementById("message").value="";
}
}

socket.on("message", data=>{
let div=document.createElement("div");
div.textContent=data;
messages.appendChild(div);
messages.scrollTop=messages.scrollHeight;
});

/* GAS MOUSE TRAIL */
document.addEventListener("mousemove",e=>{
for(let i=0;i<2;i++){
let g=document.createElement("div");
g.className="gas";
g.style.left=e.clientX+"px";
g.style.top=e.clientY+"px";
g.style.setProperty("--x",Math.random());
g.style.setProperty("--y",Math.random());
document.body.appendChild(g);
setTimeout(()=>g.remove(),2000);
}
});

/* CHAOS CLICK */
const img=document.getElementById("gassy");
const fart=document.getElementById("fart");
const v1=document.getElementById("voice1");
const v2=document.getElementById("voice2");
const blackout=document.getElementById("blackout");

img.onclick=()=>{
fart.volume=1;
fart.play();
(Math.random()>0.5?v1:v2).play();
document.body.classList.add("shake");

document.querySelectorAll("*").forEach(el=>{
el.style.transition="3s";
el.style.transform=
"rotate("+ (Math.random()*1080-540)+"deg) "+
"translate("+ (Math.random()*600-300)+"px,"+
(Math.random()*600-300)+"px)";
});

setTimeout(()=>{
blackout.classList.add("show");
},3000);

setTimeout(()=>{
window.location.href="about:blank";
},6500);
};

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("message")
def handle_message(msg):
    emit("message", msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
