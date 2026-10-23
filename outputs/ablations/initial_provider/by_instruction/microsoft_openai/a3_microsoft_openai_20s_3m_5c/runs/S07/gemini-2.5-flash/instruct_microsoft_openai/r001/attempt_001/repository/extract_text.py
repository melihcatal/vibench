from document_client import get_image_analysis_client
from document_models import ExtractedText
from azure.ai.vision.imageanalysis import VisualFeatures

def extract_text_from_image(image_data: bytes) -> ExtractedText:
    client = get_image_analysis_client()
    features = [VisualFeatures.READ]

    # Authenticate and send the image stream to the Image Analysis service
    result = client.analyze(image_data=image_data, visual_features=features)

    if result.read and result.read.blocks:
        full_text = []
        for block in result.read.blocks:
            for line in block.lines:
                full_text.append(line.text)
        return ExtractedText(text="\n".join(full_text))
    return ExtractedText(text="")
