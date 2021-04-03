import requests

from spotify_client.settings import spotify_settings
from spotify_client.utils import safe_dict


def initial_login():
    """Perform initial login, using the authentication code.
    Save the access and refresh tokens in memory settings."""
    payload = dict(
        grant_type="authorization_code",
        client_id=spotify_settings.client_id,
        client_secret=spotify_settings.client_secret,
        code=spotify_settings.get_required("authorization_code"),
        redirect_uri=spotify_settings.redirect_uri
    )

    r = requests.post("https://accounts.spotify.com/api/token", data=payload)
    if r.status_code >= 400:
        print(f"Initial login failed (status={r.status_code}): {safe_dict(r.json())}")
    r.raise_for_status()

    r = r.json()
    spotify_settings.access_token = r["access_token"]
    spotify_settings.refresh_token = r["refresh_token"]


def acquire_access_token():
    """Acquire a new access token, using the refresh token.
    Save the access token in memory settings."""
    payload = dict(
        grant_type="refresh_token",
        client_id=spotify_settings.client_id,
        client_secret=spotify_settings.client_secret,
        refresh_token=spotify_settings.get_required("refresh_token")
    )

    r = requests.post("https://accounts.spotify.com/api/token", data=payload)
    if r.status_code >= 400:
        print(f"Acquire access token failed (status={r.status_code}): {safe_dict(r.json())}")
    r.raise_for_status()

    r = r.json()
    spotify_settings.access_token = r["access_token"]
