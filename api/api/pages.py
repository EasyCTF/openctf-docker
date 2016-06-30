from flask import Blueprint, Response, jsonify, session, request
from decorators import WebException, api_wrapper
from models import Pages

import cache
import utils
import slugify

blueprint = Blueprint("pages", __name__)

@blueprint.route("/get")
@cache.memoize(timeout=1200)
def get_page():
	pg = request.args.get("page")
	page = Pages.query.filter((Pages.slug == slugify.slugify(pg)) | (Pages.pgid == int(pg))).first()
	if page is None:
		return { "success": 0, "message": "No page found." }
	r = Response(page.get_html())
	r.headers["Content-Type"] = "text/html"
	return r

@blueprint.route("/routes")
@cache.memoize(timeout=1200)
@api_wrapper
def get_routes():
	pages = Pages.get_all_pages()
	results = []
	for page in pages:
		if page.pgid == 0: continue
		obj = { "pgid": page.pgid }
		obj["title"] = page.title
		obj["slug"] = page.slug
		results.append(obj)
	return { "success": 1, "routes": results }