"""Thin async client for the official Clash Royale API."""

from urllib.parse import quote

import httpx

# Player tags only ever use these characters.
VALID_TAG_CHARS = set("0289PYLQGRJCUV")


class InvalidTag(ValueError):
    pass


class PlayerNotFound(Exception):
    pass


class ApiError(Exception):
    pass


def normalize_tag(raw: str) -> str:
    """Turn user input like ' pv20q9qq8 ' or '#PV2OQ9QQ8' into '#PV20Q9QQ8'."""
    tag = raw.strip().upper().lstrip("#").replace("O", "0")
    if not 3 <= len(tag) <= 12 or any(c not in VALID_TAG_CHARS for c in tag):
        raise InvalidTag(raw)
    return "#" + tag


class ClashClient:
    def __init__(self, api_key: str, base_url: str):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
            timeout=15,
        )

    async def _get(self, path: str):
        try:
            resp = await self._client.get(path)
        except httpx.HTTPError as e:
            raise ApiError(f"Could not reach the Clash Royale API: {e}") from e

        if resp.status_code == 404:
            raise PlayerNotFound(path)
        if resp.status_code == 403:
            raise ApiError("The API key was rejected (403). Check the key and that your IP is whitelisted.")
        if resp.status_code == 429:
            raise ApiError("Too many requests to the Clash Royale API. Try again in a minute.")
        if resp.status_code == 503:
            raise ApiError("The Clash Royale API is down for maintenance. Try again later.")
        if resp.status_code >= 400:
            raise ApiError(f"Clash Royale API error {resp.status_code}: {resp.text[:200]}")
        return resp.json()

    async def get_player(self, tag: str) -> dict:
        return await self._get(f"/players/{quote(tag)}")

    async def get_battlelog(self, tag: str) -> list:
        return await self._get(f"/players/{quote(tag)}/battlelog")

    async def get_upcoming_chests(self, tag: str) -> list:
        return (await self._get(f"/players/{quote(tag)}/upcomingchests")).get("items", [])

    async def aclose(self):
        await self._client.aclose()
