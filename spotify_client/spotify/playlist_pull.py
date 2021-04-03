from typing import List

from spotify_client.spotify.utils import authenticated_request
from spotify_client.models import SongPull
from spotify_client.settings import spotify_settings


def _parse_track(track_data: dict) -> SongPull:
    return SongPull(
        id=track_data["id"],
        artist=track_data["artists"][0]["name"],
        album=track_data["album"]["name"],
        name=track_data["name"]
    )


def pull_playlist() -> List[SongPull]:
    """Load all the songs existing in the Spotify playlist, as SongPull objects"""
    playlist_id = spotify_settings.get_required("playlist_id")
    songs: List[SongPull] = list()

    next_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    while next_url is not None:
        r = authenticated_request("GET", next_url)
        js = r.json()
        next_url = js.get("next")

        for item in js["items"]:
            track_data = item["track"]
            songs.append(_parse_track(track_data))

    return songs
