import json
import asyncio
import sys
from typing import AsyncIterable

# Load helper config for Watson credentials
from speech_client import load_config
config = load_config()
WATSON_APIKEY = config["WATSONX_API_KEY"]
WATSON_PROJECT_ID = config["WATSONX_PROJECT_ID"]

async def summarize_captions(captions: AsyncIterable[str]):
    """Summarize live caption chunks using watsonx.ai Qwen model (hosted via dashscope).""",
    import dashscope
    client = dashscope.client.Client(api_key=WATSON_APIKEY)

    async def run_chat(model="qwen:latest"):
        async for chunk in captions:
            # Append new caption to ongoing conversation
            messages = [{"role": "user", "content": chunk}]
            response = await client.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=200,
                system="You are a meeting summarizer. Keep only essential points from the transcript."
            )
            summary = response.choices[0].message.content
            print("[SUMMARY]", summary.strip())

    await run_chat()

if __name__ == "__main__":
    # Simple example: read lines from stdin as transcript chunks
    async def caption_source():
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            yield line.strip()
    asyncio.run(summarize_captions(caption_source()))
