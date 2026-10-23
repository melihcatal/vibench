from google.cloud import documentai

# Configuration
PROJECT_ID = 'your-project-id'
LOCATION = 'us'
PROCESSOR_ID = 'your-processor-id'

# Initialize client
client = documentai.DocumentProcessorServiceClient()

# Function to summarize onboarding state
def summarize_onboarding_state(text):
    name = f'projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}'
    document = documentai.Document(content=text.encode('utf-8'), mime_type='text/plain')
    request = documentai.ProcessRequest(name=name, document=document)
    response = client.process_document(request=request)
    return response.document_text_annotation