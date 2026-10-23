import asyncio
import json
import os
from typing import AsyncIterator, Optional

import speech_recognition as sr


async def stream_microphone(language: str = "en-US", phrase_time_limit: Optional[int] = None) -> AsyncIterator[str]:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    while True:
        loop = asyncio.get_running_loop()
        audio = await loop.run_in_executor(None, _listen_once, recognizer, microphone, phrase_time_limit)
        if audio is None:
            continue
        text = await loop.run_in_executor(None, _recognize_google, recognizer, audio, language)
        if text:
            yield text


def _listen_once(recognizer: sr.Recognizer, microphone: sr.Microphone, phrase_time_limit: Optional[int]) -> Optional[sr.AudioData]:
    with microphone as source:
        try:
            return recognizer.listen(source, phrase_time_limit=phrase_time_limit)
        except Exception:
            return None


def _recognize_google(recognizer: sr.Recognizer, audio: sr.AudioData, language: str) -> str:
    api_key = os.environ.get("GOOGLE_SPEECH_RECOGNITION_API_KEY")
    if api_key:
        return recognizer.recognize_google(audio, key=api_key, language=language)
    return recognizer.recognize_google(audio, language=language)


async def main() -> None:
    async for transcript in stream_microphone():
        print(transcript)


if __name__ == "__main__":
    asyncio.run(main())
