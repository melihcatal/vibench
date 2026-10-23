"""
Local configuration and client helper utilities for Text Content Safety.

Wraps the OpenAI client with moderation-specific helpers and default
configuration for the omni-moderation-latest model.
"""

from __future__ import annotations

import logging
from typing import List, Optional

import openai
from openai import OpenAI

from safety_models import (
    BatchModerationRequest,
    BatchModerationResult,
    ModerationRequest,
    ModerationResult,
    build_openai_moderation_params,
    get_openai_api_key,
    normalize_openai_moderation,
)

logger = logging.getLogger(__name__)

_OPENAI_MODERATION_MODEL = "omni-moderation-latest"


class SafetyClient:
    """Thin wrapper around the OpenAI client focused on content moderation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = _OPENAI_MODERATION_MODEL,
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key or get_openai_api_key()
        self._model = model
        self._client = OpenAI(
            api_key=self._api_key,
            timeout=timeout,
        )

    @property
    def model(self) -> str:
        return self._model

    def moderate_single(self, text: str) -> ModerationResult:
        """Moderate a single piece of text via OpenAI moderation."""
        params = build_openai_moderation_params(text)
        raw = self._client.moderations.create(**params)
        result = raw.results[0] if raw.results else None
        if result is None:
            return ModerationResult(text=text, flagged=False)
        return normalize_openai_moderation(result, text)

    def moderate_batch(
        self, request: BatchModerationRequest
    ) -> BatchModerationResult:
        """Moderate a batch of texts. Sends individual calls for each text."""
        results: List[ModerationResult] = []
        flagged_count = 0
        for text in request.texts:
            try:
                res = self.moderate_single(text)
                results.append(res)
                if res.flagged:
                    flagged_count += 1
            except openai.APIError as exc:
                logger.error(
                    "OpenAI moderation API error for text segment: %s", exc
                )
                results.append(ModerationResult(text=text, flagged=False))

        return BatchModerationResult(
            results=results,
            overall_flagged_count=flagged_count,
            total_texts=len(request.texts),
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        if hasattr(self._client, "close"):
            self._client.close()
