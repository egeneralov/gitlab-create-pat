#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import argparse
import logging

from urllib.parse import urljoin
from bs4 import BeautifulSoup


class GitlabCreatePAT:

  def __init__(self, **kwargs):
    logging.debug('Recived: {}'.format(kwargs))
    self.__dict__.update(**kwargs)
    self.root_route = urljoin(self.endpoint, "/")
    self.sign_in_route = urljoin(self.endpoint, "/users/sign_in")
    self.pat_route = urljoin(self.endpoint, "/profile/personal_access_tokens")

    self.obtain_csrf_token()
    self.sign_in()
    self.obtain_personal_access_token()


  def find_csrf_token(self, text):
    logging.debug('find_csrf_token: {}'.format(text))
    soup = BeautifulSoup(text, "lxml")
    logging.debug('recived soup')
    token = soup.find(attrs={"name": "csrf-token"})
    logging.debug('token: {}'.format(token))
    param = soup.find(attrs={"name": "csrf-param"})
    logging.debug('param: {}'.format(param))
    data = {param.get("content"): token.get("content")}
    logging.debug('data: {}'.format(data))
    return data


  def obtain_csrf_token(self):
    logging.debug('obtain_csrf_token')
    r = requests.get(self.root_route)
    self.csrf1 = self.find_csrf_token(r.text)
    self.cookies1 = r.cookies



  def sign_in(self):
    logging.debug('sign_in')
    data = {
      "user[login]": self.login,
      "user[password]": self.password,
      "user[remember_me]": 0,
      "utf8": "✓"
    }
    data.update(self.csrf1)
    logging.debug('data: {}'.format(data))
    r = requests.post(
      self.sign_in_route,
      data = data,
      cookies = self.cookies1
    )
    self.cookies2 = r.history[0].cookies
    logging.debug('cookies2: {}'.format(self.cookies2))
    self.csrf2 = self.find_csrf_token(r.text)
    logging.debug('csrf2: {}'.format(self.csrf2))


  def obtain_personal_access_token(self):
    logging.debug('obtain_personal_access_token')
    data = {
      "personal_access_token[expires_at]": self.expires_at,
      "personal_access_token[name]": self.name,
      "utf8": "✓"
    }
    data.update(self.scopes)
    data.update(self.csrf2)
    logging.debug('data: {}'.format(data))
    r = requests.post(
      self.pat_route,
      data = data,
      cookies = self.cookies2
    )
    soup = BeautifulSoup(r.text, "lxml")
    logging.debug('soup: {}'.format(data))
    self.token = soup.find('input', id='created-personal-access-token').get('value')
    logging.debug('token: {}'.format(self.token))



if __name__ == "__main__":
  config = {
    "name": "terraform",
    "expires_at": "2020-08-27",
    "endpoint": "http://209.97.130.234.xip.io",
    "login": "root",
    "password": "egeneralov",
    "scopes": {
      'personal_access_token[scopes][]': [
        'api',
        'sudo',
        'read_user',
        'read_repository'
      ]
    }
  }
  logging.debug('config: {}'.format(config))
  some = GitlabCreatePAT(**config)
  print(some.token)
