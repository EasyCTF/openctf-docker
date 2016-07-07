from flask import Blueprint, jsonify, request
from flask import current_app as app
from decorators import admins_only, api_wrapper, WebException
from models import db, Config, Problems, Teams, Users, UserActivity
from schemas import verify_to_schema, check
from operator import itemgetter

import logger
import problem
import team
import user
import utils

blueprint = Blueprint("admin", __name__)

@blueprint.route("/setup/init")
@api_wrapper
def admin_setup_init():
	if utils.is_setup_complete(): raise WebException("Setup has already been complete.")

	verification = Config("setup_verification", utils.generate_string().lower())
	with app.app_context():
		for item in Config.query.filter_by(key="setup_verification").all():
			db.session.delete(item)
		db.session.add(verification)
		db.session.commit()

		db.session.close()
	return { "success": 1 }

@blueprint.route("/setup", methods=["POST"])
@api_wrapper
def admin_setup():
	global user
	params = utils.flat_multi(request.form)
	if utils.is_setup_complete(): raise WebException("Setup has already been complete.")

	if params.get("verification") != Config.query.filter_by(key="setup_verification").first().value:
		raise WebException("Verification does not match.")

	if params.get("password") != params.get("password_confirm"):
		raise WebException("Passwords do not match.")
	verify_to_schema(user.UserSchema, params)

	name = params.get("name")
	email = params.get("email")
	username = params.get("username")
	password = params.get("password")
	password_confirm = params.get("password_confirm")
	utype = int(params.get("type"))

	setup_vars = [
		Config("ctf_name", params.get("ctf_name")),
		Config("start_time", params.get("start_time")),
		Config("end_time", params.get("end_time")),
		Config("team_size", params.get("team_size")),
		Config("stylesheet", "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"),
		Config("setup_complete", True)
	]

	_user = Users(name, username, email, password, utype=utype, admin=True)
	with app.app_context():
		for var in setup_vars:
			db.session.add(var)

		db.session.add(_user)
		db.session.commit()
		join_activity = UserActivity(_user.uid, 0)
		db.session.add(join_activity)
		db.session.commit()

		db.session.close()

	logger.log(__name__, "%s registered with %s" % (name.encode("utf-8"), email.encode("utf-8")))
	user.login_user(username, password)

	return { "success": 1, "message": "Success!" }

@blueprint.route("/stats/overview")
@api_wrapper
@admins_only
def admin_stats_overview():
	overview = { }
	overview["num_users"] = user.num_users(), user.num_users(include_observers=True)
	overview["num_teams"] = team.num_teams(), team.num_teams(include_observers=True)
	overview["num_problems"] = problem.num_problems()

	return { "success": 1, "overview": overview }

@blueprint.route("/settings")
@api_wrapper
@admins_only
def admin_settings():
	return { "success": 1, "settings": get_settings() }

@blueprint.route("/settings/update", methods=["POST"])
@api_wrapper
@admins_only
def admin_settings_update():
	params = utils.flat_multi(request.form)
	params.pop("csrf_token")
	with app.app_context():
		for key in params:
			config = Config.query.filter_by(key=key).first()
			new = params[key]
			if config.value != new:
				config.value = params[key]
				db.session.add(config)
		db.session.commit()

	return { "success": 1, "message": "Success!" }

@blueprint.route("/teams/overview")
@api_wrapper
@admins_only
def admin_team_overview():
	teams_return = []
	teams = Teams.query.all()
	for _team in teams:
		teams_return.append(_team.get_info())
	teams_return.sort(key=itemgetter("points"), reverse=True)
	return { "success": 1, "teams": teams_return }

@blueprint.route("/info")
@api_wrapper
def admin_info():
	settings = get_settings()
	result = { }
	if "start_time" in settings: result["start_time"] = settings["start_time"]
	if "end_time" in settings: result["end_time"] = settings["end_time"]
	if "team_size" in settings: result["team_size"] = settings["team_size"]
	if "stylesheet" in settings: result["stylesheet"] = settings["stylesheet"]
	return { "success": 1, "info": result }

def get_settings():
	settings_return = {}
	settings = Config.query.all()
	for setting in settings:
		settings_return[setting.key] = setting.value
	return settings_return
