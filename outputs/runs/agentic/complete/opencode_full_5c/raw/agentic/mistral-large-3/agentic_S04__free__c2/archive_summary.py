from google.cloud import aiplatform
from speech_models import TranscriptionResult
import os


def archive_summary(transcript: TranscriptionResult) -> str:
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    prompt = f"Summarize the following transcript:\n\n"
    for segment in transcript.segments:
        prompt += f"{segment.text}\n"

    model = aiplatform.TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        prompt, max_output_tokens=1024, temperature=0.2, top_k=40, top_p=0.8
    )

    return response.text
