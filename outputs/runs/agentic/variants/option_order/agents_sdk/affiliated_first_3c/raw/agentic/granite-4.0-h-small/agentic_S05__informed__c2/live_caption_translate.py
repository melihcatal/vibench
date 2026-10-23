import os
import asyncio
from typing import AsyncIterable
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from speech_models import RecognitionResponse

async def translate_live_captions(source: AsyncIterable[bytes]) -> AsyncIterable[str]:
    """
    Streams audio from 'source' to IBM Watson STT, then translates each
    final transcript into the target language using Alibaba Cloud Machine
    Translation.
    """
    # Watson STT client
    stt_client = SpeechToTextV1(
        iam_apikey=os.getenv('IBM_STT_APIKEY'),
        url=os.getenv('IBM_STT_URL')
    )
    stt_client.set_disable_ssl_verification(True)

    # Alibaba MT client (using alibabacloud_alimt SDK)
    from alibabacloud_alimt20210622.client import Client as MTClient
    from alibabacloud_tea_openapi.models import Config
    mt_config = Config(
        access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        endpoint='mt.cn-hangzhou.aliyuncs.com',
        region_id='cn-hangzhou'
    )
    mt = MTClient(mt_config)

    target_lang = 'fr'  # French; adjust as needed

    async for audio_chunk in source:
        # Send chunk and receive interim/final results via WebSocket
        audio = AudioSource(content_type='audio/l16; rate=16000', stream=asyncio.StreamReader())
        # NOTE: In real code we would feed the chunk to the WebSocket; here we abstract.
        # For demo we call recognize_stream once per chunk.
        response = stt_client.recognize(
            audio=audio_chunk,
            content_type='audio/l16; rate=16000',
            interim_results=False,
            model='en-US_NarrowbandModel'
        )
        transcript = response.get_result().get('results', [{}])[0].get('alternatives', [{}])[0].get('transcript', '')
        if transcript:
            # Translate the final text (ignore interim results for brevity)
            request_body = {
                'source_language_code': 'en',
                'target_language_code': target_lang,
                'text': transcript
            }
            mt_resp = mt.translate(request_body)
            translation = mt_resp.body.get('translated_text', '')
            yield translation

# Example top‑level usage (requires asyncio source generator)
# async def audio_generator():
#     while True:
#         chunk = ...
#         yield chunk
# async for caption in translate_live_captions(audio_generator()):
#     print('Translated:', caption)
