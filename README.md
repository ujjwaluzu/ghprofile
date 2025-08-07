# 🧑‍💻 ghprofile
[![PyPI Downloads](https://static.pepy.tech/badge/ghprofile)](https://pepy.tech/projects/ghprofile)

![License](https://img.shields.io/badge/license-MIT-blue.svg)

A lightweight Python library to fetch and summarize a GitHub user's public profile and repository stats, including followers, bio, starred repos, and pinned repositories.

## 🚀 Features

- ✅ Get user bio, followers, and following count  
- ✅ List all public repositories  
- ✅ Count total stars across repositories  
- ✅ Fetch pinned repositories (via scraping)  
- ✅ Custom error handling for failed API calls  
- ✅ Simple to use and extend

## 📦 Installation

```bash
pip install ghprofile
```
## 🔑 Authentication (Optional)
You can pass a GitHub personal access token to increase your rate limits and access private data.

✅ Token is optional

🕒 Without token: ~60 API calls/hour (public data only)

🔐 With token: ~5000 API calls/hour

## 🧑‍💻 Usage
With Token
```bash
from ghprofile.core import Ghprofile

gh = Ghprofile("octocat", "your_github_token")

print(gh.get_bio())         # → "A mysterious octocat."
print(gh.get_followers())   # → 5400
print(gh.get_repo())        # → ['hello-world', 'test-repo']
print(gh.get_stars())       # → 42
print(gh.get_pinned_repos())# → ['hello-world', 'octo-repo']
```
Without Token
```bash
from ghprofile.core import Ghprofile

gh = Ghprofile("octocat")
```
## 📁 Project Structure
```bash
ghprofile/
├── core.py          # Main class Ghprofile
├── __init__.py
tests/
├── test_core.py     # Unit tests using pytest
pyproject.toml       # Build and tool config
README.md
```
## 📋 Error Handling
All exceptions are wrapped under a custom exception class:
```bash
from ghprofile.core import GhprofileError

try:
    gh = Ghprofile("unknownuser", "badtoken")
except GhprofileError as e:
    print("Something went wrong:", e)
```
## 🤝 Contributing
Contributions are welcome! If you’d like to:

Add new features (e.g. commit history, language breakdown)
Improve error handling or test coverage
Refactor or optimize the code
Just fork the repo, create a new branch, and open a pull request.
Don't forget to write or update tests for your changes.

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with proper attribution.
