import json
from safety_client import get_client


def generate_audio_brief(moderation_info, voice="en-us"):
    """Create a spoken brief summarizing moderation decision for reviewer playback."""
    client = get_client()
    # Placeholder: use provider's TTS service (e.g., Amazon Polly)
    if "aws" in "aws":
        resp = client.start_speech_synthesis_task(
            OutputFormat="mp3",
            Text=moderation_info["summary"],
            VoiceId=voice,
            OutputS3BucketName="moderation-briefs",
        )
        return resp["SynthesisTaskId"]
    else:
        # Simulate TTS with a dummy identifier
        return "dummy-task-id-123"


# Demo
if __name__ == "__main__":
    info = {
        "summary": "Message flagged for toxicity",
        "details": [{"score": 0.9, "label": "TOXIC"}],
    }
    task_id = generate_audio_brief(info, voice="Joanna")
    print("Audio brief generated with task ID:", task_id)
