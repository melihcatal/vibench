from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel
from speech_models import SpeechRecognitionResult
from typing import Iterator, Dict, Any

class MeetingSummarizer:
    def __init__(self, project_id: str, location: str = "us-central1"):
        vertexai.init(project=project_id, location=location)
        self._model = TextGenerationModel.from_pretrained("text-bison")

    def summarize_chunk(self, transcript_chunk: str) -> str:
        if not transcript_chunk:
            return ""
        
        # Vertex AI Generative AI for summarization
        # Using text-bison model, which is good for text generation tasks like summarization.
        prompt = f"Summarize the following meeting transcript chunk: {transcript_chunk}"
        response = self._model.predict(prompt=prompt, temperature=0.2, max_output_tokens=250)
        return response.text

def meeting_summary(transcript_chunks: Iterator[SpeechRecognitionResult], project_id: str) -> Iterator[Dict[str, Any]]:
    summarizer = MeetingSummarizer(project_id)
    combined_transcript = []
    for chunk in transcript_chunks:
        combined_transcript.append(chunk.text)
        if chunk.is_final: # Summarize when a final chunk is received
            full_transcript_segment = " ".join(combined_transcript)
            summary = summarizer.summarize_chunk(full_transcript_segment)
            yield {"summary": summary, "is_final_segment": True}
            combined_transcript = [] # Reset for the next segment
        else:
            yield {"current_transcript_segment": chunk.text, "is_final_segment": False}
