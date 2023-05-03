import requests
import re
import envparse

github_token = envparse.env("GITHUB_TOKEN")


headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": github_token,
    "X-GitHub-Api-Version": "2022-11-28"
}

url = "https://api.github.com/repos/prometheus/prometheus/releases?per_page=50"

response = requests.get(url, headers=headers)

data = response.json()

for release in data:
    tag_name = release['tag_name']
    if not bool(re.search('rc', tag_name)): # Ignore tag rc (release candidate)
        print(tag_name)
    # print(f"name: {release['name']}")
    # print(f"tag name: {release['tag_name']}")

# https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28   #list-releases-for-a-repository
