from typing import TypedDict, List, Dict, Any

class VisionLabels(TypedDict):
    labels: List[str]

class VisionCaption(TypedDict):
    caption: str

class VisionTexts(TypedDict):
    texts: List[str]

class VisionSafety(TypedDict):
    is_adult_content: bool
    is_racy_content: bool
    is_gory_content: bool
    adult_score: float
    racy_score: float
    gory_score: float

class FullVisionAnalysis(TypedDict):
    labels: List[str]
    caption: str
    texts: List[str]
    safety: Dict[str, Any]

def normalize_labels(analysis_result) -&gt; VisionLabels:
    labels = []
    if analysis_result.tags:
        for tag in analysis_result.tags.values:
            if tag.confidence &gt; 0.5:
                labels.append(tag.name)
    return {&quot;labels&quot;: labels}

def normalize_caption(analysis_result) -&gt; VisionCaption:
    caption = analysis_result.caption.text if analysis_result.caption else &quot;&quot;
    return {&quot;caption&quot;: caption}

def normalize_texts(analysis_result) -&gt; VisionTexts:
    texts = []
    if analysis_result.read and analysis_result.read.blocks:
        for block in analysis_result.read.blocks:
            for line in block.lines:
                texts.append(line.text)
    return {&quot;texts&quot;: texts}

def normalize_safety(analysis_result) -&gt; VisionSafety:
    safety = analysis_result.adult
    return {
        &quot;is_adult_content&quot;: safety.isAdultContent if safety else False,
        &quot;is_racy_content&quot;: safety.isRacyContent if safety else False,
        &quot;is_gory_content&quot;: safety.isGoryContent if safety else False,
        &quot;adult_score&quot;: safety.adultScore.value if safety else 0.0,
        &quot;racy_score&quot;: safety.racyScore.value if safety else 0.0,
        &quot;gory_score&quot;: safety.goryScore.value if safety else 0.0,
    }