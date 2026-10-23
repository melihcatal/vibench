from dataclasses import dataclass


def normalize_caption(text):
    return ' '.join((text or '').strip().split())


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False

    def as_dict(self):
        return {'text': normalize_caption(self.text), 'is_final': self.is_final}


@dataclass
class CaptionRequest:
    language_code: str
    sample_rate_hz: int
    audio_chunks: list


@dataclass
class CaptionResponse:
    text: str
    is_final: bool

    def as_dict(self):
        return {'text': normalize_caption(self.text), 'is_final': self.is_final}
