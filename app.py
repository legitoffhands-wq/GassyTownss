# Gassytown – Ultimate Incredible Gassy Meme Experience
# Render-safe, production-ready, no infinite loading

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
    <title>Gassytown – All About Incredible Gassy</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Roboto:wght@400&display=swap" rel="stylesheet">

    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>

    <style>
        body {
            margin: 0;
            background: linear-gradient(135deg, #0d5c0d, #2e8b57, #4caf50, #81c784);
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
            font-family: 'Roboto', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        #particles-js {
            position: fixed;
            inset: 0;
            z-index: -1;
        }

        .container {
            background: rgba(255,255,255,0.9);
            border-radius: 30px;
            padding: 60px 40px;
            margin: 80px auto;
            max-width: 1300px;
            box-shadow: 0 20px 70px rgba(0,0,0,0.3);
        }

        h1 {
            font-family: 'Fredoka', sans-serif;
            color: #0b4e0b;
            text-align: center;
            font-size: 5rem;
        }

        #gassy-big {
            display: block;
            margin: 40px auto;
            max-width: 80%;
            border-radius: 24px;
            cursor: pointer;
            box-shadow: 0 15px 50px rgba(0,80,0,0.5);
        }

        .section {
            background: rgba(240,255,240,0.85);
            border-radius: 22px;
            padding: 35px;
            margin: 50px 0;
            border-left: 10px solid #2e7d32;
            opacity: 0;
            transform: translateY(40px);
            transition: all 0.8s ease;
        }

        .section.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .chat-container {
            background: #f9fff9;
            border-radius: 24px;
            padding: 30px;
            height: 450px;
            overflow-y: auto;
        }

        .chat-message {
            background: white;
            border: 2px solid #81c784;
            padding: 16px;
            margin: 14px 0;
            border-radius: 18px;
        }

        footer {
            text-align: center;
            padding: 60px 0 40px;
            color: #0b4e0b;
        }
    </style>
</head>
<body>

<div id="particles-js"></div>

<div class="container">
    <h1>Gassytown</h1>
    <p class="text-center fs-4 mb-5">
        Deep dive into <strong>Incredible Gassy</strong>.
    </p>

    <img id="gassy-big"
         src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg">

    <div class="section">
        <h2>Origins</h2>
        <p>Atomic fart legend born from internet chaos.</p>
    </div>

    <div class="section">
        <h2>Chat – Let It Rip</h2>
        <div class="chat-container" id="chat-box"></div>

        <form id="chat-form" class="mt-4">
            <div class="input-group input-group-lg">
                <input id="chat-input" class="form-control" placeholder="Say something gassy…">
                <button class="btn btn-success px-4">Blast</button>
            </div>
        </form>
    </div>
</div>

<footer>Atomic vibes only • Gassytown 2026</footer>

<audio id="fart-sound" preload="auto">
    <source src="https://www.soundjay.com/human/sounds/fart-01.mp3">
</audio>

<script>
    particlesJS("particles-js", {
        particles: {
            number: { value: 100 },
            color: { value: "#4caf50" },
            opacity: { value: 0.6, random: true },
            size: { value: 5, random: true },
            move: { enable: true, speed: 3 }
        }
    });

    const socket = io({ transports: ["websocket"] });

    socket.on("message", msg => {
        const box = document.getElementById("chat-box");
        const div = document.createElement("div");
        div.className = "chat-message";
        div.textContent = msg;
        box.appendChild(div);
        box.scrollTop = box.scrollHeight;
    });

    document.getElementById("chat-form").onsubmit = e => {
        e.preventDefault();
        const input = document.getElementById("chat-input");
        if (input.value.trim()) {
            socket.emit("message", input.value.trim());
            input.value = "";
        }
    };

    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => e.isIntersecting && e.target.classList.add("visible"));
    });

    document.querySelectorAll(".section").forEach(s => observer.observe(s));
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
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
