from collections import Counter
from typing import List, Optional

from spotify_client.spotify.utils import authenticated_request
from spotify_client.models import SongPull
from spotify_client.settings import spotify_settings


def _parse_track(track_data: dict) -> SongPull:
    return SongPull(
        id=track_data["id"],
        artist=track_data["artists"][0]["name"],
        album=track_data["album"]["name"],
        name=track_data["name"],
        total_seconds=int(track_data["duration_ms"] / 1000)
    )


def _detect_duplicates(songs: List[SongPull]):
    """Detect repeated songs on the given list of SongPull objects. Duplicates are detected from the songs IDs.
    If any repeated track is found, log all the repeated songs and exit the application with exitcode 1."""
    songs_counter = Counter([song.id for song in songs])
    repeated_ids = {song_id: song_count for song_id, song_count in songs_counter.items() if song_count > 1}

    if repeated_ids:
        print(f"Found {len(repeated_ids)} repeated songs in playlist:")
        for song_id, song_count in repeated_ids.items():
            print(f"id={song_id} count={song_count}")
        exit(1)


def pull_playlist(detect_duplicates: bool = True) -> List[SongPull]:
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

    if detect_duplicates:
        _detect_duplicates(songs)
    return songs


def get_playlist_total_seconds(songs: Optional[List[SongPull]] = None) -> int:
    """Calculate the total length of the playlist in seconds, as the sum of the length from all the songs in it.
    List of SongPull can be given; if not, the playlist is pulled."""
    if songs is None:
        songs = pull_playlist()

    return sum(song.total_seconds for song in songs)
