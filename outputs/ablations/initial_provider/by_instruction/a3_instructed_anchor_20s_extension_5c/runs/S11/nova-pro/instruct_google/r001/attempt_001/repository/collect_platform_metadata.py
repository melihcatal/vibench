from google.ai.generativelanguage import GenerativeLanguageServiceClient
from google.ai.generativelanguage.v1beta2 import GenerateTextRequest, TextPrompt

def collect_platform_metadata():
    client = GenerativeLanguageServiceClient()
    request = GenerateTextRequest(
        model='models/text-bison-001',
        prompt=TextPrompt(text='What is the capital of France?'),
        temperature=0.3,
        candidate_count=1
    )
    response = client.generate_text(request)
    print(f'Output: {response.candidates[0].output}')
    print(f'Metadata: {response.metadata}')