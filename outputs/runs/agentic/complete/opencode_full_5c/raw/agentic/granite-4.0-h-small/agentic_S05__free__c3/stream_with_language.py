from google.cloud import speech_v1p1beta1 as speech

# Provider identifier: GCP Speech-to-Text
client = speech.SpeechClient()

#
# Build a recognizer with language code and punctuation settings
#
language_code = "es-ES"  # Spanish (Spain)
model = "default"  # you can also use "phone_call" or other models
auto_punc = True  # enable automatic punctuation

request = speech.StreamingRecognizeRequest()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code=language_code,
    enable_automatic_punctuation=auto_punc,
    model=model,
)
streaming_config = speech.StreamingRecognitionConfig(
    config=config,
    interim_results=True,
)
request.streaming_config = streaming_config

print(
    f"Starting streaming recognizer for language: {language_code} with auto-punctuation={auto_punc}"
)
# The request object is now ready to be used with the streaming API client as in other scripts.
