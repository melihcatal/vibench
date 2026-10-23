class DocumentRequest:
    def __init__(self, project_id, location, processor_id, file_path):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.file_path = file_path


class DocumentResponse:
    def __init__(self, document):
        self.document = document
