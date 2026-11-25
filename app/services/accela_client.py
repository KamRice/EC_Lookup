from urllib.parse import quote

import httpx

from app.config import settings
from app.services.accela_auth import get_token


def _headers(force_refresh: bool = False) -> dict:
    return {
        "Authorization": get_token(force_refresh=force_refresh),
        "x-accela-appid": settings.client_id,
    }


def _get(path: str, params: dict | None = None) -> dict:
    url = f"{settings.api_base}{path}"
    with httpx.Client(timeout=30) as client:
        resp = client.get(url, headers=_headers(), params=params)
        if resp.status_code == 401:  # token rejected: refresh once and retry
            resp = client.get(url, headers=_headers(force_refresh=True), params=params)
    if resp.status_code != 200:
        raise RuntimeError(f"GET {path} failed ({resp.status_code}): {resp.text}")
    return resp.json()


def _get_all(path: str, params: dict | None = None, page_size: int = 100) -> list:
    """Follow limit/offset paging until a short page comes back."""
    params = dict(params or {})
    results, offset = [], 0
    while True:
        params.update({"limit": page_size, "offset": offset})
        page = _get(path, params).get("result", [])
        results.extend(page)
        if len(page) < page_size:
            return results
        offset += page_size


def get_parcel_records(parcel_number: str, types: tuple) -> list:
    params = {
        "types": ",".join(types),
        "fields": "openedDate,customId,updateDate,name,id,type",
    }
    path = f"/parcels/{quote(parcel_number, safe='')}/records"
    return _get_all(path, params)


def get_record_documents(record_id: str) -> list:
    return _get_all(f"/records/{quote(record_id, safe='')}/documents")