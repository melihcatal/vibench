from google.cloud import contentsafety_v1
import os

def moderate_transcript(text_content: str):
    # Before running, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file.
    # Example: os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    client = contentsafety_v1.ContentSafetyServiceClient()

    request = contentsafety_v1.ScreenTextRequest(
        # project_id = "your-project-id", # Can be set explicitly or inferred from credentials
        text_content=text_content,
    )

    response = client.screen_text(request=request)

    # The response will contain information about safety attributes like categories and scores.
    # You can process this response to determine if the content is safe.
    return response.safety_ratings
