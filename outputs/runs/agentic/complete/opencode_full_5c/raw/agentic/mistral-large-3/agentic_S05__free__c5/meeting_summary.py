from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient
from google.cloud.aiplatform import Model
from typing import List, Dict, Any


def summarize_meeting_transcript(
    transcript_chunks: List[Dict[str, Any]],
    project_id: str = "your-google-cloud-project",
    location: str = "us-central1",
) -> Dict[str, Any]:
    """Summarizes live meeting transcript chunks using Google Cloud Vertex AI."""
    aiplatform.init(project=project_id, location=location)

    model = Model(
        "projects/{}/locations/{}/models/text-bison@latest".format(project_id, location)
    )
    client = PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )

    full_transcript = " ".join(
        chunk["text"] for chunk in transcript_chunks if chunk["is_final"]
    ).strip()

    if not full_transcript:
        return {"summary": "", "action_items": []}

    prompt = f"Summarize the following meeting transcript and extract action items:\n\n{full_transcript}"

    response = client.predict(
        endpoint=model.resource_name,
        instances=[{"prompt": prompt}],
        parameters={
            "temperature": 0.2,
            "maxDecodeSteps": 1024,
            "topP": 0.8,
            "topK": 40,
        },
    )

    summary = response.predictions[0]["content"]

    action_items_prompt = f"Extract action items from the following meeting transcript:\n\n{full_transcript}"

    action_items_response = client.predict(
        endpoint=model.resource_name,
        instances=[{"prompt": action_items_prompt}],
        parameters={
            "temperature": 0.2,
            "maxDecodeSteps": 1024,
            "topP": 0.8,
            "topK": 40,
        },
    )

    action_items = [
        item.strip()
        for item in action_items_response.predictions[0]["content"].split("\n")
        if item.strip()
    ]

    return {
        "summary": summary,
        "action_items": action_items,
    }
