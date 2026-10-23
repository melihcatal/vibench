from google.ai.generativelanguage import GenerativeLanguageServiceClient
from google.ai.generativelanguage.v1beta2 import GenerateTextRequest, TextPrompt

def invoke_platform_model():
    client = GenerativeLanguageServiceClient()
    request = GenerateTextRequest(
        model='models/text-bison-001',
        prompt=TextPrompt(text='Translate to French: Hello, how are you?'),
        temperature=0.3,
        candidate_count=1
    )
    response = client.generate_text(request)
    print(response.candidates[0].output)