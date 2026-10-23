from typing import Iterable, List

from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel


class MeetingSummaryGenerator:
    def __init__(self, project_id: str, location: str = 'us-central1', model_name: str = 'gemini-1.5-flash-002') -> None:
        self.project_id = project_id
        self.location = location
        self.model = GenerativeModel(model_name)

    def summarize(self, transcript_chunks: Iterable[str]) -> str:
        prompt = 'Summarize the meeting in bullet points, including decisions, action items, and risks.\n\n' + '\n'.join(transcript_chunks)
        response = self.model.generate_content(prompt)
        return getattr(response, 'text', '')

