from typing import Dict, Any, List, Union

# Define simple type aliases for common LLM input/output structures.
# These are local helper types, not provider-specific.

LLM_TextInput = Dict[str, str]
LLM_ContextInput = Dict[str, str]
LLM_PromptInput = Union[str, List[Dict[str, str]]] # Can be simple string or a list of messages
LLM_Output = Dict[str, str]
