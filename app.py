from flask import Flask, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")