from dataclasses import dataclass

@dataclass
class TranscriptResult:
    text: str
    is_final: bool
    language: str = ""
    offset_ms: int = 0
    duration_ms: int = 0

    @classmethod
    def from_speech_sdk_result(cls, sdk_result, is_final: bool):
        # Azure Speech SDK result objects have .text and can have other properties
        # For simplicity, we'll just capture text and final status here.
        # More advanced scenarios might parse .json for detailed timing, etc.
        return cls(
            text=sdk_result.text,
            is_final=is_final,
            # language=sdk_result.language # Not directly available on all results in a simple way
            # offset_ms=sdk_result.offset / 10000, # Ticks to ms
            # duration_ms=sdk_result.duration / 10000 # Ticks to ms
        )
