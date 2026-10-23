import azure.cognitiveservices.speech as speechsdk
import os
from speech_client import get_speech_config

def get_timestamped_transcript(audio_file_path: str, locale: str = "en-US"):
    speech_config = get_speech_config()
    client = speechsdk.SpeechConfig.from_subscription(speech_config.speech_key, speech_config.speech_region)
    
    # Request word-level timestamps
    client.request_word_level_timestamps()

    audio_config = speechsdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=client, audio_config=audio_config, language=locale)

    done = False
    timestamped_segments = []

    def stop_cb(evt):
        print("CLOSING speech recognition for timestamps")
        nonlocal done
        done = True

    def recognized_cb(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            words = []
            # Iterate through word-level details if available
            for word in evt.result.words:
                words.append({
                    "word": word.word,
                    "offset": word.offset,
                    "duration": word.duration
                })
            timestamped_segments.append({
                "text": evt.result.text,
                "words": words
            })
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")

    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    print("Starting speech recognition with word-level timestamps...")
    speech_recognizer.start_continuous_recognition()
    while not done:
        pass
    speech_recognizer.stop_continuous_recognition()

    return {"timestamped_segments": timestamped_segments}

if __name__ == '__main__':
    # Example usage (requires an audio file)
    # print("Please provide an audio file path for testing timestamps.")
    # result = get_timestamped_transcript("path/to/your_audio.wav")
    # for segment in result['timestamped_segments']:
    #     print(f"Segment: {segment['text']}")
    #     for word_info in segment['words']:
    #         print(f"  Word: {word_info['word']}, Offset: {word_info['offset']}, Duration: {word_info['duration']}")
    pass
