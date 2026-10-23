import asyncio
from ibm_watsonx_ai import watsonxai
from ibm_watsonx_ai.nlu import NaturalLanguageUnderstandingV2
import json

class MeetingSummary:
    def __init__(self):
        self.nlu = NaturalLanguageUnderstandingV2(
            version='2024-08-01',
            auth_type='iam',
            apikey=os.getenv('WATSONX_API_KEY'),
            service_url='https://api.ibm.com/watsonx/v1/nlu'
        )

    async def summarize(self, text_chunks):
        """Combines text chunks and requests a short summary from watsonx.ai generative model.
        Returns a concise summary string."
        full_text = ''.join(text_chunks)
        if not full_text:
            return ''
        # Prompt for summarization
        prompt = {
            'model': 'granite-13b-v2',
            'messages': [
                {'role': 'user', 'content': f'Summarize the following meeting transcript in 3 sentences:\n\n{full_text}'},
            ]
        }
        response = await self.nlu.generate_text(prompt)
        # Parse generated text
        generated = json.loads(response.get('generated_text', ''))
        summary = generated.get('text', '')
        return summary

if __name__ == '__main__':
    async def demo():
        chunks = [
            'Welcome everyone to the product design review meeting. ',
            'Today we will discuss the latest prototype features, feedback, and timeline. ',
            'First, the engineering lead will present prototype performance metrics. '
        ]
        summarizer = MeetingSummary()
        summary = await summarizer.summarize(chunks)
        print('Meeting summary:', summary)
    asyncio.run(demo())
