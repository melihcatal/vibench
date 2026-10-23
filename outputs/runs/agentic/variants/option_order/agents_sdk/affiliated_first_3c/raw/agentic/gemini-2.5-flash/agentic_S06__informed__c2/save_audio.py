def save_audio_to_file(audio_content: bytes, output_filepath: str):
    """Writes synthesized speech audio to a local file."""
    try:
        with open(output_filepath, "wb") as out:
            out.write(audio_content)
        return f"Audio content successfully saved to {output_filepath}"
    except IOError as e:
        return f"Error saving audio to file: {e}"

if __name__ == "__main__":
    # Example usage
    dummy_audio_data = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    message = save_audio_to_file(dummy_audio_data, "test_output.mp3")
    print(message)
    import os
    if os.path.exists("test_output.mp3"):
        os.remove("test_output.mp3")
