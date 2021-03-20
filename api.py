from flask import Blueprint, jsonify, make_response, abort, redirect
from datetime import date, timedelta, datetime
from db_init import *


api_blueprint = Blueprint("api", __name__,
                          template_folder="templates")
