import os
import yaml
import github_releases
import logging

from flask import Flask, request, render_template, send_file, send_from_directory, url_for
# from image_generator import generate_image
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

def _fetch_result_yaml():
    """Fetch result.yaml"""
    with open("result.yaml", 'r') as stream:
        try:
            result_yaml = yaml.safe_load(stream)
            # print(result_yaml)
        except yaml.YAMLError as exc:
            logging.error(f"YAML error in result.yaml {exc}")
            return {}
    return result_yaml


@app.route('/', methods=['GET'])
def index():
    try:
        context = _fetch_result_yaml()['services']
    except:
        context = {}
    return render_template('index.html', context=context)


@app.route('/config', methods=['GET'])
def config():
    try:
        context = github_releases.fetch_config_yaml()
        context = context['services']
    except:
        context = {}
    return render_template('config.html', context=context)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        github_releases.generate_result_yaml()
        logging.info("Generate result.yaml")
    try:
        context = _fetch_result_yaml()['services']
    except:
        context = {}
    return render_template('result.html', context=context)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)