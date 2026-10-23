import boto3

class InvoiceExtractor:
    def __init__(self):
        self.textract_client = boto3.client('textract')

    def extract_fields(self, document_path):
        with open(document_path, 'rb') as document:
            image_bytes = document.read()

        response = self.textract_client.analyze_document(
            Document={'Bytes': image_bytes},
            FeatureTypes=['FORMS', 'TABLES']
        )

        vendor = None
        date = None
        total = None
        line_items = []

        for block in response['Blocks']:
            if block['BlockType'] == 'KEY_VALUE_SET':
                if 'VENDOR' in block['Text']:
                    vendor = block['Text'].split('VENDOR')[1].strip()
                elif 'DATE' in block['Text']:
                    date = block['Text'].split('DATE')[1].strip()
                elif 'TOTAL' in block['Text']:
                    total = block['Text'].split('TOTAL')[1].strip()
            elif block['BlockType'] == 'TABLE':
                for relationship in block['Relationships']:
                    if relationship['Type'] == 'CHILD':
                        for child_id in relationship['Ids']:
                            child_block = next(b for b in response['Blocks'] if b['Id'] == child_id)
                            if child_block['BlockType'] == 'CELL':
                                line_items.append(child_block['Text'].strip())

        return {
            'vendor': vendor,
            'date': date,
            'total': total,
            'line_items': line_items
        }
