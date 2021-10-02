from spotify_client.spotify.utils import authenticated_request
from spotify_client.settings import spotify_settings, general_settings
from spotify_client.models import PlaylistStats, DatedPlaylistStats


def get_playlist_stats() -> PlaylistStats:
    """Fetch stats from the playlist, as a PlaylistStats object"""
    playlist_id = spotify_settings.get_required("playlist_id")
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    r = authenticated_request("GET", url)
    js = r.json()

    followers = js["followers"]["total"]
    songs = js["tracks"]["total"]

    return PlaylistStats(followers=followers, songs=songs)


def append_stats_to_file(stats: PlaylistStats):
    """Append the given PlaylistStats object to the stats file configured.
    The stats file is an ndjson file, where each line corresponds to the JSON representation
    of a DatedPlaylistStats object, with the stats for a single day."""
    stats_file = general_settings.get_required("playlist_stats_file")
    dated_stats = DatedPlaylistStats(**stats.dict())

    with open(stats_file, "a") as f:  # open file in append mode
        f.write("\n")
        f.write(dated_stats.json())
