import pytest
from ghprofile.core import Ghprofile, GhprofileError

# Replace with a real username and token for testing
USERNAME = "octocat"
TOKEN = "ghp_exampletoken1234567890"  # Use a valid token when running locally

@pytest.fixture
def client():
    return Ghprofile(USERNAME, TOKEN)

def test_get_bio(client):
    bio = client.get_bio()
    assert isinstance(bio, str)

def test_get_followers(client):
    followers = client.get_followers()
    assert isinstance(followers, int)

def test_get_following(client):
    following = client.get_following()
    assert isinstance(following, int)

def test_get_repo(client):
    repos = client.get_repo()
    assert isinstance(repos, list)

def test_get_stars(client):
    stars = client.get_stars()
    assert isinstance(stars, int)

def test_get_pinned_repos(client):
    pinned = client.get_pinned_repos()
    assert isinstance(pinned, list) or isinstance(pinned, str)

def test_invalid_user():
    with pytest.raises(GhprofileError):
        Ghprofile("invalidusername999999999999", TOKEN)
