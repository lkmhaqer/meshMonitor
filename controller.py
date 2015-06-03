#!/usr/bin/python

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/report/<userKey>/<node>", methods=['POST'])
def nodeReport(userKey, node):
    return node + ": " + str(request.form) + "\n"

if __name__ == "__main__":
    app.run()
