
import os
from google.cloud import content_safety_v1

def moderate_transcript(text_content: str):
    """
    Moderates transcript text using Google Cloud Content Safety API.
    """
    client = content_safety_v1.ContentSafetyServiceClient()

    # Construct the request.
    request = content_safety_v1.ModerateTextRequest(
        parent=f"projects/{os.environ.get("GOOGLE_CLOUD_PROJECT")}", # GOOGLE_CLOUD_PROJECT should be set in environment variables
        text_content=text_content
    )

    response = client.moderate_text(request=request)

    # You can process the moderation response here.
    # The response will contain information about categories and their scores.
    # For example, to print detected categories:
    for detection in response.moderation_detections:
        print(f"Category: {detection.category}, Likelihood: {detection.sentiment}")
    
    return response

if __name__ == "__main__":
    # Example usage:
    example_transcript = "This is an example transcript with some potentially harmful content like hate speech."
    moderation_result = moderate_transcript(example_transcript)
    print("Moderation complete.")
