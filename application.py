# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os

import boto3
import flask
from flask import Response, request

# Default config vals
THEME = "default" if os.environ.get("THEME") is None else os.environ.get("THEME")
FLASK_DEBUG = (
    "false" if os.environ.get("FLASK_DEBUG") is None else os.environ.get("FLASK_DEBUG")
)

# Create the Flask app
application = flask.Flask(__name__)

# Load config values specified above
application.config.from_object("default_config")

# Load configuration vals from a file
application.config.from_envvar("APP_CONFIG", silent=True)

# Only enable Flask debugging if an env var is set to true
application.debug = application.config["FLASK_DEBUG"] in ["true", "True"]

# Region
region = application.config["AWS_REGION"]

# Init DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name=region)

# Init SNS client
sns_client = boto3.client("sns", region_name=region)


@application.route("/")
def welcome():
    theme = application.config["THEME"]
    return flask.render_template(
        "index.html", theme=theme, flask_debug=application.debug
    )


@application.route("/signup", methods=["POST"])
def signup():
    signup_data = dict()
    for item in request.form:
        signup_data[item] = request.form[item]

    try:
        store_in_dynamo(signup_data)
        publish_to_sns(signup_data)
    except Exception as ex:
        logging.error(f"Sign up failed with error: {str(ex)}")
        return Response("", status=409, mimetype="application/json")

    return Response(json.dumps(signup_data), status=201, mimetype="application/json")


def store_in_dynamo(signup_data):
    table = dynamodb.Table(application.config["STARTUP_SIGNUP_TABLE"])
    table.put_item(Item=signup_data)


def publish_to_sns(signup_data):
    sns_client.publish(
        TopicArn=application.config["NEW_SIGNUP_TOPIC"],
        Message="New signup: %s" % signup_data["email"],
    )


if __name__ == "__main__":
    application.run(host="0.0.0.0")
