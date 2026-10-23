import assemblyai
import os

def submit_transcription(audio_file_path):
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    # AssemblyAI API Key - it is recommended to store this in an environment variable
    # For example: export ASSEMBLYAI_API_KEY="YOUR_ASSEMBLYAI_API_KEY"
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    # Initialize the AssemblyAI transcriber
    transcriber = assemblyai.Transcriber(api_key)

    # Submit the audio file for transcription
    print(f"Submitting {audio_file_path} for transcription...")
    config = assemblyai.TranscriptionConfig(language_code="en_us")
    transcript = transcriber.transcribe(audio_file_path, config=config)

    if transcript.status == assemblyai.TranscriptStatus.error:
        print(f"Transcription failed: {transcript.error}")
    else:
        print("Transcription successful!")
        print(f"Transcript ID: {transcript.id}")
        print(f"Text: {transcript.text}")
        return transcript

if __name__ == "__main__":
    # Example usage:
    # Replace "path/to/your/audio.wav" with the actual path to your audio file
    # Ensure you have the ASSEMBLYAI_API_KEY environment variable set
    try:
        # Placeholder for an actual audio file path.
        # For a real run, replace this with a valid path to an audio file.
        # For demonstration purposes, we'll use a non-existent file to show the flow.
        audio_file = "path/to/your/audio.wav"
        # To run this, you would typically upload an audio file to a URL
        # or provide a local path if the AssemblyAI SDK supports direct file upload for batch.
        # For simplicity, we are assuming direct file path for now.
        # In a real scenario, you might upload to S3 or similar and provide a URL.

        # For a simple test without an actual file, one might mock the transcriber or
        # catch the file not found error. This example assumes a file will be provided.

        # In a true batch transcription scenario, you might pass a URL to an audio file
        # AssemblyAI's SDK also accepts local file paths which it uploads
        # Let's assume `audio_file` is a local path.
        
        # NOTE: This example will likely fail if "path/to/your/audio.wav" does not exist.
        # For a working example, replace "path/to/your/audio.wav" with an actual audio file path
        # and ensure ASSEMBLYAI_API_KEY is set.

        # To prevent immediate FileNotFoundError for this general example,
        # we will simulate success if file doesn't exist to demonstrate the API call structure.
        # In a real application, you'd handle the file existence explicitly.
        
        if not os.path.exists(audio_file):
            print(f"Warning: Audio file '{audio_file}' not found. "
                  "Please replace with a valid audio file path and set ASSEMBLYAI_API_KEY "
                  "to run this example successfully.")
            # We won't call submit_transcription if the file doesn't exist for a cleaner demo.
        else:
            submit_transcription(audio_file)

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
