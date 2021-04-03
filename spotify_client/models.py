from typing import List

from pydantic import BaseModel, constr, validator

String = constr(strip_whitespace=True, min_length=1)
StringEmptyable = constr(strip_whitespace=True)


class BaseSong(BaseModel):
    """Base model with common attributes and methods for all Song classes"""
    id: String

    @property
    def uri(self):
        return f"spotify:track:{self.id}"

    @validator("comment", pre=True, check_fields=False)
    def _comment_default(cls, v):
        return v or ""

    @classmethod
    def from_playlist_file_row(cls, row_columns: List[str]):
        kwargs = dict()
        headers = cls.Config.headers
        for i in range(len(headers)):
            column_name = headers[i]
            try:
                column_value = row_columns[i]
                kwargs[column_name] = column_value
            except IndexError:
                pass
        return cls(**kwargs)

    class Config(BaseModel.Config):
        headers: List[str] = []
        validate_assignment = True


class SongNew(BaseSong):
    """New song committed in the playlist file, with basic info (only id and optional comment)"""
    id: String
    comment: StringEmptyable = ""

    class Config(BaseSong.Config):
        headers = ["id", "comment"]
        """Song attributes in the same order as used for columns on playlist file"""


class SongPull(BaseSong):
    """Song read from the Spotify playlist"""
    name: String
    artist: String
    album: String


class SongInRepo(SongPull):
    """Song parsed from or written to the playlist file"""
    comment: StringEmptyable = ""

    class Config(SongPull.Config):
        headers = ["id", "name", "artist", "album", "comment"]
        """Song attributes in the same order as used for columns on playlist file"""

    def to_playlist_file_rows(self):
        return [self.__getattribute__(column_name) for column_name in self.Config.headers]
