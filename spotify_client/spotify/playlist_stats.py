from spotify_client.spotify.utils import authenticated_request
from spotify_client.settings import spotify_settings
from spotify_client.models import PlaylistStats


def get_playlist_stats() -> PlaylistStats:
    """Fetch stats from the playlist, as a PlaylistStats object"""
    playlist_id = spotify_settings.get_required("playlist_id")
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    r = authenticated_request("GET", url)
    js = r.json()

    followers = js["followers"]["total"]
    songs = js["tracks"]["total"]

    return PlaylistStats(followers=followers, songs=songs)
