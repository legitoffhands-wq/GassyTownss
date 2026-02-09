# Gassytown – Ultimate Incredible Gassy Meme Experience
# Packed with lore, effects, chaos on big picture click, and more

from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
socketio = SocketIO(app)

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
            color: #111;
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
            transition: all 0.6s ease;
        }
        .container:hover {
            transform: translateY(-10px);
            box-shadow: 0 30px 90px rgba(0,0,0,0.4);
        }
        h1 {
            font-family: 'Fredoka', sans-serif;
            color: #0b4e0b;
            text-align: center;
            font-size: 5rem;
            text-shadow: 5px 5px 12px rgba(76,175,80,0.7);
            animation: popIn 1.5s ease-out;
        }
        @keyframes popIn {
            0% { transform: scale(0.6); opacity: 0; }
            70% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); }
        }
        #gassy-big {
            display: block;
            margin: 40px auto;
            max-width: 80%;
            border-radius: 24px;
            box-shadow: 0 15px 50px rgba(0,80,0,0.5);
            cursor: pointer;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }
        #gassy-big:hover {
            transform: scale(1.05);
            box-shadow: 0 25px 70px rgba(76,175,80,0.8);
        }
        #chaos-overlay {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0);
            pointer-events: none;
            z-index: 2000;
            transition: background 4s ease;
        }
        .chaos-active {
            background: rgba(0,0,0,0.95) !important;
            transition: background 5s ease;
        }
        .chaos-active .container, .chaos-active #gassy-big, .chaos-active footer {
            opacity: 0;
            transition: opacity 4s ease;
        }
        .section {
            background: rgba(240,255,240,0.8);
            border-radius: 22px;
            padding: 35px;
            margin: 50px 0;
            border-left: 10px solid #2e7d32;
            opacity: 0;
            transform: translateY(50px);
            transition: all 1s ease;
        }
        .section.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .fun-fact {
            font-style: italic;
            color: #1b5e20;
            background: #e8f5e9;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
        }
        .chat-container {
            background: #f9fff9;
            border-radius: 24px;
            padding: 30px;
            height: 500px;
            overflow-y: auto;
            box-shadow: inset 0 4px 15px rgba(0,0,0,0.1);
            margin-top: 40px;
        }
        .chat-message {
            background: white;
            border: 2px solid #81c784;
            padding: 18px;
            margin: 18px 0;
            border-radius: 20px;
            transition: transform 0.4s;
        }
        .chat-message:hover {
            transform: translateX(10px);
        }
        footer {
            text-align: center;
            padding: 80px 0 40px;
            color: #0b4e0b;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <div id="chaos-overlay"></div>

    <div class="container">
        <h1>Gassytown</h1>
        <p class="text-center fs-4 mb-5">Deep dive into <strong>Incredible Gassy</strong> – the atomic fart legend. Click the big pic for ultimate chaos.</p>

        <img id="gassy-big" src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg" alt="Incredible Gassy Big">

        <div class="section">
            <h2>The Origins (2021)</h2>
            <p>Incredible Gassy started as a private commission by artist Bobo Comics (@BobocomicsArt) in 2021. Originally called "Incredible Fatty" in concept art, it turned into a fart-fetish animation parody of Mr. Incredible from The Incredibles. The character is morbidly obese, wears a lime-green supersuit, and has "atomic toxic farts" as his power. The original (now partially lost) explicit animation shows him riding an oversized toy while unleashing massive farts. Bobo later said it wasn't his style and only did it for commission money.</p>
            <div class="fun-fact">Bobo Comics distanced himself after the meme exploded, saying gassy stuff "not my cup of tea" – but the internet never forgets.</div>
        </div>

        <div class="section">
            <h2>Rise to Fame (2022–2023)</h2>
            <p>Cropped SFW clips spread on YouTube (earliest repost June 2021 by "I Like Basset Hounds"). By 2022–2023 it became huge in Soyjak comics, 4chan, Reddit, and Twitter edits. Used in ironic gross-out humor and shock memes. The character got nicknames like "Incredible Gassie" and became a staple for absurd parody content.</p>
            <div class="fun-fact">Early posts called him "the best super from The Incredibles" – pure chaos humor.</div>
        </div>

        <div class="section">
            <h2>2025 Explosion: Viggle AI Era</h2>
            <p>In late 2024–2025, Viggle AI made it viral again. Users rotoscoped hated figures (bad NFL players after losses, celebs, IdkSterling trend starters) into the explicit animation. Called "getting Incredible Gassied" or "Gassassination." NFL fans especially loved roasting underperformers. Videos flooded TikTok, Instagram, Reddit. It merged with brainrot trends and became peak shock/absurdity meme.</p>
            <div class="fun-fact">One blast = instant humiliation. No villain stands a chance against the green gas.</div>
        </div>

        <div class="section">
            <h2>Chat – Let It Rip</h2>
            <div class="chat-container" id="chat-box"></div>
            <form id="chat-form" class="mt-4">
                <div class="input-group input-group-lg">
                    <input type="text" id="chat-input" class="form-control" placeholder="Gassy thoughts go here...">
                    <button type="submit" class="btn btn-success px-5">Blast</button>
                </div>
            </form>
        </div>
    </div>

    <footer>Atomic vibes only • Gassytown 2026</footer>

    <!-- Fart sound -->
    <audio id="fart-sound" preload="auto">
        <source src="https://www.soundjay.com/human/sounds/fart-01.mp3" type="audio/mpeg">
        <source src="https://www.soundjay.com/human/sounds/fart-02.mp3" type="audio/mpeg">
    </audio>

    <script>
        // Particles
        particlesJS('particles-js', {
            particles: {
                number: {value: 120},
                color: {value: '#4caf50'},
                opacity: {value: 0.7, random: true},
                size: {value: 6, random: true},
                move: {enable: true, speed: 3.5, random: true}
            },
            interactivity: {events: {onhover: {enable: true, mode: 'repulse'}}}
        });

        // Chat
        const socket = io();
        socket.on('message', msg => {
            const box = document.getElementById('chat-box');
            const div = document.createElement('div');
            div.className = 'chat-message';
            div.textContent = msg;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        });
        document.getElementById('chat-form').addEventListener('submit', e => {
            e.preventDefault();
            const input = document.getElementById('chat-input');
            if (input.value.trim()) {
                socket.emit('message', input.value.trim());
                input.value = '';
            }
        });

        // Big picture chaos
        const bigPic = document.getElementById('gassy-big');
        const overlay = document.getElementById('chaos-overlay');
        const sound = document.getElementById('fart-sound');
        let unlocked = false;

        document.body.addEventListener('click', () => {
            if (!unlocked) {
                sound.play().catch(() => {});
                sound.pause();
                unlocked = true;
            }
        }, {once: true});

        bigPic.addEventListener('click', () => {
            sound.currentTime = 0;
            sound.play().catch(() => {});

            // Chaos mode
            overlay.classList.add('chaos-active');

            // Random flying/rotating/bouncing – simple CSS chaos
            document.querySelectorAll('.container, h1, .section, footer, #gassy-big').forEach(el => {
                el.style.position = 'relative';
                el.style.transition = 'all 5s ease';
                el.style.transform = `translate(${Math.random()*800-400}px, ${Math.random()*600-300}px) rotate(${Math.random()*720-360}deg) scale(${Math.random()*1.5 + 0.5})`;
            });

            setTimeout(() => {
                // Black screen with final gassy pic
                document.body.style.background = 'black';
                document.body.innerHTML = '<img src="https://i.kym-cdn.com/entries/icons/original/000/044/286/igassycover.jpg" style="position:fixed; inset:0; margin:auto; max-width:90%; max-height:90%; border-radius:20px; box-shadow:0 0 50px #0f0; cursor:pointer;">' +
                                          '<p style="position:fixed; bottom:20px; left:0; right:0; text-align:center; color:#0f0; font-size:2rem;">Click to escape Gassytown</p>';

                document.body.querySelector('img').addEventListener('click', () => {
                    window.location.href = 'about:blank';  // "removes" you / blank page
                });
            }, 5000);
        });

        // Scroll reveals
        const observer = new IntersectionObserver(entries => {
            entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
        });
        document.querySelectorAll('.section').forEach(s => observer.observe(s));
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
@app.route('/gassytown')
def home():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('message')
def handle_message(msg):
    messages.append(msg)
    emit('message', msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)