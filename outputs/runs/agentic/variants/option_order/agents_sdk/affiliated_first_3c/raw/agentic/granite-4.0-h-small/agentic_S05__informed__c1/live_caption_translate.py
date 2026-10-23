import asyncio
import json
from google.cloud import speech
from google.cloud import translate_v2 as translate

def stream_and_translate(audio_stream, target_lang='es'):
    """
    Streams audio to Google Cloud Speech-to-Text and translates the interim
    transcript to the target language. Yields translated captions.
    """
    # Initialize clients
    speech_client = speech.SpeechClient()
    translate_client = translate.Client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_stream
    )

    responses = speech_client.streaming_recognize(streaming_config, requests)
    current_transcript = []
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                frag = result.alternatives[0].transcript.strip()
                if result.is_final:
                    # Translate final segment
                    translation = translate_client.translate(
                        frag, target_language=target_lang
                    )['translatedText']
                    yield translation, True
                    current_transcript.clear()
                else:
                    # Translate interim fragment
                    translation = translate_client.translate(
                        frag, target_language=target_lang
                    )['translatedText']
                    yield translation, False
                    current_transcript.append(translation)

async def async_test():
    # Example: use a file-like object as audio source
    import io
    audio_file = io.BytesIO(b'')  # placeholder – replace with real audio bytes
    async for caption, final in stream_and_translate(audio_file, target_lang='es'):
        print('Translated caption:', caption, '(final)' if final else '')

if __name__ == '__main__':
    asyncio.run(async_test())
