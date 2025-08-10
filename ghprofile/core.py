import requests
from bs4 import BeautifulSoup
class GhprofileError(Exception):
    pass

class Ghprofile:
    api_base = "https://api.github.com/users/"

    def __init__(self, username, token=None):
        self.username = username

        if token:
            self.headers = {
                "Authorization": f"token {token}",
                "User-Agent": "ghprofile-lib"
            }
        else:
            self.headers = {
                "User-Agent": "ghprofile-lib"
            }
       
        try:
            self.api = requests.get(f"{self.api_base}{self.username}", headers=self.headers)
            self.repo_api = requests.get(f"{self.api_base}{self.username}/repos", headers=self.headers)

            if self.api.status_code != 200:
                raise GhprofileError(f"User API request failed: {self.api.status_code}")
            if self.repo_api.status_code != 200:
                raise GhprofileError(f"Repo API request failed: {self.repo_api.status_code}")

            self.api_response = self.api.json()
            self.repo_api_response = self.repo_api.json()
        except requests.exceptions.RequestException as e:
            raise GhprofileError(f"Network error: {e}")

    def get_bio(self):
        bio = self.api_response.get("bio")
        if bio is None:
            return "User has no bio"
        else:
            return bio



    def get_followers(self):
        followers = self.api_response.get("followers", 0)
        return followers


    def get_following(self):
        following = self.api_response.get("following", 0)
        return following



    def get_repo(self):
        l = []

        for i in self.repo_api_response:
            name = i.get("name")
            l.append(name)
        return l



    def get_stars(self):
        total = 0

        for i in self.repo_api_response:
            star = i.get("stargazers_count", 0)
            total += star
        return total



    def get_pinned_repos(self):
        url = f"https://github.com/{self.username}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "Could not fetch pinned repos"

        soup = BeautifulSoup(response.text, "html.parser")
        pinned_items = soup.select("span.repo")

        repos = [item.text.strip() for item in pinned_items]
        return repos if repos else "No pinned repositories"