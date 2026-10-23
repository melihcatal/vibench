class DocumentModel:
    def __init__(self, blocks):
        self.blocks = blocks

    def get_text(self):
        text_blocks = [block for block in self.blocks if block['BlockType'] == 'LINE']
        return ' '.join([block['Text'] for block in text_blocks])