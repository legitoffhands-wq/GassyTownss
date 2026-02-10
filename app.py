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
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>

<style>
body{
margin:0;
background:linear-gradient(135deg,#0d5c0d,#2e8b57,#4caf50,#81c784);
background-size:400% 400%;
animation:bg 20s ease infinite;
font-family:sans-serif;
}

@keyframes bg{
0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}
}

.container{
background:white;
border-radius:30px;
padding:50px;
margin:60px auto;
max-width:1100px;
}

.chat{
height:400px;
overflow:auto;
background:#f5fff5;
padding:20px;
border-radius:20px;
}

.msg{
background:white;
border:2px solid #81c784;
padding:12px;
margin:10px 0;
border-radius:14px;
}
</style>
</head>

<body>

<div class="container">
<h1 class="text-center">Gassytown</h1>

<div class="chat" id="chat"></div>

<fo
