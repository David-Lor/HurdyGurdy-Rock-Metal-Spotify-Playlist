import sys
from typing import List

from spotify_client.spotify.playlist_pull import pull_playlist
from spotify_client.spotify.playlist_push import push_playlist
from spotify_client.spotify.authentication import initial_login, acquire_access_token
from spotify_client.persistence import save_refresh_token, save_playlist, load_playlist
from spotify_client.models import SongInRepo


def login():
    """Perform initial login, to save the refresh token in a file."""
    initial_login()
    save_refresh_token()


def pull():
    acquire_access_token()
    pulled_songs = {song.id: song for song in pull_playlist()}
    save_songs: List[SongInRepo] = list()

    try:
        current_songs = {song.id: song for song in load_playlist()}
    except FileNotFoundError:
        current_songs = dict()

    for song_id, pulled_song in pulled_songs.items():
        current_song = current_songs.get(song_id)
        comment = current_song.comment if current_song else None
        save_songs.append(SongInRepo(**pulled_song.dict(), comment=comment))

    save_playlist(save_songs)


def push():
    acquire_access_token()
    local_songs = load_playlist()
    push_playlist([song.uri for song in local_songs])


COMMANDS = {
    "login": login,
    "pull": pull,
    "push": push
}


def main():
    command = sys.argv[-1]
    try:
        COMMANDS[command]()
    except KeyError:
        print("No valid command given!")
        exit(1)
