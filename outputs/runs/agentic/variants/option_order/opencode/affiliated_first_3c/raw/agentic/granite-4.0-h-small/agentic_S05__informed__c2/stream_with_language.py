import ibm_watson
import ibm_watson.streaming.base as asr_base

# Watson STT WebSocket credentials (environment variables)
API_KEY = os.getenv("IBM_STT_APIKEY")
URL = os.getenv("IBM_STT_URL")


async def stream_with_language(
    language: str = "en-US", enable_punctuation: bool = True
):
    """Starts a streaming recognizer with specified language and punctuation settings.

    Args:
        language: BCP-47 language code (default "en-US").
        enable_punctuation: Whether to add punctuation to transcripts.
    """
    # Build model name with language suffix (Watson uses "_" separator)
    model = f"{language.replace('-', '_')}BroadbandModel"
    config = ibm_watson.speech_to_text_v1.RecognizeStreamConfig(
        content_type="audio/l16; rate=16000",
        interim_results=True,
        continuous=True,
        model=model,
        smart_formatting=enable_punctuation,
        word_confidence=True,
    )
    # Authenticate via IAM
    token_manager = ibm_watson.IamAuthenticator(API_KEY)
    auth_token = token_manager.get_token()
    async for result in asr_base.recognize_stream(
        url=URL,
        config=config,
        auth_token=auth_token,
        audio_provider=asr_base.MicrophoneStream(),
    ):
        if result.alternatives and result.alternatives[0].transcript:
            print(result.alternatives[0].transcript)


# Example call with French and punctuation off
if __name__ == "__main__":
    asyncio.run(stream_with_language(language="fr-FR", enable_punctuation=False))
