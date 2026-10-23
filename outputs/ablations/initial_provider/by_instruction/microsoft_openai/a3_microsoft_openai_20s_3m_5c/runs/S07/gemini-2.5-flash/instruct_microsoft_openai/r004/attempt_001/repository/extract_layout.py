from document_client import get_document_analysis_client
from document_models import ExtractedLayout
from azure.ai.vision.imageanalysis.models import VisualFeatures

def extract_layout_from_image(image_data: bytes) -> ExtractedLayout:
    client = get_document_analysis_client()
    
    result = client.analyze(image_data, visual_features=[VisualFeatures.READ])
    
    blocks_data = []
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            block_info = {
                "text": block.text,
                "bounding_box": [(p.x, p.y) for p in block.bounding_box],
                "lines": []
            }
            for line in block.lines:
                line_info = {
                    "text": line.text,
                    "bounding_box": [(p.x, p.y) for p in line.bounding_box],
                    "words": []
                }
                if line.words:
                    for word in line.words:
                        line_info["words"].append({
                            "text": word.text,
                            "bounding_box": [(p.x, p.y) for p in word.bounding_box],
                            "confidence": word.confidence
                        })
                block_info["lines"].append(line_info)
            blocks_data.append(block_info)
                
    return ExtractedLayout(blocks=blocks_data)
