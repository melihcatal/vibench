from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class DocumentKey:
    partition_key: str
    sort_key: str = None

    def to_dynamodb_key(self, partition_key_name: str, sort_key_name: str = None) -> Dict[str, Dict[str, str]]:
        key = {
            partition_key_name: {'S': self.partition_key}
        }
        if self.sort_key and sort_key_name:
            key[sort_key_name] = {'S': self.sort_key}
        return key

@dataclass
class Document:
    id: str
    data: Dict[str, Any]
    version: int = 1

    @staticmethod
    def from_dynamodb_item(item: Dict[str, Dict[str, Any]]) -> 'Document':
        if not item: return None
        # Assuming 'id' is the primary key and 'data' holds the rest, 'version' for optimistic locking
        doc_id = item.pop('id', {}).get('S') if 'id' in item else None
        doc_version = int(item.pop('version', {}).get('N', 1)) if 'version' in item else 1
        
        # Convert DynamoDB typed values back to native Python types for the data field
        native_data = {}
        for k, v_typed in item.items():
            if 'S' in v_typed: native_data[k] = v_typed['S']
            elif 'N' in v_typed: native_data[k] = float(v_typed['N']) # Or int if always integers
            elif 'BOOL' in v_typed: native_data[k] = v_typed['BOOL']
            # Add other types as needed (B, SS, NS, BS, L, M, NULL)
            elif 'M' in v_typed: native_data[k] = {ik: iv['S'] if 'S' in iv else (float(iv['N']) if 'N' in iv else None) for ik, iv in v_typed['M'].items()}
            elif 'L' in v_typed: native_data[k] = [iv['S'] if 'S' in iv else (float(iv['N']) if 'N' in iv else None) for iv in v_typed['L']]
            else: native_data[k] = None # Fallback

        return Document(id=doc_id, data=native_data, version=doc_version)

    def to_dynamodb_item(self, primary_key_name: str = "id") -> Dict[str, Dict[str, Any]]:
        item = {
            primary_key_name: {'S': self.id},
            'version': {'N': str(self.version)}
        }
        for k, v in self.data.items():
            if isinstance(v, str):
                item[k] = {'S': v}
            elif isinstance(v, (int, float)):
                item[k] = {'N': str(v)}
            elif isinstance(v, bool):
                item[k] = {'BOOL': v}
            elif isinstance(v, dict):
                # Simple conversion for nested dicts, more complex logic might be needed
                item[k] = {'M': {ik: {'S': str(iv)} for ik, iv in v.items()}}
            elif isinstance(v, list):
                # Simple conversion for nested lists, more complex logic might be needed
                item[k] = {'L': [{'S': str(iv)} for iv in v]}
            else:
                item[k] = {'NULL': True} # Handle other types or skip
        return item

@dataclass
class DocumentSummary:
    document_id: str
    summary_text: str
    keywords: List[str] = field(default_factory=list)

@dataclass
class SafetyCheckResult:
    document_id: str
    unsafe_content_detected: bool
    moderation_labels: List[Dict[str, Any]] = field(default_factory=list) # For AWS Comprehend/Rekognition

@dataclass
class TranslatedDocument:
    document_id: str
    original_field: str
    translated_text: str
    target_language: str
