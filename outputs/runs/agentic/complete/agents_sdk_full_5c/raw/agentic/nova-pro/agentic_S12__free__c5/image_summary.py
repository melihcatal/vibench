from vision_models import VisionResponse

def summarize(vision_response):
    summary = f'Labels: {vision_response.labels}, Description: {vision_response.description}, Text: {vision_response.text}, Safety: {vision_response.safety}'
    print('Summary:', summary)