from typing import List, Union

from pydantic import ValidationError

from spotify_client.models import SongInRepo, SongNew
from spotify_client.settings import general_settings, spotify_settings

PLAYLIST_FILE_DELIMITER = "\t"


def save_refresh_token():
    token = spotify_settings.get_required("refresh_token")
    with open(general_settings.refresh_token_file, "w") as file:
        file.write(token)


def save_playlist(songs: List[SongInRepo]):
    with open(general_settings.playlist_file, "w") as file:
        lines: List[str] = [PLAYLIST_FILE_DELIMITER.join(SongInRepo.Config.headers)]

        for song in songs:
            rows = song.to_playlist_file_rows()
            row_str = PLAYLIST_FILE_DELIMITER.join(rows)
            lines.append(row_str)

        file_content = "\n".join(lines)
        file.write(file_content)


def load_playlist() -> List[Union[SongInRepo, SongNew]]:
    songs = list()
    with open(general_settings.playlist_file, "r") as file:
        for i, line in enumerate(file.readlines()):
            try:
                if i == 0:
                    continue

                chunks = line.strip().split("\t")

                if len(chunks) == 0:
                    continue

                if len(chunks) <= 2:
                    songs.append(SongNew.from_playlist_file_row(chunks))
                    continue

                songs.append(SongInRepo.from_playlist_file_row(chunks))

            except ValidationError:
                print(f"ValidationError on line \"{line}\"")

    return songs
