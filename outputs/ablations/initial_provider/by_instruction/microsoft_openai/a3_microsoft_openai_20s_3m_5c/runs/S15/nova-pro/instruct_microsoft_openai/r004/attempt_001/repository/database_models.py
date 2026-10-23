from typing import Dict

class DatabaseModels:
    @staticmethod
    def create_document(document_id: str, content: str) -> Dict:
        return {
            'id': document_id,
            'content': content
        }

    @staticmethod
    def normalize_response(response: Dict) -> Dict:
        return {
            'id': response.get('id'),
            'content': response.get('content', '')
        }

if __name__ == '__main__':
    pass