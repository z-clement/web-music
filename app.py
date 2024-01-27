from settings import API_KEY, CLIENT_SECRET
from flask import Flask, redirect, render_template, request, session
import requests

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
