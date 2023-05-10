import logging

import yaml
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

import github_releases


app = Flask(__name__)
bootstrap = Bootstrap5(app)

def _fetch_result_yaml() -> dict:
    """Fetch result.yaml."""
    with open("result.yaml") as stream:
        try:
            result_yaml = yaml.safe_load(stream)
            result_yaml = result_yaml['services']
        except yaml.YAMLError as exc:
            logging.error(f"YAML error in result.yaml {exc}")
            return {}
    return result_yaml


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', context=_fetch_result_yaml())


@app.route('/config', methods=['GET'])
def config():
    try:
        config_yaml = github_releases.fetch_config_yaml()
        config_yaml = config_yaml['services']
    except:
        config_yaml = {}
    return render_template('config.html', context=config_yaml)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        github_releases.generate_result_yaml()
        logging.info("Generate result.yaml")
    return render_template('result.html', context=_fetch_result_yaml())


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)