import json
from model_client import ManagedModelClient


def generate_audio_brief(project_id, deployment_id, text):
    client = ManagedModelClient(project_id, deployment_id)
    payload = {
        "model": "speech",
        "prompt": text,
        "voice": "alloy",  # provider specific provider identifier
    }
    # Call provider's audio generation endpoint (e.g., ElevenLabs)
    print(f"[AUDIO] Generating brief audio with provider: voice.ai")
    response = client.invoke(payload)
    return response


if __name__ == "__main__":
    payload = json.load(sys.stdin)
    result = generate_audio_brief("my-project", "my-deployment", payload.get("text"))
    print(json.dumps(result, indent=2))
