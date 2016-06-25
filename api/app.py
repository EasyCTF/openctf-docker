from flask import Flask

app = Flask(__name__)

@app.route("/api")
def hello_world():
	return "hei im an api"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)