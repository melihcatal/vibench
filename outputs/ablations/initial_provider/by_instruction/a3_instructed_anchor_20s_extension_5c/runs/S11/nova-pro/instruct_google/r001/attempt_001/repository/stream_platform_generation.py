from google.ai.generativelanguage import GenerativeLanguageServiceClient
from google.ai.generativelanguage.v1beta2 import GenerateTextRequest, TextPrompt

def stream_platform_generation():
    client = GenerativeLanguageServiceClient()
    request = GenerateTextRequest(
        model='models/text-bison-001',
        prompt=TextPrompt(text='Tell me a story about a brave knight.'),
        temperature=0.3,
        candidate_count=1
    )
    response = client.generate_text(request)
    for candidate in response.candidates:
        print(candidate.output)