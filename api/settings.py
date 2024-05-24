from functools import lru_cache
from pathlib import Path
from typing import Any, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pytz import timezone

from api.enums import Environment, LogLevel

BASE_PATH = Path(__file__).parent.absolute()
KST = timezone("Asia/Seoul")


def kv_string_to_dict(comma_seperated_data: str) -> dict:
    """
    "key1:value1,key2:value2" -> {"key1": "value1", "key2": "value2"}
    """
    kv_map_list = [
        kv_string.split(":") for kv_string in comma_seperated_data.split(",")
    ]
    return {k: v for k, v in kv_map_list}


class MyCustomSource(EnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        # Examples
        # if field_name == "allowed_services":
        #     return value.split(",")
        # if field_name in ("dust_service_map", "service_auth_map"):
        #     return kv_string_to_dict(value)
        return value


class Settings(BaseSettings):
    """
    Settings for the app.
    """

    environment: Environment = Environment.TEST
    loglevel: LogLevel = LogLevel.DEBUG
    enable_cors: bool = True
    cors_origins: str = ""
    data_api_token: str = ""
    mongo_host: str = "mongodb"
    mongo_port: int = 27017
    mongo_username: str | None = None
    mongo_password: str | None = None
    mongo_db: str = "nolzapan"
    mongo_auth_source: str | None = None

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)

    model_config = SettingsConfigDict(
        env_prefix="nolza_",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns the settings for the app.
    """
    env_ = Settings()
    return env_


env = get_settings()

SERVICE_INFO = {
    "title": "NOLZAPAN",
    "version": "0.0.1",
}
