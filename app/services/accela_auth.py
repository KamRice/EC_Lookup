import threading
import time

import httpx

from app.config import settings

_lock = threading.Lock()
_token = None
_expires_at = 0.0


def _request_token() -> dict:
    data = {
        "grant_type": "password",
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "username": settings.username,
        "password": settings.password,
        "scope": settings.scope,
        "agency_name": settings.agency,
        "environment": settings.environment,
    }
    resp = httpx.post(settings.auth_url, data=data, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Token request failed ({resp.status_code}): {resp.text}")
    return resp.json()


def get_token(force_refresh: bool = False) -> str:
    """Return a valid token, fetching a new one if missing or near expiry."""
    global _token, _expires_at
    with _lock:
        if force_refresh or _token is None or time.time() > _expires_at - 60:
            payload = _request_token()
            _token = payload["access_token"]
            _expires_at = time.time() + int(payload.get("expires_in", 900))
        return _token