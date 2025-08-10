import requests
from bs4 import BeautifulSoup

# Custom exception for Ghprofile-specific errors
class GhprofileError(Exception):
    pass

class Ghprofile:
    # Base GitHub API endpoint for user-related data
    api_base = "https://api.github.com/users/"

    def __init__(self, username, token=None):
        """
        Initialize the Ghprofile instance.

        Args:
            username (str): GitHub username to fetch data for.
            token (str, optional): GitHub Personal Access Token for authenticated requests.
                                   If not provided, requests are unauthenticated.
        """
        self.username = username

        # Set request headers — include Authorization if token is provided
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
            # Fetch user profile data
            self.api = requests.get(f"{self.api_base}{self.username}", headers=self.headers)
            # Fetch user repositories data
            self.repo_api = requests.get(f"{self.api_base}{self.username}/repos", headers=self.headers)

            # Handle non-successful responses
            if self.api.status_code != 200:
                raise GhprofileError(f"User API request failed: {self.api.status_code}")
            if self.repo_api.status_code != 200:
                raise GhprofileError(f"Repo API request failed: {self.repo_api.status_code}")

            # Store JSON responses for later use
            self.api_response = self.api.json()
            self.repo_api_response = self.repo_api.json()

        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            raise GhprofileError(f"Network error: {e}")

    def get_bio(self):
        """
        Get the user's GitHub bio.

        Returns:
            str: Bio text or a default message if not set.
        """
        bio = self.api_response.get("bio")
        if bio is None:
            return "User has no bio"
        else:
            return bio

    def get_followers(self):
        """
        Get the number of followers.

        Returns:
            int: Number of followers.
        """
        followers = self.api_response.get("followers", 0)
        return followers

    def get_following(self):
        """
        Get the number of accounts the user is following.

        Returns:
            int: Number of following accounts.
        """
        following = self.api_response.get("following", 0)
        return following

    def get_repo(self):
        """
        Get a list of repository names.

        Returns:
            list: Repository names owned by the user.
        """
        l = []
        for i in self.repo_api_response:
            name = i.get("name")
            l.append(name)
        return l

    def get_stars(self):
        """
        Get the total number of stars across all repositories.

        Returns:
            int: Sum of stargazers_count for all repos.
        """
        total = 0
        for i in self.repo_api_response:
            star = i.get("stargazers_count", 0)
            total += star
        return total

    def get_pinned_repos(self):
        """
        Get a list of pinned repositories by scraping the user's GitHub profile page.

        Returns:
            list or str: List of pinned repository names or an error message.
        """
        url = f"https://github.com/{self.username}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Send GET request to GitHub profile page
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "Could not fetch pinned repos"

        # Parse HTML to find pinned repositories
        soup = BeautifulSoup(response.text, "html.parser")
        pinned_items = soup.select("span.repo")

        # Extract repo names and return them
        repos = [item.text.strip() for item in pinned_items]
        return repos if repos else "No pinned repositories"
