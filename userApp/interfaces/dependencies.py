# -*- coding: utf-8 -*-
from flask import send_from_directory
from userApp import userApp
import os
import config


@userApp.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(os.path.join(config.config['TEMPLATES']['template_folder'], 'static/css'), path)


@userApp.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(config.config['TEMPLATES']['template_folder'], 'static/js'), path)


@userApp.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(os.path.join(config.config['TEMPLATES']['template_folder'], 'static/imgs'), path)