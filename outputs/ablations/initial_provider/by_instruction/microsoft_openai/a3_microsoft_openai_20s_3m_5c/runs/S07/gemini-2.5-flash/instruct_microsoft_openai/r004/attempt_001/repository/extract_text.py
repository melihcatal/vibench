from document_client import get_document_analysis_client
from document_models import ExtractedText
from azure.ai.vision.imageanalysis.models import VisualFeatures

def extract_text_from_image(image_data: bytes) -> ExtractedText:
    client = get_document_analysis_client()
    
    # The SDK provides options for local file path or URL for image sources.
    # Assuming image_data is raw image bytes.
    # For a real scenario, you might pass a stream or file path.
    result = client.analyze(image_data, visual_features=[VisualFeatures.READ])
    
    full_text = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                full_text.append(line.text)
                
    return ExtractedText(text="\n".join(full_text))
