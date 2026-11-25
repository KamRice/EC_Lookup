import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    client_id: str
    client_secret: str
    username: str
    password: str
    agency: str
    environment: str
    scope: str
    auth_url: str = "https://auth.accela.com/oauth2/token"
    api_base: str = "https://apis.accela.com/v4"

    # What counts as a Final Elevation Certificate (compared lowercase)
    ec_category: str = "final elevation certificate"
    # Set to "" to skip the group check until you've confirmed its format
    ec_group: str = "BLD"

    # Record types that can carry certificates
    record_types: tuple = (
        "Building/Accessory Structure/NA/NA",
        "Building/Residential/NA/NA",
    )


settings = Settings(
    client_id=_require("ACCELA_CLIENT_ID"),
    client_secret=_require("ACCELA_CLIENT_SECRET"),
    username=_require("ACCELA_USERNAME"),
    password=_require("ACCELA_PASSWORD"),
    agency=_require("ACCELA_AGENCY"),
    environment=_require("ACCELA_ENVIRONMENT"),
    scope=os.getenv("ACCELA_SCOPE", "records documents parcels addresses"),
)