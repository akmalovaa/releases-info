import datetime
import logging
import re
from pathlib import Path

import envparse
import requests
import yaml


github_token = envparse.env("GITHUB_TOKEN")

headers = {"Accept": "application/vnd.github+json", "Authorization": github_token, "X-GitHub-Api-Version": "2022-11-28"}

result_content = {"services": {}}


def fetch_config_yaml():
    """Fetch config.yaml."""
    with open("config.yaml") as stream:
        try:
            config_yaml = yaml.safe_load(stream)
            logging.debug(f"Read config.yaml {config_yaml}")
        except yaml.YAMLError as exc:
            logging.error(f"YAML error in config.yaml {exc}")
            return {}
    return config_yaml


def _github_date_format(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("%d.%m.%Y")


def _fetch_latest_release(owner, repo):
    url_latest = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url_latest, headers=headers)
    latest = response.json()
    logging.debug(f"latest: {latest['tag_name']} - {latest['published_at']}")
    return latest


def _fetch_all_releases(owner, repo) -> dict:
    url_releases = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100"
    response = requests.get(url_releases, headers=headers)
    releases = response.json()
    releases_dict = {}
    for release in releases:
        tag_name = release["tag_name"]  # Get tag name (release version)
        tag_date = _github_date_format(release["published_at"])  # Convert date format
        if not bool(re.search("rc", tag_name)):  # Ignore tag rc (release candidate)
            releases_dict[tag_name] = tag_date
    logging.debug(f"Releases: {releases_dict}")
    return releases_dict


def _number_of_missed_releases(all_releses, current_tag):
    if current_tag in all_releses:
        releases_list = list(all_releses.keys())
        tag_index = releases_list.index(current_tag)
    else:
        tag_index = "unidentified"
    return tag_index


def _days_of_missed_releases(current_tag_date, latest_tag_date):
    try:
        latest_tag_date = datetime.datetime.strptime(latest_tag_date, "%d.%m.%Y")
        current_tag_date = datetime.datetime.strptime(current_tag_date, "%d.%m.%Y")
        days_delta = (latest_tag_date - current_tag_date).days
    except TypeError:
        days_delta = "unidentified"
    except ValueError:
        days_delta = "unidentified"
    return days_delta


def generate_result_yaml():
    config = fetch_config_yaml()
    for services in config["services"]:
        try:
            logging.info(f"Fetch releases info: {services}")
            github_owner = config["services"][services]["github"]["owner"]
            github_repo = config["services"][services]["github"]["repo"]
            current_tag = config["services"][services]["version"]
            all_releses = _fetch_all_releases(github_owner, github_repo)
            current_tag_date = all_releses.get(current_tag, "unidentified")  # fetch date of current tag
            latest = _fetch_latest_release(github_owner, github_repo)
            latest_tag = latest["tag_name"]
            latest_tag_date = _github_date_format(latest["published_at"])
            latest_tag_url = latest["html_url"]
            missed_releases = _number_of_missed_releases(all_releses, current_tag)
            misser_releases_days = _days_of_missed_releases(current_tag_date, latest_tag_date)
            service_result = {
                "current_tag": current_tag,
                "current_tag_date": current_tag_date,
                "latest_tag": latest_tag,
                "latest_tag_date": latest_tag_date,
                "latest_tag_url": latest_tag_url,
                "missed_releases": missed_releases,
                "missed_releases_days": misser_releases_days,
            }
            result_content["services"][services] = service_result
        except KeyError:
            logging.error(f"Error fetch releases info: {services}")
    result_yaml = Path(__file__).parent / "result.yaml"
    with open(result_yaml, "w", encoding="UTF-8") as result_file:
        yaml.dump(result_content, result_file, sort_keys=False)


if __name__ == "__main__":
    generate_result_yaml()
