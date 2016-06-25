from flask import Flask

app = Flask(__name__)

import api
import config

from api.decorators import api_wrapper

app.config.from_object(config.options)
app.secret_key = config.SECRET_KEY

@app.route("/api")
@api_wrapper
def hello_world():
	return { "success": 1, "message": "The API is apparently functional." }

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)