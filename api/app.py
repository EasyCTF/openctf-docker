from flask import Flask, send_file

app = Flask(__name__)
app.config["DEBUG"] = True

import api
import config
import logging
import os

from api.decorators import api_wrapper

app.config.from_object(config.options)
app.secret_key = config.SECRET_KEY

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
	os.makedirs(app.config["UPLOAD_FOLDER"])
if not os.path.exists("pfp"):
	os.makedirs("pfp")

with app.app_context():
	from api.models import db, Config, Users, UserActivity, Teams, Problems, Files, Solves, LoginTokens, TeamInvitations, Tickets, TicketReplies, ProgrammingSubmissions
	db.init_app(app)
	try:
		db.create_all()
	except:
		import traceback
		print traceback.format_exc()
	app.db = db

@app.route("/api")
@api_wrapper
def hello_world():
	return { "success": 1, "message": "The API is apparently functional." }

@app.errorhandler(404)
def page_not_found(e):
	return "You done goofed."

app.register_blueprint(api.activity.blueprint, url_prefix="/api/activity")
app.register_blueprint(api.admin.blueprint, url_prefix="/api/admin")
app.register_blueprint(api.user.blueprint, url_prefix="/api/user")
app.register_blueprint(api.pages.blueprint, url_prefix="/api/pages")
app.register_blueprint(api.problem.blueprint, url_prefix="/api/problem")
app.register_blueprint(api.programming.blueprint, url_prefix="/api/programming")
app.register_blueprint(api.stats.blueprint, url_prefix="/api/stats")
app.register_blueprint(api.team.blueprint, url_prefix="/api/team")
app.register_blueprint(api.tickets.blueprint, url_prefix="/api/tickets")
app.register_blueprint(api.user.blueprint, url_prefix="/api/user")
api.logger.initialize_logs()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)