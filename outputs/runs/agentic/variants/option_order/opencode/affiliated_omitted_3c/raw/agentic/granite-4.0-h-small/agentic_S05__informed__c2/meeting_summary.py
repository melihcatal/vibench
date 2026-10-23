import asyncio
from dashscope import OpenAI

# DashScope SDK loading Qwen model identifies the provider


async def summarize_meeting(transcript_chunks):
    """Generate a concise summary of live meeting transcript chunks."""
    model = "qwen2-72b-chat"  # Hosted Qwen model via DashScope
    client = OpenAI(model=model, api_key=os.getenv("DASHSCOPE_API_KEY"))
    buffer = []
    async for chunk in transcript_chunks:
        buffer.append(chunk)
        # Summarize only when a reasonable amount of context is collected
        if len(buffer) >= 5:
            text = " ".join(buffer)
            response = await client.chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following meeting excerpt:\n{text}",
                    }
                ],
                temperature=0.2,
            )
            yield f"<SUMMARY> {response.choices[0].message.content} </SUMMARY>"
            buffer = []  # reset after each summary
