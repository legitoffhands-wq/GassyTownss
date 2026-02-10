from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import os, uuid, random

app = Flask(__name__)
app.config["SECRET_KEY"] = "gassy-chaos"
socketio = SocketIO(app, cors_allowed_origins="*")

DEVELOPER_PASSWORD = "AdminGasser"

messages = []
users = {}
user_data = {}
chat_locked = False

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gassytown Universe</title>
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<style>
body{
margin:0;
font-family:Arial;
background:radial-gradient(circle,#0f2027,#000);
color:white;
overflow-x:hidden;
transition:0.3s;
}

/* MENU */
.menu-btn{
position:fixed;
top:20px;
left:20px;
font-size:30px;
cursor:pointer;
z-index:1000;
}

.sidebar{
position:fixed;
left:-250px;
top:0;
width:250px;
height:100%;
background:#111;
padding-top:60px;
transition:0.3s;
box-shadow:0 0 20px #00ff88;
z-index:999;
}

.sidebar a{
display:block;
padding:15px;
color:white;
text-decoration:none;
transition:0.2s;
}

.sidebar a:hover{
background:#1b5e20;
}

.sidebar.open{
left:0;
}

/* SECTIONS */
.section{
display:none;
padding:80px 20px;
max-width:1100px;
margin:auto;
}

.active{
display:block;
}

/* HOME */
#gassy{
max-width:60%;
border-radius:20px;
box-shadow:0 0 30px #00ff88;
cursor:pointer;
transition:0.3s;
}

#gassy:hover{
transform:scale(1.05);
}

/* CHAT */
#messages{
height:300px;
overflow-y:auto;
background:#111;
padding:10px;
border-radius:10px;
margin-bottom:10px;
}

.msg{
margin-bottom:6px;
padding:5px;
border-bottom:1px solid #222;
}

.dev{
color:#ff4444;
font-weight:bold;
}

button{
padding:6px 10px;
border:none;
border-radius:6px;
background:#1b5e20;
color:white;
cursor:pointer;
}

input{
padding:6px;
border-radius:6px;
border:none;
margin:3px;
}

.panel{
background:rgba(0,0,0,0.85);
padding:20px;
border-radius:20px;
box-shadow:0 0 30px #00ff88;
}

</style>
</head>
<body>

<div class="menu-btn" onclick="toggleMenu()">☰</div>

<div class="sidebar" id="sidebar">
<a href="#" onclick="showSection('home')">🏠 Home</a>
<a href="#" onclick="showSection('chat')">💬 Chat</a>
</div>

<!-- HOME SECTION -->
<div id="home" class="section active">
<div class="panel">
<h1>🌪 Welcome to Gassytown</h1>
<p>The chaotic meme universe.</p>
<img id="gassy" src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg">
<p>Scroll. Explore. Or open chat from the menu.</p>
</div>
</div>

<!-- CHAT SECTION -->
<div id="chat" class="section">
<div class="panel">

<div id="login">
<h2>Enter Chat</h2>
<input id="username" placeholder="Username">
<input id="password" placeholder="Dev Password (optional)">
<button onclick="join()">Enter</button>
<p id="status"></p>
</div>

<div id="chatMain" style="display:none;">
<h2>💬 Gassy Live Chat</h2>
<div id="messages"></div>
<input id="message" placeholder="Message">
<button onclick="sendMsg()">Send</button>

<div id="devPanel" style="display:none;margin-top:10px;">
<hr>
<h3>👑 Dev Controls</h3>
<button onclick="clearChat()">Clear</button>
<button onclick="lockChat()">Lock/Unlock</button>
<button onclick="announce()">Announce</button>
</div>

</div>
</div>
</div>

<script>
const socket = io();
let isDev=false;

/* MENU */
function toggleMenu(){
document.getElementById("sidebar").classList.toggle("open");
}

function showSection(id){
document.querySelectorAll(".section").forEach(s=>s.classList.remove("active"));
document.getElementById(id).classList.add("active");
toggleMenu();
}

/* CHAT */
function join(){
socket.emit("join",{
username:username.value,
password:password.value
});
}

socket.on("join_ok",data=>{
login.style.display="none";
chatMain.style.display="block";
isDev=data.dev;
if(isDev) devPanel.style.display="block";
});

socket.on("status",msg=>{
status.innerText=msg;
});

socket.on("history",data=>{
messages.innerHTML="";
data.forEach(addMsg);
});

socket.on("new_msg",addMsg);

function addMsg(m){
let div=document.createElement("div");
div.className="msg";
div.innerHTML="<span style='color:"+m.color+"'>"+
m.username+(m.dev?" 👑":"")+": "+
m.text+"</span>";
messages.appendChild(div);
messages.scrollTop=messages.scrollHeight;
}

function sendMsg(){
socket.emit("send",message.value);
message.value="";
}

function clearChat(){socket.emit("clear");}
function lockChat(){socket.emit("lock");}
function announce(){
let m=prompt("Announcement:");
if(m) socket.emit("announce",m);
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("join")
def join(data):
    username=data["username"]
    password=data["password"]
    sid=request.sid

    if not username:
        emit("status","Username required")
        return

    if username in users.values():
        emit("status","Username taken")
        return

    users[sid]=username
    user_data[sid]={
        "dev": password==DEVELOPER_PASSWORD,
        "color": "#"+''.join(random.choices('0123456789ABCDEF',k=6))
    }

    emit("join_ok",{"dev":user_data[sid]["dev"]})
    emit("history",messages)
    
@socketio.on("send")
def send(msg):
    sid=request.sid
    if sid not in users:
        return

    message={
        "username":users[sid],
        "text":msg,
        "color":user_data[sid]["color"],
        "dev":user_data[sid]["dev"]
    }

    messages.append(message)
    emit("new_msg",message,broadcast=True)

@socketio.on("clear")
def clear():
    sid=request.sid
    if user_data.get(sid,{}).get("dev"):
        messages.clear()
        emit("history",[],broadcast=True)

@socketio.on("lock")
def lock():
    global chat_locked
    sid=request.sid
    if user_data.get(sid,{}).get("dev"):
        chat_locked=not chat_locked

@socketio.on("announce")
def announce(msg):
    sid=request.sid
    if user_data.get(sid,{}).get("dev"):
        emit("new_msg",{
            "username":"SYSTEM",
            "text":"📢 "+msg,
            "color":"#00ff88",
            "dev":True
        },broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
