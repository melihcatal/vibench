import os
import azure.cognitiveservices.speech as speechsdk

def submit_transcription_job(audio_file_path: str, locale: str = "en-US"):
    speech_key = os.environ.get("SPEECH_KEY")
    service_region = os.environ.get("SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # This example uses the Azure Speech SDK, which primarily focuses on real-time and
    # file-based transcription with direct SDK calls. For true "batch" transcription
    # as an asynchronous operation (e.g., submitting a URL and polling for results),
    # the Azure Speech to Text REST API v3.0 is typically used.
    # The SDK provides a more direct way for single-file processing.
    
    # For a real batch scenario with the REST API, you'd typically upload the audio to blob storage,
    # then submit a transcription job with the blob URI to the REST API, and poll for status.
    # This SDK example demonstrates submitting a single file for transcription.
    
    audio_config = speechsdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language=locale)

    print(f"Submitting transcription for {audio_file_path}...")

    # The recognize_once_async() call performs transcription for a single audio file.
    # For a batch scenario, you would typically manage multiple such operations or use the REST API.
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Transcription successful. Text: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return None

if __name__ == "__main__":
    # Example usage (replace with a real audio file path)
    # Ensure you have a WAV file with suitable audio.
    # For testing, you might need to create a dummy audio file or use a small sample.
    dummy_audio_file = "sample_audio.wav"
    
    # Create a dummy WAV file for demonstration if it doesn't exist
    if not os.path.exists(dummy_audio_file):
        print(f"Creating a dummy WAV file: {dummy_audio_file} for demonstration.")
        # This is a highly simplified dummy file creation. 
        # For actual speech recognition, you need a valid WAV file with audio data.
        # This just creates an empty WAV header.
        try:
            from scipy.io.wavfile import write as write_wav
            import numpy as np
            samplerate = 16000
            duration = 1  # seconds
            frequency = 440  # Hz
            t = np.linspace(0., duration, int(samplerate * duration))
            amplitude = 0.5
            data = amplitude * np.sin(2. * np.pi * frequency * t)
            write_wav(dummy_audio_file, samplerate, data.astype(np.float32))
            print(f"Dummy WAV file '{dummy_audio_file}' created. Please ensure it contains actual speech for meaningful transcription.")
        except ImportError:
            print("SciPy not installed. Cannot create dummy WAV file. Please install it (`pip install scipy`) or provide a real audio file.")
            print(f"Alternatively, you can manually create '{dummy_audio_file}' with some speech content.")

    if os.path.exists(dummy_audio_file):
        # Set environment variables or replace with actual keys for testing
        # os.environ["SPEECH_KEY"] = "YOUR_SPEECH_KEY"
        # os.environ["SPEECH_REGION"] = "YOUR_SPEECH_REGION"
        
        # Ensure SPEECH_KEY and SPEECH_REGION are set in your environment
        # For example:
        # export SPEECH_KEY="YOUR_AZURE_SPEECH_SERVICE_KEY"
        # export SPEECH_REGION="YOUR_AZURE_SPEECH_SERVICE_REGION"
        
        # Test with the dummy file
        # transcript = submit_transcription_job(dummy_audio_file)
        # if transcript:
        #     print(f"Main function received transcript: {transcript}")
        # else:
        #     print("Transcription failed or returned no text.")
        print("To run this example, set SPEECH_KEY and SPEECH_REGION environment variables and uncomment the test lines.")
    else:
        print(f"Please provide a valid audio file path for transcription, or ensure '{dummy_audio_file}' is created with speech content.")
