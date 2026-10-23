from document_client import get_image_analysis_client
from document_models import ExtractedBlock
from azure.ai.vision.imageanalysis import VisualFeatures

def extract_layout_from_image(image_data: bytes) -> list[ExtractedBlock]:
    client = get_image_analysis_client()
    features = [VisualFeatures.DENSE_CAPTIONS] # This feature provides bounding boxes and descriptions of regions

    result = client.analyze(image_data=image_data, visual_features=features)

    extracted_blocks = []
    if result.dense_captions and result.dense_captions.list:
        for caption in result.dense_captions.list:
            # The Image Analysis service doesn't directly provide 'blocks' in the same way Document Intelligence does.
            # For layout extraction, we can interpret dense captions as content blocks with bounding boxes.
            # We'll use the bounding box and the text from the caption.
            bounding_box = [caption.bounding_box.x, caption.bounding_box.y, caption.bounding_box.width, caption.bounding_box.height]
            extracted_blocks.append(ExtractedBlock(content=caption.text, bounding_box=bounding_box, kind="region", confidence=caption.confidence))
    
    # Optionally, to get text blocks with bounding boxes, you could also use VisualFeatures.READ
    # and then iterate through result.read.blocks, but the dense captions are more about layout regions.
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                bounding_box = [line.bounding_box[0], line.bounding_box[1], line.bounding_box[2], line.bounding_box[3]]
                extracted_blocks.append(ExtractedBlock(content=line.text, bounding_box=bounding_box, kind="textLine", confidence=None)) # Confidence not directly available for line from Image Analysis

    return extracted_blocks
