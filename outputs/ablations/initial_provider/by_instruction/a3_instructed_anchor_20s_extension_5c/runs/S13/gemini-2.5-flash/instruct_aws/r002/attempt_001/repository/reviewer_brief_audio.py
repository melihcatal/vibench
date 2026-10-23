import os
import requests

def reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> dict:
    """
    Generate spoken briefs for moderation reviewers using Eleven Labs API.
    """
    elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice_id

    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key
    }

    data = {
        "text": brief_text,
        "model_id": "eleven_monolingual_v1",  # Or other appropriate Eleven Labs model
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        with open(output_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return {
            "brief_text": brief_text,
            "output_filepath": output_filepath,
            "message": "Audio brief generated successfully."
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to generate audio brief with Eleven Labs API."}
