import json
from typing import List, Dict

from spotify_client.spotify.playlist_pull import get_playlist_total_seconds
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
    total_seconds = get_playlist_total_seconds()

    return PlaylistStats(followers=followers, songs=songs, total_seconds=total_seconds)


def append_stats_to_file(stats: PlaylistStats):
    """Append the given PlaylistStats object to the stats file configured.
    The stats file is an ndjson file, where each line corresponds to the JSON representation
    of a DatedPlaylistStats object, with the stats for a single day."""
    stats_file = general_settings.get_required("playlist_stats_file")
    dated_stats = DatedPlaylistStats(**stats.dict())

    with open(stats_file, "a") as f:  # open file in append mode
        f.write("\n")
        f.write(dated_stats.json())


def load_stats() -> Dict[str, DatedPlaylistStats]:
    """Load the persisted stats from the stats ndjson file, and returns them as dict of {date(str), DatedPlaylistStats} objects,
    returned in the same order as read from the file (considering Python >= 3.6 keeps insertion order on dicts).
    For repeated dates, the last loaded line is used."""
    stats_file = general_settings.get_required("playlist_stats_file")
    parsed_dates_stats: Dict[str, DatedPlaylistStats] = dict()

    with open(stats_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                line_js = json.loads(line)
                line_stats = DatedPlaylistStats(**line_js)
                parsed_dates_stats[line_stats.date] = line_stats
            except:
                # TODO proper except and log
                continue

    return parsed_dates_stats


def export_chart():
    """Load the persisted stats from the stats file, and generate a chart using plotly, exporting it as a picture.
    More info about plotly export and supported output files: https://plotly.com/python/static-image-export/
    """
    import plotly.graph_objects as go
    import pandas as pd

    stats = load_stats()
    chart_file = general_settings.get_required("playlist_chart_file")

    dataframe_followers = dict(date=[], value=[])
    dataframe_songs = dict(date=[], value=[])
    dataframe_duration = dict(date=[], value=[])
    dates_stats = load_stats()

    for date, stats in dates_stats.items():
        dataframe_followers["date"].append(date)
        dataframe_songs["date"].append(date)
        dataframe_followers["value"].append(stats.followers)
        dataframe_songs["value"].append(stats.songs)
        dataframe_duration["date"].append(date)
        dataframe_duration["value"].append(int(stats.total_seconds / 60 / 60))  # duration in hours

    dataframe_followers = pd.DataFrame(dataframe_followers)
    dataframe_songs = pd.DataFrame(dataframe_songs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe_followers["date"], y=dataframe_followers["value"], mode="lines+markers", name="Followers", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=dataframe_songs["date"], y=dataframe_songs["value"], mode="lines+markers", name="Songs", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=dataframe_duration["date"], y=dataframe_duration["value"], mode="lines+markers", name="Length (hours)", line=dict(color="green")))
    fig.write_image(chart_file)
