import os
from openai import OpenAI
from speech_models import SummaryRequest, SummaryResponse

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class MeetingSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def summarize(self, request: SummaryRequest) -> SummaryResponse:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
                {"role": "user", "content": f"Summarize the following meeting transcript:\n\n{request.transcript_chunk}"}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return SummaryResponse(summary=summary)