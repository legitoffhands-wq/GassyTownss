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
overflow:hidden;
font-family:Arial;
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

<audio id="fart" src="https://www.myinstants.com/media/sounds/fart-with-reverb.mp3"></audio>
<audio id="voice1" src="https://www.myinstants.com/media/sounds/hey-stinky.mp3"></audio>
<audio id="voice2" src="https://www.myinstants.com/media/sounds/oh-no.mp3"></audio>

<script>

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

/* TOTAL CHAOS */
document.querySelectorAll("*").forEach(el=>{
el.style.transition="3s";
el.style.transform=
"rotate("+ (Math.random()*1080-540)+"deg) "+
"translate("+ (Math.random()*600-300)+"px,"+
(Math.random()*600-300)+"px)";
});

/* FADE TO BLACK */
setTimeout(()=>{
blackout.classList.add("show");
},3000);

/* KICK USER OUT */
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

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
