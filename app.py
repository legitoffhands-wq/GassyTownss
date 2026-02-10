from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import os
import uuid
import random
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "gassy-chaos"
socketio = SocketIO(app, cors_allowed_origins="*")

DEVELOPER_PASSWORD = "AdminGasser"

# =====================
# MEMORY STORAGE
# =====================
messages = []
users = {}
user_data = {}
muted_users = set()
pinned_message = None
chat_locked = False
chaos_mode = False

# =====================
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gassytown Control</title>
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<style>
body{
margin:0;
font-family:Arial;
background:radial-gradient(circle,#0f2027,#000);
color:white;
transition:0.4s;
}

.chaos{
animation:shake 0.2s infinite alternate;
background:radial-gradient(circle,#1a0000,#000);
}

@keyframes shake{
from{transform:translate(1px,1px)}
to{transform:translate(-1px,-1px)}
}

.panel{
max-width:1100px;
margin:30px auto;
background:rgba(0,0,0,0.85);
padding:30px;
border-radius:20px;
box-shadow:0 0 40px #00ff88;
}

h1,h2{text-align:center}

#messages{
height:300px;
overflow-y:auto;
background:#111;
padding:15px;
border-radius:10px;
margin-bottom:10px;
}

.msg{margin-bottom:8px;padding:6px;border-bottom:1px solid #222;}
.admin{color:#ff4444;font-weight:bold;}
.bot{color:#00ff88;}
.pinned{background:#222;padding:10px;border-radius:8px;margin-bottom:10px;}

button{padding:6px 10px;border:none;border-radius:6px;background:#1b5e20;color:white;cursor:pointer;}
input{padding:6px;border-radius:6px;border:none;margin:3px;}

.sidebar{
float:right;
width:200px;
background:#111;
padding:10px;
border-radius:10px;
height:300px;
overflow:auto;
}

.clearfix::after{content:"";display:block;clear:both;}
.small{font-size:12px;color:#aaa;}
</style>
</head>
<body>

<div class="panel">
<h1>🌪 GASSYTOWN CHAOS CONTROL</h1>

<div id="login">
<input id="username" placeholder="Username">
<input id="password" placeholder="Dev Password (optional)">
<button onclick="join()">Enter</button>
<p id="status"></p>
</div>

<div id="main" style="display:none;">
<div class="clearfix">

<div class="sidebar">
<h3>Online</h3>
<div id="online"></div>
<hr>
<h3>Leaderboard</h3>
<div id="leaderboard"></div>
</div>

<div style="margin-right:220px;">
<div id="pinned"></div>
<div id="messages"></div>

<input id="message" placeholder="Message">
<button onclick="send()">Send</button>
<button onclick="changeColor()">Color</button>
<button onclick="showStats()">Stats</button>
</div>

</div>

<div id="devPanel" style="display:none;margin-top:20px;">
<h2>👑 Developer Panel</h2>
<button onclick="clearChat()">Clear Chat</button>
<button onclick="toggleLock()">Lock Chat</button>
<button onclick="toggleChaos()">Toggle Chaos</button>
<button onclick="announce()">Announcement</button>
</div>

</div>
</div>

<script>
const socket = io();
let isDev=false;
let myName="";
let myColor="white";

function join(){
socket.emit("join",{
username:username.value,
password:password.value
});
}

socket.on("join_ok",data=>{
login.style.display="none";
main.style.display="block";
status.innerText="";
isDev=data.dev;
myName=data.username;
myColor=data.color;
if(isDev) devPanel.style.display="block";
});

socket.on("status",msg=>status.innerText=msg);

socket.on("update_online",list=>{
online.innerHTML="";
list.forEach(u=>{
online.innerHTML+="<div>"+u+"</div>";
});
});

socket.on("leaderboard",list=>{
leaderboard.innerHTML="";
list.forEach(u=>{
leaderboard.innerHTML+="<div>"+u.name+" (Lv."+u.level+")</div>";
});
});

socket.on("chat_history",data=>{
messages.innerHTML="";
data.forEach(addMsg);
});

socket.on("new_message",addMsg);

socket.on("delete_msg",id=>{
document.getElementById(id)?.remove();
});

socket.on("pin",msg=>{
pinned.innerHTML='<div class="pinned">📌 '+msg+'</div>';
});

socket.on("chaos",state=>{
document.body.classList.toggle("chaos",state);
});

function addMsg(m){
let div=document.createElement("div");
div.className="msg";
div.id=m.id;
div.innerHTML='<span style="color:'+m.color+'">'+m.username+
': '+m.text+'</span> <span class="small">🔥'+m.reactions+'</span>';
messages.appendChild(div);
messages.scrollTop=messages.scrollHeight;
}

function send(){
socket.emit("send",message.value);
message.value="";
}

function changeColor(){
let c=prompt("Enter CSS color:");
if(c){
myColor=c;
socket.emit("color",c);
}
}

function showStats(){
socket.emit("stats");
}

function clearChat(){socket.emit("clear");}
function toggleLock(){socket.emit("lock");}
function toggleChaos(){socket.emit("chaos_toggle");}
function announce(){
let msg=prompt("Announcement:");
if(msg) socket.emit("announce",msg);
}
</script>
</body>
</html>
"""

# =====================
@app.route("/")
def home():
    return render_template_string(HTML)

# =====================
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
        "xp":0,
        "level":1,
        "color":"white",
        "dev": password==DEVELOPER_PASSWORD
    }

    emit("join_ok",{
        "username":username,
        "dev":user_data[sid]["dev"],
        "color":"white"
    })

    emit("chat_history",messages)
    update_online()
    update_leaderboard()

# =====================
@socketio.on("send")
def send(msg):
    sid=request.sid
    if chat_locked and not user_data[sid]["dev"]:
        return
    if sid in muted_users:
        return

    user=user_data[sid]
    user["xp"]+=5
    if user["xp"]>=user["level"]*50:
        user["level"]+=1

    message={
        "id":str(uuid.uuid4()),
        "username":users[sid],
        "text":msg,
        "color":user["color"],
        "reactions":random.randint(0,3)
    }

    messages.append(message)
    emit("new_message",message,broadcast=True)
    update_leaderboard()

# =====================
@socketio.on("color")
def color(c):
    user_data[request.sid]["color"]=c

@socketio.on("clear")
def clear():
    if user_data[request.sid]["dev"]:
        messages.clear()
        emit("chat_history",[],broadcast=True)

@socketio.on("lock")
def lock():
    global chat_locked
    if user_data[request.sid]["dev"]:
        chat_locked=not chat_locked

@socketio.on("chaos_toggle")
def chaos_toggle():
    global chaos_mode
    if user_data[request.sid]["dev"]:
        chaos_mode=not chaos_mode
        emit("chaos",chaos_mode,broadcast=True)

@socketio.on("announce")
def announce(msg):
    if user_data[request.sid]["dev"]:
        emit("pin",msg,broadcast=True)

@socketio.on("disconnect")
def disconnect():
    users.pop(request.sid,None)
    user_data.pop(request.sid,None)
    update_online()
    update_leaderboard()

# =====================
def update_online():
    emit("update_online",list(users.values()),broadcast=True)

def update_leaderboard():
    lb=[{"name":users[s],"level":user_data[s]["level"]}
        for s in users]
    lb=sorted(lb,key=lambda x:x["level"],reverse=True)
    emit("leaderboard",lb,broadcast=True)

# =====================
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
