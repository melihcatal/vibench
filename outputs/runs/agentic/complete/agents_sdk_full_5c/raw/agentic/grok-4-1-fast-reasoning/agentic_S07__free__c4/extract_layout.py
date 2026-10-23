from document_client import get_textract_client
from document_models import LayoutBlock
from typing import List
import io

def extract_layout(image_path: str) -> List[LayoutBlock]:
    client = get_textract_client()
    with io.open(image_path, 'rb') as image_file:
        img_bytes = image_file.read()
    response = client.analyze_document(
        Document={'Bytes': img_bytes},
        FeatureTypes=[]
    )
    blocks = []
    for block in response['Blocks']:
        if block['BlockType'] in ['LINE', 'WORD']:
            geometry = block['Geometry']['BoundingBox']
            bbox = {
                'top': geometry['Top'],
                'left': geometry['Left'],
                'width': geometry['Width'],
                'height': geometry['Height']
            }
            conf = block.get('Confidence', 0.0)
            blocks.append(LayoutBlock(
                type=block['BlockType'].lower(),
                text=block.get('Text', ''),
                bounding_box=bbox,
                confidence=conf
            ))
    return blocks