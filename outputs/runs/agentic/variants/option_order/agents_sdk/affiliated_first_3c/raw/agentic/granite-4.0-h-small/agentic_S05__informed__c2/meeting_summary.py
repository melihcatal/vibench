import os
import asyncio
from typing import AsyncIterable
from ibm_watsonx_ai import WatsonxApi
from ibm_watsonx_ai.llms import SamplingParameters
from speech_models import RecognitionResponse

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
ASSISTANT_ID = 'assistant-12345'  # placeholder ID

async def summarize_meeting_chapters(chapters: AsyncIterable[str]) -> AsyncIterable[str]:
    """
    Takes streaming text chunks (e.g., meeting minutes) and returns a concise
    summary for each chunk using watsonx.ai Granite model.
    """
    # Initialise watsonx API client (sdk-or-rest style)
    api = WatsonxApi(credential=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)
    # Granite model identifier (family: granite-13b-chat)
    model_id = 'granite-13b-chat'
    # Simple summarization prompt
    system_prompt = "You are a helpful meeting summarizer. Summarize the following meeting notes in no more than 3 sentences."

    async for chapter in chapters:
        response = await api.call_completion(
            model=model_id,
            messages=[{'role': 'user', 'content': f"{system_prompt}\n\n{chapter}"}],
            max_output_tokens=128
        )
        # The SDK returns the completion text in response['choices'][0]['message']['content']
        summary = response['choices'][0]['message']['content']
        yield summary.strip()

# Usage example (requires an async generator that yields each meeting paragraph)
# async for summary in summarize_meeting_chapters(line_generator()):
#     print('Summary:', summary)
