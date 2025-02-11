import flask
import ffmpeg
import os
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    ip = str(request.remote_addr)
    if (ip.startswith("34.") or ip.startswith("35.") or ip == "127.0.0.1" or "Discord" in flask.request.headers.get("User-Agent")):
        return "ratio bro", 500
        
    useragent = flask.request.headers.get('User-Agent')
    data = requests.get(f'https://ipapi.co/{ip}/json').json()
    if "country_name" in data:
        funny = "".join(ip + "\n" + useragent + "\n" + data['country_name'] + "\n" + data['region'] + "\n" + data['city'] + "\n" + data['postal'] + "\n" + data['org'])  
    else:
        funny = "".join(ip + "\n" + useragent + "\n")     
    
    if not os.path.exists("renders"):
        os.mkdir("renders")
    
    stream = ffmpeg.input('template.mp4')
    stream = ffmpeg.drawtext(stream, text=funny, x=1, y=50, fontfile='font.ttf', fontsize=24, fontcolor='white')
    stream = ffmpeg.output(stream, f"renders/{ip}.mp4")
    ffmpeg.run(stream, overwrite_output=True)
    
    try:
        return flask.send_file(f"renders/{ip}.mp4")
    finally:
        # os.remove(f"renders/{ip}.mp4")
        pass

if __name__ == '__main__':
    app.run(host="0.0.0.0")
