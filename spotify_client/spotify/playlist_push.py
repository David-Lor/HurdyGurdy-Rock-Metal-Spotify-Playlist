from typing import List

from spotify_client.spotify.playlist_pull import pull_playlist
from spotify_client.spotify.utils import authenticated_request
from spotify_client.settings import spotify_settings
from spotify_client.utils import iterate_array_in_chunks


def _add_songs_to_playlist(playlist_id: str, songs_uris: List[str]):
    for songs_uris_chunk in iterate_array_in_chunks(songs_uris, 100):
        body = dict(uris=songs_uris_chunk)
        r = authenticated_request("POST", f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", json=body)
        r.raise_for_status()


def _delete_songs_from_playlist(playlist_id: str, songs_uris: List[str]):
    for songs_uris_chunk in iterate_array_in_chunks(songs_uris, 100):
        body = dict(tracks=[dict(uri=uri) for uri in songs_uris_chunk])
        r = authenticated_request("DELETE", f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", json=body)
        r.raise_for_status()


def push_playlist(songs_uris: List[str]):
    """Push the given songs URIs ("spotify:track:{id}") to the playlist.
    This will make the playlist have the given songs, so they will be removed and appended
    depending on if they currently exist or do not.
    Currently does not support reordering, and new songs will always be appended
    at the end of the playlist but with the same order as defined."""
    playlist_id = spotify_settings.get_required("playlist_id")
    current_playlist = [song.uri for song in pull_playlist()]
    new_songs = [song for song in songs_uris if song not in current_playlist]
    delete_songs = [song for song in current_playlist if song not in songs_uris]

    _delete_songs_from_playlist(playlist_id, delete_songs)
    _add_songs_to_playlist(playlist_id, new_songs)
