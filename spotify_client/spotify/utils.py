import requests

from spotify_client.settings import spotify_settings
from spotify_client.utils import safe_dict


def authenticated_request(method, url, **kwargs):
    access_token = spotify_settings.get_required("access_token")
    headers = kwargs.get("headers", {})
    headers["Authorization"] = "Bearer " + access_token
    kwargs["headers"] = headers

    r = requests.request(method, url, **kwargs)
    if r.status_code >= 400:
        print(f"Request failed failed (status={r.status_code}): {safe_dict(r.json())}")
    r.raise_for_status()
    return r
