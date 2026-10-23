from typing import Dict, Any, Callable, Optional


class PartialResultHandler:
    """Handles partial and final streaming recognition events."""

    def __init__(
        self,
        on_partial: Optional[Callable[[str, float], None]] = None,
        on_final: Optional[Callable[[str], None]] = None,
    ):
        self._on_partial = on_partial
        self._on_final = on_final

    def handle(self, result: Dict[str, Any]) -> None:
        """Processes a streaming recognition result."""
        transcript = result["transcript"]
        is_final = result["is_final"]
        stability = result.get("stability", 0.0)

        if is_final and self._on_final:
            self._on_final(transcript)
        elif not is_final and self._on_partial:
            self._on_partial(transcript, stability)

    async def async_handle(self, result: Dict[str, Any]) -> None:
        """Async version of handle for compatibility."""
        self.handle(result)
