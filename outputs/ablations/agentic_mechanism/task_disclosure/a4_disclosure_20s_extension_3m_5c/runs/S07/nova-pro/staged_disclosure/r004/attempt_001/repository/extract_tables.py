import boto3

def extract_tables(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    response = textract_client.analyze_document(Document={'Bytes': imageBytes}, FeatureTypes=['TABLES'])
    tables = response['Blocks']
    table_cells = []
    for block in tables:
        if block['BlockType'] == 'CELL':
            table_cells.append(block)
    return table_cells

if __name__ == '__main__':
    document_path = 'path_to_your_document'
    table_cells = extract_tables(document_path)
    print(table_cells)