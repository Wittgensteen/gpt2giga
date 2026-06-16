"""GigaChat provider client helpers."""

import os
from typing import Any, Dict

import httpx

from gigachat import GigaChat

from gpt2giga.providers.gigachat.types import SupportsAclose

# Custom headers injected into every GigaChat HTTP request.
# Set GIGACHAT_HEADER_X_IDENTIFICATION_SYSTEM="" to disable a header.
_CUSTOM_HEADER_DEFS: Dict[str, str] = {
    "x-identification-system": os.getenv("GIGACHAT_X_IDENTIFICATION_SYSTEM", "csp_lab"),
    "x-identification-module": os.getenv(
        "GIGACHAT_X_IDENTIFICATION_MODULE", "csp_lab_antifraud_edge"
    ),
}
CUSTOM_HEADERS: Dict[str, str] = {
    k: v for k, v in _CUSTOM_HEADER_DEFS.items() if v
}


def _inject_custom_headers(client: httpx.Client | httpx.AsyncClient | None) -> None:
    if client is None or not CUSTOM_HEADERS:
        return
    client.headers.update(CUSTOM_HEADERS)


def create_gigachat_client(settings: Any) -> GigaChat:
    """Create a GigaChat SDK client from settings."""
    client = GigaChat(**settings.model_dump())
    # Force creation of the lazy httpx client instances and inject custom headers.
    _inject_custom_headers(client._client)
    _inject_custom_headers(getattr(client, "_aclient", None))
    return client


async def close_gigachat_client(client: SupportsAclose | None, logger: Any) -> None:
    """Close a GigaChat SDK client without failing application shutdown."""
    if client is None:
        return
    try:
        await client.aclose()
        logger.info("GigaChat client closed")
    except Exception as exc:
        logger.warning(f"Error closing GigaChat client: {exc}")
