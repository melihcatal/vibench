import os
import assemblyai

def transcribe_audio_sample(audio_data: bytes) -> str:
    """
    Transcribes a synthesized audio sample to verify its content using AssemblyAI.

    This function is intended for quality assurance (QA) purposes. It takes
    raw audio bytes (e.g., from a TTS synthesis function) and returns the
    transcribed text.

    Requires the ASSEMBLYAI_API_KEY environment variable to be set.

    Args:
        audio_data: The raw bytes of the audio to transcribe.

    Returns:
        The transcribed text as a string.

    Raises:
        ValueError: If the ASSEMBLYAI_API_KEY is not set.
        assemblyai.errors.AssemblyAIError: If the transcription fails.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    assemblyai.settings.api_key = api_key

    try:
        transcriber = assemblyai.Transcriber()
        transcript = transcriber.transcribe(audio_data)

        if transcript.error:
            raise assemblyai.errors.AssemblyAIError(f"Transcription failed: {transcript.error}")

        return transcript.text

    except Exception as e:
        print(f"An error occurred during transcription with AssemblyAI: {e}")
        raise
