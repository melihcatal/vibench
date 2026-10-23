from typing import List, Optional, Callable, Awaitable
from dataclasses import dataclass, field

from speech_models import (
    StreamingTranscriptResponse,
    NormalizedTranscript,
    TranscriptType,
    parse_deepgram_response,
    normalize_transcript,
    merge_final_transcripts,
    extract_interim_text,
)


@dataclass
class StreamingSession:
    interim_transcripts: List[NormalizedTranscript] = field(default_factory=list)
    final_transcripts: List[NormalizedTranscript] = field(default_factory=list)
    current_interim: Optional[NormalizedTranscript] = None
    session_id: str = ""
    language: str = "en"


class PartialResultsHandler:
    def __init__(
        self,
        language: str = "en",
        on_interim: Optional[Callable[[NormalizedTranscript], Awaitable[None]]] = None,
        on_final: Optional[Callable[[NormalizedTranscript], Awaitable[None]]] = None,
        on_speech_final: Optional[
            Callable[[List[NormalizedTranscript]], Awaitable[None]]
        ] = None,
    ):
        self.language = language
        self.on_interim = on_interim
        self.on_final = on_final
        self.on_speech_final = on_speech_final
        self.session = StreamingSession(language=language)

    def process_response(
        self, response: StreamingTranscriptResponse
    ) -> List[NormalizedTranscript]:
        normalized = normalize_transcript(response, language=self.language)
        results = []

        for norm in normalized:
            if response.is_final:
                self.session.final_transcripts.append(norm)
                self.session.current_interim = None
                if self.on_final:
                    import asyncio

                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            asyncio.ensure_future(self.on_final(norm))
                    except RuntimeError:
                        pass
            else:
                self.session.current_interim = norm
                self.session.interim_transcripts.append(norm)
                if self.on_interim:
                    import asyncio

                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            asyncio.ensure_future(self.on_interim(norm))
                    except RuntimeError:
                        pass

            results.append(norm)

        if response.speech_final and self.on_speech_final:
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.ensure_future(
                        self.on_speech_final(list(self.session.final_transcripts))
                    )
            except RuntimeError:
                pass

        return results

    def get_current_interim_text(self) -> str:
        if self.session.current_interim:
            return self.session.current_interim.text
        return ""

    def get_final_merged_text(self) -> str:
        return merge_final_transcripts(self.session.final_transcripts)

    def get_all_final_transcripts(self) -> List[NormalizedTranscript]:
        return list(self.session.final_transcripts)

    def reset_session(self):
        self.session = StreamingSession(language=self.language)


def create_interim_callback(
    handler: Callable[[str], None],
) -> Callable[[NormalizedTranscript], Awaitable[None]]:
    async def _callback(transcript: NormalizedTranscript):
        handler(transcript.text)

    return _callback


def create_final_callback(
    handler: Callable[[str], None],
) -> Callable[[NormalizedTranscript], Awaitable[None]]:
    async def _callback(transcript: NormalizedTranscript):
        handler(transcript.text)

    return _callback
