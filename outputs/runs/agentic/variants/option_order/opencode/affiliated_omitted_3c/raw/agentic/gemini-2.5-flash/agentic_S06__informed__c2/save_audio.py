import os


def save_audio_to_file(audio_bytes: bytes, file_path: str):
    try:
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_bytes)
        # print(f"Audio saved successfully to {file_path}")
    except Exception as e:
        raise IOError(f"Failed to save audio to {file_path}: {e}")


if __name__ == "__main__":
    # Example usage - in a real scenario, audio_bytes would come from synthesis
    sample_audio_bytes = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    output_file = "output_audio.wav"
    # save_audio_to_file(sample_audio_bytes, output_file)
    # if os.path.exists(output_file):
    #     os.remove(output_file)
