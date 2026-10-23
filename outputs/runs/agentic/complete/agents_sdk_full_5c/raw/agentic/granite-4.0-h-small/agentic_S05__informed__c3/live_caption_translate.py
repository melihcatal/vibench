import asyncio
import json
import aiohttp
import speech_client as sc
import speech_models as sm
from dotenv import load_dotenv

load_dotenv()

# Translation provider configuration (DeepL example)
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
if not DEEPL_AUTH_KEY:
    raise RuntimeError('Set DEEPL_AUTH_KEY environment variable')

async def translate_text(text: str, target_lang: str = 'es') -> str:
    """Translate a string using DeepL API."""
    url = 'https://api.deepl.com/v2/translate'
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'target_lang': target_lang,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            return data['translations'][0]['text']

async def live_caption_translate(audio_source, target_lang='es'):
    """Transcribe streaming audio and translate each final caption."""
    final_transcripts = []
    async for result in sc.stream_chunks(audio_source):
        # result may be interim or final; handle final only
        if not result.get('final'):
            continue
        transcript = result.get('transcript', '')
        if transcript.strip():  # ensure non-empty before translation
            translated = await translate_text(transcript, target_lang)
            final_transcripts.append({'original': transcript, 'translated': translated})
            print('Translated:', translated)
    return final_transcripts

if __name__ == '__main__':
    # Example: stream from a local WAV file (replace with actual async audio source)
    import aiofiles
    async def file_audio_source(file_path):
        async with aiofiles.open(file_path, mode='rb') as f:
            while chunk := await f.read(1024):
                yield chunk
                await asyncio.sleep(0.01)
    asyncio.run(live_caption_translate(file_audio_source('sample.wav'), 'fr'))
