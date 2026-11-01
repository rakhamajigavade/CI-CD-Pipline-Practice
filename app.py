from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = "1.0.0"


@app.route("/")
def home():
    return jsonify({
        "message": "Version 2 - Automatic Deployment Successful !",
        "application": "Jenkins CI/CD Demo",
        "version": APP_VERSION,
        "status": "Running Successfully"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)