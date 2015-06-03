#!/usr/bin/python

from flask import Flask

app = Flask(__name__)


@app.route("/report/<userKey>/<node>", methods=['POST'])
def nodeReport(userKey, node):
    return "Hello World!" + userKey + node + "\n"

if __name__ == "__main__":
    app.run()
