from flask import current_app as app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import random
import string

__check_email_format = lambda email: re.match(".+@.+\..{2,}", email) is not None
__check_ascii = lambda s: all(c in string.printable for c in s)
__check_alphanumeric = lambda s: all(c in string.digits + string.ascii_uppercase + string.ascii_lowercase for c in s)

def isoformat(seconds):
	return datetime.datetime.fromtimestamp(seconds).isoformat() + "Z"

def unix_time_seconds(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt - epoch).total_seconds()

def get_time_since_epoch():
	return unix_time_seconds(datetime.datetime.now())

def hash_password(s):
	return generate_password_hash(s)

def check_password(hashed_password, try_password):
	return check_password_hash(hashed_password, try_password)

def generate_string(length=32, alpha=string.hexdigits):
	return "".join([random.choice(alpha) for x in range(length)])
