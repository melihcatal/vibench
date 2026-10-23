def save_audio_to_file(audio_content: bytes, filename: str):
    """Saves audio content (bytes) to a local file."""
    try:
        with open(filename, "wb") as f:
            f.write(audio_content)
        print(f"Audio successfully saved to {filename}")
    except IOError as e:
        print(f"Error saving audio to {filename}: {e}")

if __name__ == "__main__":
    # Example usage (requires dummy audio content)
    dummy_audio = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    output_filename = "test_output.mp3"
    save_audio_to_file(dummy_audio, output_filename)
    import os
    if os.path.exists(output_filename):
        print(f"File {output_filename} exists with size {os.path.getsize(output_filename)} bytes.")
        os.remove(output_filename)
        print(f"Cleaned up {output_filename}.")
