# platform_brief_audio.py
# [LATER-STEP]
# Generate spoken briefings from platform outputs

from model_client import ManagedModelClient
from model_models import ModelInvocationResponse, BriefAudioRequest, BriefAudioResponse
import base64
import json


# ---------------------------------------------------------------------------
# Helper: call provider's text‑to‑speech (TTS) endpoint
# ---------------------------------------------------------------------------
def generate_speech(text: str) -> bytes:
    """Placeholder for a real TTS API call (e.g., OpenAI's audio service)."""
    client = ManagedModelClient(provider="openai")
    # Pretend the provider returns raw audio bytes
    audio_bytes = client.audio.speech.create(input=text, voice="alloy")
    return audio_bytes


def create_brief(
    invocation: ModelInvocationResponse,
    prompt: str = "Provide a 30‑second spoken summary of the result.",
) -> BriefAudioResponse:
    client = ManagedModelClient(provider="openai")
    # Generate the script using the same model (or a dedicated summarization model)
    script_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"You are a news anchor. Write a 30‑second spoken briefing based on the following output:\n\n{invocation.output_text}\n\nThen speak the text.",
            }
        ],
    )
    script_text = script_resp.choices[0].message.content.strip() if script_resp else ""
    # Convert script to speech
    audio_bytes = generate_speech(script_text)
    # Encode as base64 for easy transport (optional)
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    # Build the response object
    return BriefAudioResponse(
        run_id=invocation.run_id,
        audio_base64=audio_base64,
        original_output=invocation,
    )


@dataclass
class BriefAudioRequest:
    run_id: str
    prompt: str = "Provide a concise spoken summary."

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BriefAudioResponse:
    run_id: str
    audio_base64: str
    original_output: ModelInvocationResponse

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = ModelInvocationResponse(run_id="0", output_text="Today we launched a new feature.", usage=None)
#     audio = create_brief(resp)
#     print(audio.to_dict())
