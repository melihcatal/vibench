from openai import OpenAI

from speech_models import normalize_text


class MeetingSummaryService:
    def __init__(self) -> None:
        self._client = OpenAI()

    def summarize(self, transcript_chunks: list[str]) -> str:
        text = normalize_text(" \n".join(chunk for chunk in transcript_chunks if chunk))
        if not text:
            return ""
        response = self._client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": "Summarize the live meeting transcript chunks into concise bullets."},
                {"role": "user", "content": text},
            ],
        )
        return normalize_text(response.output_text)

