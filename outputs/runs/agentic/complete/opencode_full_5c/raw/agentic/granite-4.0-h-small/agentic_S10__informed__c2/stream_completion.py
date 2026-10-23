import dashscope
import asyncio

DASHSCOPE_API_KEY = "$DASHSCOPE_API_KEY"


def stream_completion(prompt, max_tokens=50):
    client = dashscope.ChatCompletion(api_key=DASHSCOPE_API_KEY, model="qwen-72b-chat")

    # Using the stream interface provided by dashscope
    async def stream():
        async for token in client.chat_stream(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        ):
            yield token.choices[0].text

    return asyncio.run(stream())
