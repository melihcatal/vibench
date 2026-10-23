import os

def save_audio(audio_bytes, output_path: str):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved to {output_path}")
