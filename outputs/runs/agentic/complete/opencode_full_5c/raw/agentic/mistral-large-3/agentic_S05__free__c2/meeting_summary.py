from google.cloud import aiplatform
from typing import List, Dict, Any
import os


async def meeting_summary(transcript_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    aiplatform.init(project=os.getenv("GOOGLE_PROJECT_ID"), location="us-central1")

    full_transcript = " ".join(
        [chunk["transcript"] for chunk in transcript_chunks if chunk["is_final"]]
    )

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }

    model = aiplatform.TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        prompt=f"Summarize the following meeting transcript:\n\n{full_transcript}",
        **parameters,
    )

    return {
        "summary": response.text,
        "transcript": full_transcript,
    }
