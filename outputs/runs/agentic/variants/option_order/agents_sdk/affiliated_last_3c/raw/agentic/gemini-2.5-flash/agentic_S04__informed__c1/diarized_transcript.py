import azure.cognitiveservices.speech as speechsdk
import os
from speech_client import get_speech_config

def get_diarized_transcript(audio_file_path: str, locale: str = "en-US"):
    speech_config = get_speech_config()
    client = speechsdk.SpeechConfig.from_subscription(speech_config.speech_key, speech_config.speech_region)
    
    # Enable speaker diarization
    client.request_word_level_timestamps()
    client.enable_speaker_diarization()

    audio_config = speechsdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=client, audio_config=audio_config, language=locale)

    # The event-driven model is suitable for continuous recognition.
    # For file input, we can also use `recognize_once_async` or continuous recognition.
    # Here, we'll collect results from continuous recognition for potentially longer files.

    done = False
    diarized_segments = []

    def stop_cb(evt):
        print("CLOSING speech recognition for diarization")
        nonlocal done
        done = True

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            speaker_id = speechsdk.PropertyId.SpeechServiceResponse_SpeakerId
            if evt.result.properties.get(speaker_id) is not None:
                diarized_segments.append({
                    "speaker": evt.result.properties.get(speaker_id),
                    "text": evt.result.text
                })
            else:
                diarized_segments.append({
                    "speaker": "unknown", # Fallback if speaker ID is not present
                    "text": evt.result.text
                })
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Starting speech recognition with diarization...")
    speech_recognizer.start_continuous_recognition()
    while not done:
        pass
    speech_recognizer.stop_continuous_recognition()

    return {"diarized_segments": diarized_segments}

if __name__ == '__main__':
    # Example usage (requires an audio file)
    # print("Please provide an audio file path for testing diarization.")
    # result = get_diarized_transcript("path/to/your_meeting.wav")
    # for segment in result['diarized_segments']:
    #     print(f"Speaker {segment['speaker']}: {segment['text']}")
    pass
