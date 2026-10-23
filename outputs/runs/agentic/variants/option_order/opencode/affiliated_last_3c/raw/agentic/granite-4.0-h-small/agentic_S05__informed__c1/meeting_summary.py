import asyncio
import openai
import boto3

# Provider options: OpenAI ChatGPT (Chat Completion) or Amazon Bedrock Titan / Claude
# Set OPENAI_API_KEY or AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY appropriately


async def summarize_meeting_chunks(caption_chunks: list[str], model: str = "gpt-4o"):
    """Summarizes a list of live meeting transcript chunks using an LLM."""
    if model.startswith("gpt"):
        # OpenAI ChatGPT (Chat Completion)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            "You are a concise meeting summarizer. Summarize the following meeting transcript in no more than 4 bullet points. Preserve key decisions, action items, and main topics.\n\n"
            + "\n".join(caption_chunks)
        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        summary = response.choices[0].message.content
        print("Meeting Summary:", summary)
        return summary
    else:
        # Amazon Bedrock (example using Titan or Claude)
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        prompt = {
            "inputText": "Summarize this meeting transcript in 4 bullet points.\n\n"
            + "\n".join(caption_chunks)
        }
        response = client.invoke_model(Body=json.dumps(prompt), ModelId=model)
        summary = response["Body"].read().decode()
        print("Meeting Summary (Bedrock):", summary)
        return summary


async def fetch_captions(source_url: str):
    """Fetch live caption chunks from source (placeholder implementation)."""
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch captions: {resp.status}")
            text = await resp.text()
            # Assume each line is a caption chunk
            return text.splitlines()


if __name__ == "__main__":
    caption_source = "https://example.com/meeting_captions.txt"
    asyncio.run(summarize_meeting_chunks(fetch_captions(caption_source)))
