import os

def save_audio_to_file(audio_content: bytes, file_path: str):
    """Writes synthesized speech audio bytes to a local file.
    
    Args:
        audio_content: The raw audio bytes from a text-to-speech service.
        file_path: The full path to the output audio file (e.g., "output.mp3").
    """
    try:
        with open(file_path, "wb") as out_file:
            out_file.write(audio_content)
        print(f"Audio content successfully written to {file_path}")
    except IOError as e:
        print(f"Error writing audio content to file {file_path}: {e}")

if __name__ == '__main__':
    # This is an example of how you might use this function
    # In a real scenario, audio_content would come from a TTS service call.
    
    # Example dummy audio content (replace with actual TTS output)
    dummy_audio_bytes = b"\x49\x44\x33\x03\x00\x00\x00\x00\x00\x0F\x00\x00\x00\x00\x00\x01" \
                        b"This is dummy audio data."
                        
    output_filename = "example_output.mp3"
    save_audio_to_file(dummy_audio_bytes, output_filename)
    
    # You could integrate it like this:
    # from synthesize_text import synthesize_text_to_audio
    # text_to_synthesize = "This is a real example saving audio."
    # real_audio_content = synthesize_text_to_audio(text_to_synthesize)
    # save_audio_to_file(real_audio_content, "real_output.mp3")
