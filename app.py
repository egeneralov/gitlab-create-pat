#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from flask import Flask, Response, jsonify, request
from gitlab import GitlabCreatePAT


logging.basicConfig(
  **{
    'level': logging.DEBUG,
    'format': '{"time": "%(asctime)s", "filename":"%(filename)s", "line":"%(lineno)d", "level":"%(levelname)s", "message": "%(message)s"}',
  },
  handlers = [
#    logging.FileHandler(filename='{}/history.log'.format(base_dir)),
    logging.StreamHandler(sys.stdout)
  ]
)


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def ok():
  with open('README.md') as f:
    return f.read()


@app.route('/', methods = ['POST'])
def proceed():
  try:
    payload = request.get_json(force=True)
  except Exception as e:
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e),
        "message": "payload"
      }), 400

  config = {
    "name": "",
    "expires_at": "2020-08-27",
    "endpoint": "http://gitlab.com",
    "login": "",
    "password": "",
    "scopes": {
      'personal_access_token[scopes][]': [
        'api',
        'sudo',
        'read_user',
        'read_repository'
      ]
    }
  }

  try:
    config.update(**payload)
  except Exception as e:
    return jsonify({
        "ok": False,
        "result": None,
        "error": str(e),
        "message": "config.update"
      }), 400

#   try:
  some = GitlabCreatePAT(**config)
  return jsonify({
      "ok": False,
      "result": some.token,
      "error": None
    }), 200
#   except Exception as e:
#     print(e)
#     print(dir(e))
#     return jsonify({
#         "ok": False,
#         "result": None,
#         "error": str(e),
#         "message": "GitlabCreatePAT"
#       }), 500


if __name__ == '__main__':
  os.environ['PYTHONHTTPSVERIFY'] = '0'
  app.run(
    host = '0.0.0.0',
    port = os.environ.get('PORT', '8080'),
    debug = False
)


