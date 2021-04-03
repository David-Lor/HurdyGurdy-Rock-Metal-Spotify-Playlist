import os
from typing import Optional

import pydantic

ENV_FILE = os.getenv("ENV_FILE", ".env")


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ENV_FILE

    def get_required(self, name):
        value = self.__getattribute__(name)
        if value is None:
            raise KeyError(f"Setting {name} not found or empty; is required!")
        return value


class GeneralSettings(BaseSettings):
    refresh_token_file: Optional[str] = None
    playlist_file: Optional[str] = None


class SpotifySettings(BaseSettings):
    client_id: str
    client_secret: str
    authorization_code: Optional[str] = None
    redirect_uri: str = "http://localhost"
    playlist_id: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    class Config(BaseSettings.Config):
        env_prefix = "SPOTIFY_"


general_settings = GeneralSettings()
spotify_settings = SpotifySettings()
