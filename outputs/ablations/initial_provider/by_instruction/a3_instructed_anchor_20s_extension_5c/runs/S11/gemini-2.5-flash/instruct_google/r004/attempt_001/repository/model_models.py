import dataclasses

@dataclasses.dataclass
class PlatformPrompt:
    text: str
    
@dataclasses.dataclass
class PlatformOutput:
    text: str
    metadata: dict = dataclasses.field(default_factory=dict)
