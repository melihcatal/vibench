class DocumentText:
    def __init__(self, raw_textract_response: dict):
        self.raw_response = raw_textract_response
        self.pages = []
        self.lines = []
        self.words = []
        self._parse_text_blocks()

    def _parse_text_blocks(self):
        if not self.raw_response or 'Blocks' not in self.raw_response:
            return

        for block in self.raw_response['Blocks']:
            if block['BlockType'] == 'PAGE':
                self.pages.append(block)
            elif block['BlockType'] == 'LINE':
                self.lines.append(block)
            elif block['BlockType'] == 'WORD':
                self.words.append(block)

    def get_full_text(self) -> str:
        return " ".join([line['Text'] for line in self.lines if 'Text' in line])

class DocumentLayout:
    def __init__(self, raw_textract_response: dict):
        self.raw_response = raw_textract_response
        self.blocks = []
        self.lines = []
        self.words = []
        self.forms = []
        self.tables = []
        self.selection_elements = []
        self._parse_layout_blocks()

    def _parse_layout_blocks(self):
        if not self.raw_response or 'Blocks' not in self.raw_response:
            return

        for block in self.raw_response['Blocks']:
            if block['BlockType'] == 'BLOCK': # Placeholder if a generic 'BLOCK' type is ever returned by layout
                self.blocks.append(block)
            elif block['BlockType'] == 'LINE':
                self.lines.append(block)
            elif block['BlockType'] == 'WORD':
                self.words.append(block)
            elif block['BlockType'] == 'KEY_VALUE_SET':
                self.forms.append(block)
            elif block['BlockType'] == 'TABLE':
                self.tables.append(block)
            elif block['BlockType'] == 'SELECTION_ELEMENT':
                self.selection_elements.append(block)

class DocumentTables:
    def __init__(self, raw_textract_response: dict):
        self.raw_response = raw_textract_response
        self.tables = []
        self.cells = []
        self._parse_table_blocks()

    def _parse_table_blocks(self):
        if not self.raw_response or 'Blocks' not in self.raw_response:
            return
        for block in self.raw_response['Blocks']:
            if block['BlockType'] == 'TABLE':
                self.tables.append(block)
            elif block['BlockType'] == 'CELL':
                self.cells.append(block)

class DocumentKeyValues:
    def __init__(self, raw_textract_response: dict):
        self.raw_response = raw_textract_response
        self.key_values = []
        self._parse_key_value_blocks()

    def _parse_key_value_blocks(self):
        if not self.raw_response or 'Blocks' not in self.raw_response:
            return
        for block in self.raw_response['Blocks']:
            if block['BlockType'] == 'KEY_VALUE_SET':
                self.key_values.append(block)
