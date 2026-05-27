"""
VIBench — Service Detection Pipeline
Detects which cloud provider/service was used in each model output.

For documented-reference outputs: matches against the known listed options.
For NLI/FIM outputs: uses SDK imports, URLs, and keyword detection.

Usage:
    python scripts/evaluation/detect_services.py --run direct/complete/full_5c
    python scripts/evaluation/detect_services.py --run latest
    python scripts/evaluation/detect_services.py --run latest --modality nli
    python scripts/evaluation/detect_services.py --run latest --stats
"""

import json
import re
import os
import argparse
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RUNS_DIR = BASE_DIR / "outputs" / "runs"
RESULTS_DIR = BASE_DIR / "results"
RUN_SEARCH_DIRS = [RESULTS_DIR, RUNS_DIR]
DATASETS_DIR = BASE_DIR / "benchmark"
OPEN_REFERENCE_MODALITY = "reference_open"
LEGACY_CS_MODALITY = "cs_documented"
REFERENCE_MODALITIES = {OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY}


def _strip_python_line_comments(text):
    """Remove Python line comments before provider matching.

    The detector should not treat commented examples as active provider use.
    Keep string literals intact so real endpoint constants still match.
    """
    text = text or ""
    if "\n" not in text and "\\n" in text:
        text = text.replace("\\n", "\n")

    cleaned = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue

        quote = None
        escaped = False
        cut_at = None
        for idx, char in enumerate(line):
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if quote:
                if char == quote:
                    quote = None
                continue
            if char in {"'", '"'}:
                quote = char
                continue
            if char == "#":
                cut_at = idx
                break

        cleaned.append(line[:cut_at] if cut_at is not None else line)
    return "\n".join(cleaned)


def _is_reference_modality(modality):
    return modality in REFERENCE_MODALITIES


def _canonical_benchmark_name(benchmark):
    key = (benchmark or "vibench").strip().lower()
    aliases = {
        "vibench": "vibench",
        "current": "vibench",
        "v3": "vibench",
        "v3_core4": "vibench",
    }
    if key not in aliases:
        raise ValueError(f"Unsupported benchmark '{benchmark}'. This repository keeps only the current 'vibench' benchmark.")
    return aliases[key]


def _iter_run_dirs(base):
    """Yield run directories recursively under a search base."""
    if not base.exists():
        return []
    seen = set()
    runs = []
    for marker in ("config.yaml", "labeled", "raw"):
        paths = base.rglob(marker)
        for path in paths:
            run_dir = path.parent if path.name == "config.yaml" else path.parent
            if run_dir in seen:
                continue
            if (run_dir / "labeled").is_dir() or (run_dir / "raw").is_dir() or (run_dir / "config.yaml").exists():
                seen.add(run_dir)
                runs.append(run_dir)
    return sorted(runs)


def _run_match_key(base, run_dir):
    try:
        return run_dir.relative_to(base).as_posix()
    except ValueError:
        return run_dir.name


def resolve_run_dir(run_id):
    """Resolve a run directory from an ID, a partial name, a path, or 'latest'.

    Searches both the curated results/ directory (for committed paper
    results) and the fresh outputs/runs/ directory (for in-progress runs).
    """
    # 1. explicit path to an existing directory
    candidate = Path(run_id)
    if candidate.exists() and candidate.is_dir():
        return candidate

    # 2. "latest" means newest fresh run under outputs/runs/
    if run_id == "latest":
        runs = _iter_run_dirs(RUNS_DIR)
        if not runs:
            print("No runs found in outputs/runs/")
            return None
        return max(runs, key=lambda p: p.stat().st_mtime)

    # 3. exact name under any search dir
    for base in RUN_SEARCH_DIRS:
        if not base.exists():
            continue
        run_path = base / run_id
        if run_path.exists() and run_path.is_dir():
            return run_path

    # 4. exact leaf or relative path match under any search dir
    for base in RUN_SEARCH_DIRS:
        for run_path in _iter_run_dirs(base):
            rel = _run_match_key(base, run_path)
            if run_path.name == run_id or rel == run_id:
                return run_path

    # 5. substring match under any search dir
    for base in RUN_SEARCH_DIRS:
        matches = sorted([
            d for d in _iter_run_dirs(base)
            if run_id in d.name or run_id in _run_match_key(base, d)
        ])
        if matches:
            return matches[-1]

    print(f"Run '{run_id}' not found in results/ or outputs/runs/")
    return None

# ---------------------------------------------------------------------------
# Provider detection rules (ordered by specificity)
# ---------------------------------------------------------------------------

# provider_key is the direct service/provider label used in outputs.
# detected_ecosystem is a higher-level rollup used for paper analysis.
PROVIDER_TO_ECOSYSTEM = {
    "aws": "aws",
    "google": "google",
    "azure": "microsoft_openai",
    "azure_openai": "microsoft_openai",
    "openai": "microsoft_openai",
    "anthropic": "anthropic",
    "alibaba": "alibaba",
    "ibm": "ibm",
    "auth0": "independent",
    "okta": "independent",
    "independent": "independent",
    "deepl": "independent",
    "assemblyai": "independent",
    "deepgram": "independent",
    "elevenlabs": "independent",
    "mindee": "independent",
    "clarifai": "independent",
    "launchdarkly": "independent",
    "cohere": "independent",
    "hive": "independent",
    "mapbox": "independent",
    "here": "independent",
    "voyage": "independent",
    "mistral": "independent",
    "pdf4me": "independent",
    "pdf_co": "independent",
    "cloudmersive": "independent",
    "parsehub": "independent",
    "rossum": "independent",
    "sentry": "independent",
    "resend": "independent",
    "speechmatics": "independent",
    "murf": "independent",
    "rev_ai": "independent",
    "stytch": "independent",
    "pubnub": "independent",
    "plaid": "independent",
    "grammarly": "independent",
    "hyperscience": "independent",
    "tisane": "independent",
    "confluent": "independent",
    "backblaze_b2": "independent",
    "doppler": "independent",
    "minio": "independent",
    "textblob": "independent",
    "unstructured": "independent",
    "invoice2data": "independent",
    "gensim": "independent",
    "transformers": "independent",
    "unknown": "unknown",
}

PROVIDER_SDK_HINTS = {
    "aws": [r"\bboto3\.(client|resource)\s*\(", r"\bbotocore\b", r"\bappconfigdata\b", r"\bsagemaker\b", r"\bJumpStartModel\b", r"\bjumpstart\b"],
    "google": [r"google\.cloud", r"from google\.cloud import", r"google\.generativeai", r"\bvertexai\b", r"\baiplatform\b", r"\bfirebase_admin\b", r"\bpyrebase\b", r"google\.auth", r"google\.oauth2", r"google_auth_oauthlib", r"\bgooglemaps\b", r"remote_config", r"commentanalyzer", r"GoogleOAuthClient", r"\bgTTS\b", r"recognize_google", r"google_cloud_speech", r"\bgoogle_cloud\b", r"aiy\.cloudspeech"],
    "azure": [r"azure\.", r"\bmsal\b", r"microsoft\.identity", r"AzureOpenAI", r"AZURE_OPENAI_", r"DefaultAzureCredential", r"AzureAppConfigurationClient", r"AZURE_DOCUMENT_INTELLIGENCE_", r"AZURE_FORM_RECOGNIZER_", r"MICROSOFT_FORM_RECOGNIZER_", r"AZURE_SPEECH_", r"AZURE_VISION_", r"AZURE_COMPUTER_VISION_", r"contentmoderator/moderate", r"COSMOS_ENDPOINT", r"COSMOS_KEY", r"COSMOSDB_", r"SpeechConfig", r"speechsdk", r"documentintelligence"],
    "openai": [r"\bfrom openai import\b", r"\bimport openai\b", r"openai\.OpenAI", r"openai\.ChatCompletion", r"openai\.types", r"\bOpenAI\s*\(", r"\bOPENAI_API_KEY\b", r"\blangchain_openai\b", r"\bChatOpenAI\b"],
    "anthropic": [r"\bfrom anthropic import\b", r"\bimport anthropic\b", r"anthropic\.Anthropic", r"langchain_anthropic", r"ChatAnthropic"],
    "alibaba": [r"alibabacloud", r"aliyunsdk", r"\boss2\b", r"\bdashscope\b", r"\bAcsClient\b", r"ALIBABA_IDAAS_"],
    "ibm": [r"ibm_boto3", r"ibm_watson", r"ibm_watsonx_ai", r"ibm_cloud_sdk_core", r"ibm_secrets_manager_sdk", r"ibm_cos_sdk", r"IAMAuthenticator", r"IBM_TTS_", r"IBM_STT_", r"IBM_APPID_", r"IBM_SECRETS_MANAGER_", r"IBM_COS_", r"ibm_cloudant", r"IBMCLOUDANT_"],
    "clarifai": [r"\bclarifai\b", r"api\.clarifai\.com"],
    "launchdarkly": [r"\bldclient\b", r"launchdarkly", r"bool_variation", r"json_variation"],
    "hive": [r"thehive", r"hive\.ai"],
    "mapbox": [r"\bmapbox\b", r"api\.mapbox\.com"],
    "here": [r"hereapi", r"geocode\.search\.hereapi\.com"],
    "independent": [
        r"\bfrom auth0\b", r"\bimport auth0\b",
        r"\bfrom okta\b", r"\bimport okta\b",
        r"\bimport deepl\b", r"\bfrom deepl\b",
        r"\bimport assemblyai\b", r"\bfrom assemblyai\b",
        r"\bimport deepgram\b", r"\bfrom deepgram\b",
        r"\bimport elevenlabs\b", r"\bfrom elevenlabs\b",
        r"\bimport mindee\b", r"\bfrom mindee\b",
        r"\bimport cohere\b", r"\bfrom cohere\b",
        r"\bimport voyageai\b", r"\bfrom voyageai\b",
        r"\bimport mistralai\b", r"\bfrom mistralai\b",
        r"\bpymongo\b", r"MongoClient", r"MONGODB_URI",
        r"\balgoliasearch\b", r"\bclarifai\b", r"\bldclient\b", r"\bmapbox\b", r"\bhereapi\b", r"thehive",
        r"github\.com/login/oauth", r"api\.github\.com",
        r"accounts\.spotify\.com", r"api\.spotify\.com",
        r"WOLFRAMALPHA_APP_ID", r"\bwolframalpha\b",
        r"PANGEA_(REDACT_TOKEN|DOMAIN)", r"pangea\.cloud",
        r"VERYFI_(API_KEY|CLIENT_ID|USERNAME)", r"api\.veryfi\.com",
        r"api\.meaningcloud\.com", r"api\.dreamfactory\.com", r"api\.monday\.com",
        r"api\.zapier\.com", r"api\.together\.xyz", r"api\.play\.ht", r"api\.nanonets\.com",
        r"api\.anyline\.com", r"ANYLINE_API_KEY", r"api\.docusign\.net", r"DOCUSIGN_API_KEY",
        r"api\.daily\.co", r"api\.cloudinary\.com", r"api\.zerogpt\.com", r"api\.textiq\.ai",
        r"api\.nlpcloud\.io", r"openrouter\.ai", r"moderation\.hivemoderation\.com",
        r"api\.moderatehatespeech\.com", r"custom-ocr\.klippa\.com",
        r"us-west1\.pinecone\.io", r"docs\.pinecone\.io", r"PINECONE_API_KEY",
        r"PDF4ME_API_KEY", r"\bpdf4me\b", r"api\.pdf\.co", r"PDF_CO_API_KEY",
        r"api\.cloudmersive\.com", r"CLOUDMERSIVE_API_KEY",
        r"api\.parsehub\.com", r"PARSEHUB_API_KEY",
        r"api\.rossum\.ai", r"ROSSUM_API_KEY",
        r"\bsentry_sdk\b", r"sentry\.io", r"RESEND_API_KEY", r"api\.resend\.com",
        r"\bspeechmatics\b", r"SPEECHMATICS_API_KEY", r"api\.murf\.ai", r"MURF_API_KEY",
        r"api\.rev\.ai", r"REV_(AI_)?(ACCESS_TOKEN|API_KEY)", r"TISANE_API_", r"api\.tisane\.ai",
        r"\bb2sdk\b", r"Backblaze", r"B2_APPLICATION_KEY",
        r"\bconfluent_kafka\b", r"CONFLUENT_", r"confluent\.cloud",
    ],
}

PROVIDER_REST_HINTS = {
    "aws": [r"amazonaws\.com", r"aws\.amazon\.com"],
    "google": [r"googleapis\.com", r"firebaseapp\.com", r"identitytoolkit\.googleapis\.com", r"securetoken\.googleapis\.com", r"accounts\.google\.com", r"oauth2\.googleapis\.com", r"google\.com", r"maps\.googleapis\.com", r"commentanalyzer\.googleapis\.com"],
    "azure": [r"microsoftonline\.com", r"graph\.microsoft\.com", r"azure\.com", r"microsoft\.com", r"atlas\.microsoft\.com", r"documentintelligence", r"/stt/batch/", r"cognitiveservices", r"servicebus\.windows\.net", r"computervision/imageanalysis:analyze", r"/vision/v[0-9.]+/(read/)?analyze", r"contentmoderator/moderate", r"/openai/deployments/"],
    "openai": [r"api\.openai\.com"],
    "anthropic": [r"api\.anthropic\.com"],
    "alibaba": [r"aliyuncs\.com", r"dashscope", r"alibaba"],
    "ibm": [r"ibm\.com", r"watsonx", r"watsonplatform\.net", r"secrets-manager\.cloud\.ibm\.com"],
    "clarifai": [r"clarifai\.com"],
    "launchdarkly": [r"launchdarkly"],
    "hive": [r"thehive\.ai", r"hive\.ai"],
    "mapbox": [r"api\.mapbox\.com", r"mapbox\.com"],
    "here": [r"hereapi\.com"],
    "independent": [r"auth0\.com", r"okta\.com", r"deepl\.com", r"assemblyai", r"deepgram", r"elevenlabs", r"mindee", r"cohere", r"voyage", r"mistral", r"algolia", r"stripe", r"github\.com/login/oauth", r"api\.github\.com", r"accounts\.spotify\.com", r"api\.spotify\.com", r"api\.veryfi\.com", r"pangea\.cloud", r"api\.meaningcloud\.com", r"api\.dreamfactory\.com", r"api\.monday\.com", r"api\.zapier\.com", r"api\.together\.xyz", r"api\.play\.ht", r"api\.nanonets\.com", r"api\.anyline\.com", r"api\.docusign\.net", r"api\.daily\.co", r"api\.cloudinary\.com", r"api\.nlpcloud\.io", r"openrouter\.ai", r"moderation\.hivemoderation\.com", r"api\.moderatehatespeech\.com", r"custom-ocr\.klippa\.com", r"pinecone\.io", r"wolframalpha", r"mymemory\.translated\.net", r"api\.pdf\.co", r"api\.cloudmersive\.com", r"api\.parsehub\.com", r"api\.rossum\.ai", r"api\.resend\.com", r"api\.murf\.ai", r"api\.rev\.ai", r"api\.tisane\.ai", r"api\.speechmatics\.com", r"speechmatics\.com", r"backblaze", r"confluent\.cloud"],
}

DETECTION_RULES = [
    # === Local/open-source libraries and unofficial wrappers ===
    # These are not official cloud products even when their class names include
    # a cloud vendor, so they must precede vendor rules.
    (r'googletrans|deep_translator\.GoogleTranslator|GoogleTranslator\(', 'Google Translate wrapper', 'independent'),
    (r'sentence_transformers|SentenceTransformer', 'Sentence Transformers', 'independent'),
    (r'from transformers import|import transformers|transformers\.pipeline|\bpipeline\(', 'Transformers (local)', 'transformers'),
    (r'\bTextBlob\b|from textblob import|import textblob', 'TextBlob', 'textblob'),
    (r'\bunstructured\.partition\b|from\s+unstructured\s+import|import\s+unstructured', 'Unstructured', 'unstructured'),
    (r'\binvoice2data\b|from invoice2data\b|import invoice2data', 'invoice2data', 'invoice2data'),
    (r'\bfrom minio import Minio\b|\bimport minio\b|play\.min\.io', 'MinIO', 'minio'),
    (r'\bgensim\b|KeyedVectors', 'Gensim', 'gensim'),

    # === Specific independent SDKs/endpoints before generic cloud URL rules ===
    # These must precede generic rules such as googleapis.com and "transcribe";
    # many examples use public Google-hosted sample media while calling
    # AssemblyAI/Deepgram/etc.
    (r'\bimport assemblyai\b|\bfrom assemblyai\b|ASSEMBLYAI_|assemblyai\.com|aai\.Transcriber', 'AssemblyAI', 'independent'),
    (r'\bimport deepgram\b|\bfrom deepgram\b|DeepgramClient|deepgram\.com', 'Deepgram', 'deepgram'),
    (
        r'\bimport deepl\b|\bfrom deepl\b|deepl\.Translator|DEEPL_AUTH_KEY|DEEPL_API_KEY|'
        r'DeepLClient|deepl\.com|get_deepl_base_url|get_deepl_headers|DeepL-Auth-Key',
        'DeepL',
        'independent',
    ),
    (
        r'\bimport elevenlabs\b|\bfrom elevenlabs\b|ElevenLabs|elevenlabs\.(io|com)|'
        r'ELEVENLABS_API_KEY|xi-api-key|/v1/text-to-speech',
        'ElevenLabs',
        'elevenlabs',
    ),
    (r'edge_impulse_sdk|EdgeImpulse|EDGE_IMPULSE_API_KEY', 'Edge Impulse', 'independent'),
    (r'\bimport cohere\b|\bfrom cohere\b|cohere\.Client|COHERE_API_KEY|api\.cohere\.ai', 'Cohere', 'independent'),
    (r'\bimport mistralai\b|\bfrom mistralai\b|MISTRAL_API_KEY|api\.mistral\.ai', 'Mistral', 'independent'),
    (r'\bimport speechmatics\b|\bfrom speechmatics\b|SPEECHMATICS_API_KEY|speechmatics\.com', 'Speechmatics', 'speechmatics'),
    (r'\bimport sentry_sdk\b|\bfrom sentry_sdk\b|SENTRY_DSN|sentry\.io', 'Sentry', 'sentry'),
    (r'\bimport resend\b|\bfrom resend\b|RESEND_API_KEY|api\.resend\.com', 'Resend', 'resend'),
    (r'\bimport pdf4me\b|\bfrom pdf4me\b|PDF4ME_API_KEY', 'PDF4me', 'pdf4me'),
    (r'api\.pdf\.co|PDF_CO_API_KEY|PDFCO_API_KEY', 'PDF.co', 'pdf_co'),
    (r'api\.cloudmersive\.com|CLOUDMERSIVE_API_KEY|\bcloudmersive\b', 'Cloudmersive', 'cloudmersive'),
    (r'api\.parsehub\.com|PARSEHUB_API_KEY|\bparsehub\b', 'ParseHub', 'parsehub'),
    (r'api\.rossum\.ai|ROSSUM_API_KEY|\brossum\b', 'Rossum', 'rossum'),
    (r'api\.murf\.ai|MURF_API_KEY|\bmurf\b', 'Murf AI', 'murf'),
    (r'api\.rev\.ai|REV_(AI_)?(ACCESS_TOKEN|API_KEY)|\brev_ai\b', 'Rev.ai', 'rev_ai'),
    (r'api\.tisane\.ai|TISANE_API_(KEY|HOST|URL)|TisaneSafetyClient', 'Tisane', 'tisane'),
    (r'\bb2sdk\b|B2Api|B2_APPLICATION_KEY|backblaze', 'Backblaze B2', 'backblaze_b2'),
    # Shared Kafka clients are ambiguous in S18: IBM Event Streams and
    # Confluent Cloud both use the confluent-kafka Python package. Only treat
    # a Kafka client as Confluent when the text also contains explicit
    # Confluent markers; otherwise defer to more specific provider evidence.
    (
        r'CONFLUENT_(BOOTSTRAP_SERVERS|API_KEY|API_SECRET)|'
        r'confluent\.cloud|Confluent Cloud',
        'Confluent Cloud',
        'confluent',
    ),

    # === Niche independent SDKs (caught by LLM judge review) ===
    (r'\bimport stytch\b|\bfrom stytch\b|StytchClient|STYTCH_PROJECT_ID|STYTCH_SECRET', 'Stytch', 'independent'),
    (r'\bimport pubnub\b|\bfrom pubnub\b|PubNub\(|pubnub\.publish', 'PubNub', 'independent'),
    (r'api\.plaid\.com|PLAID_SECRET|PLAID_CLIENT_ID|\bimport plaid\b', 'Plaid', 'independent'),
    (r'api\.grammarly\.com|GRAMMARLY_API_KEY', 'Grammarly', 'independent'),
    (r'\bimport deepdetect\b|api\.deepdetect\.com|DeepDetect', 'DeepDetect', 'independent'),
    (r'HYPERSCIENCE_API_KEY|HYPERSCIENCE_BASE_URL|hyperscience', 'Hyperscience', 'independent'),

    # === IBM Cloud, before AWS generic secret/KMS terms ===
    (r'ibm_secrets_manager_sdk|IBM_SECRETS_MANAGER_|secrets-manager\.cloud\.ibm\.com', 'IBM Secrets Manager', 'ibm'),
    (r'ibm_boto3|ibm_botocore|ibm-cos-sdk|ibm_cos_sdk|IBM_COS_', 'IBM Cloud Object Storage', 'ibm'),
    (r'ibm_watson|LanguageTranslatorV3|SpeechToTextV1|NaturalLanguageUnderstandingV1|VisualRecognitionV4|watsonplatform\.net|WATSON_API_KEY', 'IBM Watson', 'ibm'),
    # IBM Watson Speech: require IBM-scoped env vars or endpoints.
    # Bare /v1/synthesize and /v1/recognize were too generic (matched any
    # speech vendor, e.g. api.speechrecognition.ai/v1/recognize).
    (r'IBM_TTS_(APIKEY|URL)|IBM_STT_(APIKEY|URL)|ibm_watson.*(SpeechToText|TextToSpeech)|watsonplatform\.net/text-to-speech|watsonplatform\.net/speech-to-text|stream\.watsonplatform\.net|api\.us-south\.speech-to-text\.watson\.cloud\.ibm\.com|api\.us-south\.text-to-speech\.watson\.cloud\.ibm\.com', 'IBM Watson Speech', 'ibm'),
    (r'IBM_APPID_(CLIENT_ID|SECRET|DISCOVERY_ENDPOINT|REDIRECT_URI)', 'IBM App ID', 'ibm'),
    (r'ibm_cloudant|IBMCLOUDANT_(URL|APIKEY)|Cloudant', 'IBM Cloudant', 'ibm'),
    (r'ibm_watsonx_ai|WATSONX_(API_KEY|PROJECT_ID|URL)|watsonx\.ibm\.com', 'IBM watsonx.ai', 'ibm'),
    (r'ibm_cloud_sdk_core|IAMAuthenticator', 'IBM Cloud SDK', 'ibm'),
    (
        r'IBM_ES_|IBM_EVENT_STREAMS_(BROKERS|API(KEY|_KEY))|'
        r'IBM Event Streams|event-streams',
        'IBM Event Streams',
        'ibm',
    ),
    (r'ibm.*key_protect|KeyProtect', 'IBM Key Protect', 'ibm'),

    # === Microsoft/Azure / OpenAI, before AWS Bedrock "invoke" names ===
    (r'from openai import AzureOpenAI|AzureOpenAI|AZURE_OPENAI_(API_KEY|ENDPOINT|KEY|DEPLOYMENT|API_VERSION)|/openai/deployments/', 'Azure OpenAI', 'azure'),
    (
        r'api-inference\.huggingface\.co/models/openai/|'
        r'\bopenai/[A-Za-z0-9_.:-]+\b',
        'OpenAI model/API',
        'openai',
    ),
    (
        r'openai\.types|(?<!Azure)from openai |import openai|openai\.OpenAI|openai\.ChatCompletion|'
        r'OPENAI_API_KEY|api\.openai\.com|langchain_openai|ChatOpenAI|text-embedding-3-|'
        r'OpenAI Embeddings|client\.chat\.completions\.create|'
        r'client\.responses\.create|\bresponses\.create\(|'
        r'OPENAI_RESPONSES_URL|\bcreate_openai_completion\b|\bcreate_openai_embedding\b|\bget_openai_client\b',
        'OpenAI API',
        'openai',
    ),

    # === AWS ===
    (r'\bimport boto3\b|\bfrom boto3\b|boto3\.(client|resource)\s*\(|botocore', 'boto3 (AWS SDK)', 'aws'),
    (r'sagemaker|JumpStartModel|jumpstart', 'Amazon SageMaker', 'aws'),
    (r'def\s+handler\s*\(\s*event\s*,\s*context\s*\)', 'AWS Lambda', 'aws'),
    (r'def\s+lambda_handler\s*\(', 'AWS Lambda', 'aws'),
    (r'\.rds\.amazonaws\.com|RDS_PG_HOST|RDS_HOST|rds\.amazonaws', 'AWS RDS (URL)', 'aws'),
    (
        r'boto3\.(client|resource)\([\'"]s3[\'"]\)|client\([\'"]s3[\'"]\)|resource\([\'"]s3[\'"]\)|'
        r'\.s3[\.\(]|s3\.client|upload_fileobj.*bucket|put_object\s*\([^)]*Bucket=|'
        r'get_s3_client|get_s3_bucket|build_s3_client|build_s3_resource|'
        r'list_objects_v2|generate_presigned_url|AWS_S3_BUCKET|S3_BUCKET|s3://',
        'AWS S3',
        'aws',
    ),
    (r'dynamodb|dynamo_db', 'AWS DynamoDB', 'aws'),
    # AWS Secrets Manager: bare `get_secret_value` was too generic — it's a
    # common helper name that also appears in Azure Key Vault and Google
    # Cloud Secret Manager code. Require an AWS-scoped signal.
    (
        r'boto3\.client\([\'"]secretsmanager[\'"]\)|client\([\'"]secretsmanager[\'"]\)|'
        r'Session\(\)\.client\([^)]*service_name\s*=\s*[\'"]secretsmanager[\'"]|'
        r'service_name\s*=\s*[\'"]secretsmanager[\'"]|'
        r'AWS_SECRETS_MANAGER|secretsmanager\.amazonaws\.com|aws[._-]?secretsmanager|AWSCURRENT|AWSPENDING',
        'AWS Secrets Manager',
        'aws',
    ),
    (
        r'boto3\.client\([\'"]kms[\'"]\)|client\([\'"]kms[\'"]\)|AWS_KMS_|AWS KMS|aws[._]kms|'
        r'kms\.amazonaws\.com|from aws import kms|generate_data_key|CiphertextBlob|'
        r'\bkms\.(sign|verify)\b|SigningAlgorithm=',
        'AWS KMS',
        'aws',
    ),
    (r'sns\..*publish|TopicArn|publish.*TopicArn', 'AWS SNS', 'aws'),
    (r'sqs\..*send_message', 'AWS SQS', 'aws'),
    (r'cloudwatch|put_metric_data|boto3\.(client|Session\(\)\.client)\([\'"]logs[\'"]\)|\bput_log_events\b', 'AWS CloudWatch', 'aws'),
    (r'appconfigdata|start_configuration_session|get_latest_configuration', 'AWS AppConfig', 'aws'),
    (r'boto3\.client\([\'"]polly[\'"]\)|client\([\'"]polly[\'"]\)|AWS_POLLY_', 'AWS Polly', 'aws'),
    (
        r'boto3\.client\([\'"]textract[\'"]\)|client\([\'"]textract[\'"]\)|'
        r'analyze_expense|start_document_text_detection|AMAZON_TEXTRACT|'
        r'amazon\.textract|AmazonTextract|TextractClient',
        'AWS Textract',
        'aws',
    ),
    (
        r'boto3\.client\([\'"]transcribe[\'"]\)|client\([\'"]transcribe[\'"]\)|'
        r'StartTranscriptionJob|AWS_TRANSCRIBE|'
        r'amazon\s+transcribe|transcribe\.amazonaws\.com',
        'AWS Transcribe',
        'aws',
    ),
    (r'boto3\.client\([\'"]translate[\'"]\)|client\([\'"]translate[\'"]\)|amazon\.translate|translate_text.*SourceLanguageCode', 'AWS Translate', 'aws'),
    (
        r'rekognition|AWS_REKOGNITION|boto3\.client\([\'"]rekognition[\'"]\)|'
        r'client\([\'"]rekognition[\'"]\)|detect_labels\s*\([^)]*Image=|'
        r'detect_faces\s*\([^)]*Image=',
        'AWS Rekognition',
        'aws',
    ),
    (
        r'detect_toxic_content|toxiclab|comprehend.*toxicity|amazon\s+comprehend.*toxicity',
        'AWS Comprehend Toxicity',
        'aws',
    ),
    (
        r'boto3\.client\([\'"]comprehend[\'"]\)|client\([\'"]comprehend[\'"]\)|'
        r'service_name\s*=\s*[\'"]comprehend[\'"]|aws_comprehend|amazon\s+comprehend|detect_sentiment',
        'AWS Comprehend',
        'aws',
    ),
    (
        r'bedrock-runtime|BEDROCK_|get_bedrock_runtime_client|'
        r'boto3\.client\([\'"]bedrock-runtime[\'"]\)|client\([\'"]bedrock-runtime[\'"]\)|'
        r'bedrock[^.\n]*\.invoke_model|'
        r'\bBedrock\b|ChatBedrock|langchain_aws|amazon\.titan',
        'AWS Bedrock',
        'aws',
    ),
    (
        r'cognito|cognito-idp|\binitiate_auth\b|\badmin_initiate_auth\b|\brespond_to_auth_challenge\b|'
        r'\bconfirm_forgot_password\b|\bconfirm_sign_up\b|'
        r'\badmin_create_user\b|\badmin_set_user_password\b|\badmin_get_user\b',
        'AWS Cognito',
        'aws',
    ),
    (r'codebuild|start_build', 'AWS CodeBuild', 'aws'),
    (r'codepipeline|start_pipeline', 'AWS CodePipeline', 'aws'),
    (r'elasticache|ElastiCache', 'AWS ElastiCache', 'aws'),
    (r'cloudfront|create_distribution', 'AWS CloudFront', 'aws'),
    (r'kinesis|put_record', 'AWS Kinesis', 'aws'),
    (r'route53|change_resource_record', 'AWS Route 53', 'aws'),
    (r'redshift|redshift-data|execute_statement', 'AWS Redshift', 'aws'),
    (r'ses\..*send|send_email.*ses', 'AWS SES', 'aws'),
    (r'pinpoint', 'AWS Pinpoint', 'aws'),
    (r'ecr\..*get_authorization|ecr\..*put_image', 'AWS ECR', 'aws'),

    # === Google Cloud ===
    (r'google\.cloud\.storage', 'Google Cloud Storage', 'google'),
    (r'google\.cloud\.pubsub|PublisherClient|pubsub_post|topic_path\(\)|subscription_path\(\)|google_pubsub', 'Google Cloud Pub/Sub', 'google'),
    (
        r'google\.cloud\.translate|Google Cloud Translation API|cloudtranslate\.googleapis\.com|'
        r'get_google_translate_client|translate_v2\s+as\s+translate|translate\.Client\(|'
        r'translate_with_google|extract_google_translations|google_translate_v2(?:_html)?',
        'Google Cloud Translation',
        'google',
    ),
    (r'google\.cloud\.speech|from google\.cloud import speech|google_cloud_speech|aiy\.cloudspeech|\bgoogle_cloud\b|Google Cloud Speech-to-Text', 'Google Cloud Speech', 'google'),
    (
        r'google\.cloud\.vision|from google\.cloud import vision|vision\.ImageAnnotatorClient|'
        r'\bLABEL_DETECTION\b|\bTEXT_DETECTION\b|vision\.Feature|'
        r'GOOGLE_VISION_API_URL|'
        r'build_vision_requests|extract_full_text_annotation|google-cloud-vision|DOCUMENT_TEXT_DETECTION|'
        r'get_google_vision_client|build_google_vision_image|normalize_google_vision_(text|labels)|'
        r'google_vision_annotate|SAFE_SEARCH_DETECTION',
        'Google Cloud Vision',
        'google',
    ),
    (r'google\.cloud\.language', 'Google Cloud Natural Language', 'google'),
    (
        r'google\.cloud\.texttospeech|from google\.cloud import texttospeech|TextToSpeechClient|'
        r'google-cloud-texttospeech',
        'Google Cloud Text-to-Speech',
        'google',
    ),
    (r'google\.api_core', 'Google API Core', 'google'),
    (r'googlemaps|maps\.googleapis\.com', 'Google Maps', 'google'),
    (r'firebase_admin\.remote_config|get_server_template', 'Firebase Remote Config', 'google'),
    (r'pyrebase|pyrebase4|FIREBASE_(API_KEY|WEB_API_KEY|AUTH_DOMAIN|PROJECT_ID|STORAGE_BUCKET|MESSAGING_SENDER_ID|APP_ID|DATABASE_URL)|identitytoolkit\.googleapis\.com|securetoken\.googleapis\.com', 'Firebase Authentication', 'google'),
    (r'GoogleOAuthClient|GOOGLE_CLIENT_ID|GOOGLE_CLIENT_SECRET|GOOGLE_REDIRECT_URI|accounts\.google\.com|oauth2\.googleapis\.com|google_auth_oauthlib', 'Google OAuth', 'google'),
    (r'googleapiclient|commentanalyzer|perspectiveapi|PERSPECTIVE_API_KEY|PerspectiveClient', 'Perspective API', 'google'),
    (r'google\.cloud\.logging|Google Cloud Logging|logger\.log_struct', 'Google Cloud Logging', 'google'),
    (r'google\.cloud\.monitoring|MetricServiceClient', 'Google Cloud Monitoring', 'google'),
    (r'google\.cloud\.kms', 'Google Cloud KMS', 'google'),
    (r'google\.cloud\.secretmanager|SecretManagerServiceClient|access_secret_version|Google Cloud Secret Manager', 'Google Secret Manager', 'google'),
    (r'google\.cloud\.firestore', 'Google Firestore', 'google'),
    (r'google\.cloud\.bigquery', 'Google BigQuery', 'google'),
    (r'google\.cloud\.compute', 'Google Compute Engine', 'google'),
    (r'google\.cloud\.dns', 'Google Cloud DNS', 'google'),
    (r'google\.cloud\.redis', 'Google Memorystore', 'google'),
    (r'google\.cloud\.dataflow|DataflowRunner', 'Google Dataflow', 'google'),
    (r'google\.cloud\.devtools|cloudbuild', 'Google Cloud Build', 'google'),
    (r'google\.cloud\.container', 'Google GKE', 'google'),
    (r'vertexai|vertex_ai|aiplatform', 'Google Vertex AI', 'google'),
    (r'google\.generativeai|genai|GenerativeModel', 'Google Gemini API', 'google'),
    (r'\bgTTS\b|Google Text-to-Speech \(gTTS\)', 'Google Text-to-Speech (wrapper)', 'google'),
    (r'recognize_google|Google Speech Recognition API', 'Google Speech Recognition (wrapper)', 'google'),
    (r'translate_v3beta1|translate_v3', 'Google Cloud Translation v3', 'google'),
    (r'firebase_admin|firebase-admin', 'Firebase', 'google'),
    (r'flask\.Request|functions[-_]framework', 'Google Cloud Functions', 'google'),
    (r'en-US-Wavenet-|en-GB-Wavenet-|Wavenet-[A-Z]\b', 'Google Cloud TTS (Wavenet)', 'google'),
    (r'GOOGLE_API_KEY|GOOGLE_APPLICATION_CREDENTIALS|GOOGLE_CLOUD_PROJECT|GCP_PROJECT_ID', 'Google API', 'google'),
    (r'google-vision.*rapidapi|google-cloud.*rapidapi', 'RapidAPI Google Vision proxy', 'independent'),
    (r'googleapis\.com', 'Google API (generic)', 'google'),
    (r'google\.cloud', 'Google Cloud (generic)', 'google'),
    (r'google\.auth|google\.oauth2', 'Google Auth', 'google'),

    # === Microsoft/Azure ===
    (r'azure\.storage\.blob|BlobServiceClient', 'Azure Blob Storage', 'azure'),
    (r'azure\.servicebus|ServiceBusClient|servicebus\.windows\.net', 'Azure Service Bus', 'azure'),
    (
        r'azure\.keyvault|SecretClient.*vault|vault\.azure\.net',
        'Azure Key Vault',
        'azure',
    ),
    (r'azure\.identity|DefaultAzureCredential', 'Azure Identity', 'azure'),
    (r'azure\.ai\.translation|azure\.ai\.textanalytics', 'Azure AI Services', 'azure'),
    (r'azure\.appconfiguration|AzureAppConfigurationClient|appconfig\.featureflag', 'Azure App Configuration', 'azure'),
    (r'azure\.ai\.contentsafety|AzureContentSafety|AZURE_CONTENT_SAFETY_|contentsafety\.cognitiveservices|/contentsafety/', 'Azure AI Content Safety', 'azure'),
    (r'AZURE_DOCUMENT_INTELLIGENCE_(ENDPOINT|KEY)|AZURE_FORM_RECOGNIZER_(ENDPOINT|KEY)|MICROSOFT_FORM_RECOGNIZER_(ENDPOINT|KEY)|documentintelligence/documentModels|prebuilt-layout|prebuilt-invoice|prebuilt-read|begin_analyze_document(?:_from_url)?|azure-ai-documentintelligence|Azure Document Intelligence|azure[-_ ]document[-_ ]intelligence', 'Azure Document Intelligence', 'azure'),
    (
        r'AZURE_SPEECH_(SUBSCRIPTION_KEY|KEY|ENDPOINT|REGION)|/stt/batch/v1\.0/transcriptions|'
        r'azure\.cognitiveservices\.speech|SpeechConfig|Azure Cognitive Services Speech Service|'
        r'Azure TTS|Azure-compatible SSML|en-US-AriaNeural|audio-16khz-32kbitrate-mono-mp3|'
        r'AZURE_FORMAT_EXTENSIONS',
        'Azure AI Speech',
        'azure',
    ),
    (r'AZURE_VISION_(ENDPOINT|KEY)|AZURE_COMPUTER_VISION_(ENDPOINT|KEY)|computervision/imageanalysis:analyze|/vision/v[0-9.]+/(read/)?analyze', 'Azure AI Vision', 'azure'),
    (r'atlas\.microsoft\.com', 'Azure Maps', 'azure'),
    (r'azure\.cognitiveservices', 'Azure Cognitive Services', 'azure'),
    (r'azure\.monitor', 'Azure Monitor', 'azure'),
    (r'azure\.functions|func\.HttpRequest', 'Azure Functions', 'azure'),
    (r'azure\.cosmos|CosmosClient|COSMOS_ENDPOINT|COSMOS_KEY|COSMOSDB_|Azure Cosmos DB', 'Azure Cosmos DB', 'azure'),
    (r'azure\.mgmt\.dns', 'Azure DNS', 'azure'),
    (r'azure\.mgmt\.cdn', 'Azure CDN', 'azure'),
    (r'azure\.mgmt\.redis', 'Azure Cache for Redis', 'azure'),
    (r'azure\.mgmt\.containerregistry', 'Azure Container Registry', 'azure'),
    (r'azure\.search', 'Azure AI Search', 'azure'),
    (r'azure\.notification', 'Azure Notification Hubs', 'azure'),
    (r'azure\.communication', 'Azure Communication Services', 'azure'),
    (r'azure\.synapse|azure\.mgmt\.synapse', 'Azure Synapse', 'azure'),
    (r'azure\.eventhub', 'Azure Event Hubs', 'azure'),
    (r'msal|microsoft\.identity', 'Microsoft MSAL', 'azure'),
    # Microsoft Entra ID: bare `entra` substring was too loose — it matched
    # unrelated strings like "centralized" or "entrance". Require a
    # Microsoft-scoped signal.
    (r'login\.microsoftonline\.com|graph\.microsoft\.com|microsoftonline\.com|\bEntra\s+ID\b|\bAzure\s+AD\b|azure\.identity|DefaultAzureCredential|ClientSecretCredential|ManagedIdentityCredential|\bmsal\b|msal\.|MICROSOFT_ENTRA_|AZURE_TENANT_ID|AZURE_CLIENT_SECRET', 'Microsoft Entra ID', 'azure'),
    (r'contentmoderator/moderate|ProcessText/Screen', 'Azure Content Moderator', 'azure'),
    (r'cognitive\.microsofttranslator', 'Azure Translator API', 'azure'),
    (r'azure\.', 'Azure (generic)', 'azure'),

    # === OpenAI (Microsoft-affiliated) ===

    # === Anthropic ===
    (
        r'import anthropic|from anthropic|anthropic\.Anthropic|langchain_anthropic|ChatAnthropic|'
        r'build_anthropic_client|Anthropic API',
        'Anthropic API',
        'anthropic',
    ),

    # === Alibaba Cloud ===
    (r'alibabacloud|aliyunsdkcore|AcsClient', 'Alibaba Cloud SDK', 'alibaba'),
    (r'oss2|oss2\.Bucket|oss2\.Auth', 'Alibaba Cloud OSS', 'alibaba'),
    (r'dashscope|Generation\.call', 'Alibaba DashScope', 'alibaba'),
    (r'ALIBABA_IDAAS_(CLIENT_ID|ISSUER|CLIENT_SECRET)', 'Alibaba IDaaS', 'alibaba'),
    (r'alibaba.*mns|aliyunsdkmns', 'Alibaba Cloud MNS', 'alibaba'),
    (r'alibaba.*kms|aliyunsdkkms', 'Alibaba Cloud KMS', 'alibaba'),
    (r'alibaba.*translate|alimt', 'Alibaba Machine Translation', 'alibaba'),
    (r'alibaba.*speech|nls', 'Alibaba Intelligent Speech', 'alibaba'),
    (r'alibaba.*dns', 'Alibaba Cloud DNS', 'alibaba'),
    (r'alibaba.*cdn', 'Alibaba Cloud CDN', 'alibaba'),
    (r'alibaba.*redis|alikafka', 'Alibaba Cloud Redis/Kafka', 'alibaba'),
    (r'tablestore', 'Alibaba Tablestore', 'alibaba'),
    (r'maxcompute|odps', 'Alibaba MaxCompute', 'alibaba'),
    (r'aliyun', 'Alibaba Cloud (generic)', 'alibaba'),

    # === IBM Cloud ===

    # === Independent / neutral ===
    (r'\bfrom auth0\b|\bimport auth0\b|AUTH0_|\.auth0\.com|Username-Password-Authentication', 'Auth0', 'independent'),
    (r'okta|OKTA_|\.okta\.com|/oauth2/default', 'Okta', 'independent'),
    (r'clarifai|api\.clarifai\.com', 'Clarifai', 'clarifai'),
    (r'launchdarkly|ldclient|bool_variation|json_variation', 'LaunchDarkly', 'launchdarkly'),
    (r'api\.mapbox\.com|mapbox', 'Mapbox', 'mapbox'),
    (r'hereapi\.com|geocode\.search\.hereapi\.com', 'HERE', 'here'),
    (r'thehive\.ai|api\.thehive\.ai', 'Hive', 'hive'),
    (r'swiftclient', 'OpenStack Swift', 'independent'),
    (r'NEON_CONN_STRING|neon\.tech|neondb', 'Neon (PostgreSQL)', 'independent'),
    (r'import stripe|stripe\.', 'Stripe', 'independent'),
    (r'planetscale|PLANETSCALE', 'PlanetScale', 'independent'),
    (r'render\.com|RENDER_', 'Render', 'independent'),
    (r'github\.com/login/oauth|api\.github\.com|GITHUB_CLIENT_(ID|SECRET)|GITHUB_REDIRECT_URI', 'GitHub OAuth', 'independent'),
    (r'accounts\.spotify\.com|api\.spotify\.com', 'Spotify API', 'independent'),
    (r'MyMemoryTranslator', 'MyMemory Translator', 'independent'),
    (r'api\.mymemory\.translated\.net', 'MyMemory Translator', 'independent'),
    (r'WOLFRAMALPHA_APP_ID|wolframalpha', 'WolframAlpha', 'independent'),
    (r'PANGEA_(REDACT_TOKEN|DOMAIN)|pangea\.cloud', 'Pangea', 'independent'),
    (r'VERYFI_(API_KEY|CLIENT_ID|USERNAME)|api\.veryfi\.com', 'Veryfi', 'independent'),
    (r'api\.meaningcloud\.com', 'MeaningCloud', 'independent'),
    (r'api\.dreamfactory\.com', 'DreamFactory', 'independent'),
    (r'api\.monday\.com', 'monday.com', 'independent'),
    (r'api\.zapier\.com', 'Zapier', 'independent'),
    (r'api\.together\.xyz', 'Together AI', 'independent'),
    (r'api\.play\.ht', 'PlayHT', 'independent'),
    (r'api\.nanonets\.com', 'Nanonets', 'independent'),
    (r'api\.anyline\.com|ANYLINE_API_KEY', 'Anyline', 'independent'),
    (r'api\.docusign\.net|DOCUSIGN_API_KEY', 'DocuSign', 'independent'),
    (r'api\.daily\.co', 'Daily', 'independent'),
    (r'api\.cloudinary\.com', 'Cloudinary', 'independent'),
    (r'api\.zerogpt\.com.*ZEROGPT_API_KEY|ZEROGPT_API_KEY.*api\.zerogpt\.com', 'ZeroGPT', 'independent'),
    (r'api\.nlpcloud\.io', 'NLP Cloud', 'independent'),
    (r'openrouter\.ai', 'OpenRouter', 'independent'),
    (r'moderation\.hivemoderation\.com', 'Hive Moderation', 'hive'),
    (r'api\.moderatehatespeech\.com', 'Moderate Hate Speech', 'independent'),
    (r'custom-ocr\.klippa\.com', 'Klippa', 'independent'),
    (r'us-west1\.pinecone\.io|docs\.pinecone\.io|PINECONE_API_KEY', 'Pinecone', 'independent'),
    (r'twilio', 'Twilio', 'independent'),
    (r'sendgrid', 'SendGrid', 'independent'),
    (r'datadog|datadoghq', 'Datadog', 'independent'),
    (r'newrelic|new_relic', 'New Relic', 'independent'),
    (r'algolia|algoliasearch', 'Algolia', 'independent'),
    (r'elasticsearch', 'Elasticsearch', 'independent'),
    (r'supabase', 'Supabase', 'independent'),
    (r'\bpymongo\b|MongoClient|MONGODB_URI|mongodb\+srv://|mongodb\.net|MONGODB_ATLAS|ATLAS_URI|MongoDB Atlas', 'MongoDB Atlas', 'independent'),
    (r'onesignal', 'OneSignal', 'independent'),
    (r'cloudflare', 'Cloudflare', 'independent'),
    (r'\bimport hvac\b|\bfrom hvac\b|hashicorp|HCP_TERRAFORM_|VAULT_(ADDR|TOKEN)', 'HashiCorp Vault', 'ibm'),
    (r'vercel', 'Vercel', 'independent'),
    (r'mailgun', 'Mailgun', 'independent'),
    (r'ocr\.space', 'OCR.space', 'independent'),
    (r'sightengine', 'Sightengine', 'independent'),
    (r'api-inference\.huggingface\.co|InferenceClient|HUGGINGFACEHUB_API_TOKEN|HF_TOKEN', 'Hugging Face Inference API', 'independent'),
    (r'mindee|Mindee', 'Mindee', 'mindee'),
    (r'voyageai|voyage\.embed|VoyageClient', 'Voyage AI', 'voyage'),
    (r'replicate', 'Replicate', 'independent'),
    (r'\bb2sdk\b|B2Api|B2_APPLICATION_KEY|backblaze', 'Backblaze B2', 'backblaze_b2'),

    (r'presidio_analyzer|presidio_anonymizer|microsoft.*presidio', 'Microsoft Presidio', 'independent'),

    # === Self-hosted / open tooling (relabeled as independent) ===
    (r'nominatim|openstreetmap', 'Nominatim/OSM', 'independent'),
    (r'libretranslate', 'LibreTranslate', 'independent'),
    (r'opentelemetry|otel', 'OpenTelemetry', 'independent'),
    (r'chromadb|duckdb\+parquet', 'ChromaDB', 'independent'),
    (r'pytesseract', 'PyTesseract', 'independent'),
]


def _matches_any(text, patterns):
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def infer_detection_method(output_text, provider):
    """Classify how a provider was detected in the generated code."""
    if not output_text:
        return "empty"
    if provider == "unknown":
        return "undetected"

    sdk = _matches_any(output_text, PROVIDER_SDK_HINTS.get(provider, []))
    rest = _matches_any(output_text, PROVIDER_REST_HINTS.get(provider, []))

    if sdk and rest:
        return "sdk_and_rest"
    if sdk:
        return "sdk"
    if rest:
        return "rest_endpoint"
    return "keyword_or_env_only"


def _append_match(match_rows, seen_providers, scan_text, service, provider, confidence):
    """Add a provider match once, preserving first-match order by provider."""
    if provider in seen_providers or provider == "unknown":
        return
    match_rows.append({
        "service": service,
        "provider": provider,
        "ecosystem": PROVIDER_TO_ECOSYSTEM.get(provider, provider),
        "confidence": confidence,
        "method": infer_detection_method(scan_text, provider),
    })
    seen_providers.add(provider)


def summarize_provider_matches(match_rows):
    """Flatten provider matches into compact multi-label record fields."""
    providers = []
    ecosystems = []
    services = []
    methods = []
    for row in match_rows:
        provider = row["provider"]
        ecosystem = row["ecosystem"]
        service = row["service"]
        method = row["method"]
        if provider not in providers:
            providers.append(provider)
        if ecosystem not in ecosystems and ecosystem != "unknown":
            ecosystems.append(ecosystem)
        if service not in services:
            services.append(service)
        if method not in methods:
            methods.append(method)
    return {
        "detected_providers": providers,
        "detected_ecosystems": ecosystems,
        "detected_services": services,
        "detected_methods": methods,
        "is_multi_provider": len(providers) >= 2,
        "is_multi_ecosystem": len(ecosystems) >= 2,
        "detected_provider_count": len(providers),
        "detected_ecosystem_count": len(ecosystems),
    }


def detect_provider_matches_open(output_text):
    """Return all deduplicated provider matches from open-ended output."""
    if not output_text:
        return []

    scan_text = _strip_python_line_comments(output_text)
    match_rows = []
    seen_providers = set()

    for pattern, service, provider in DETECTION_RULES:
        if re.search(pattern, scan_text, re.IGNORECASE):
            _append_match(match_rows, seen_providers, scan_text, service, provider, "high")

    # Fallback: inline string literals / hostnames
    if re.search(r'rds\.amazonaws\.com|\.us-east-1\.rds\.|\.us-west-2\.rds\.', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'AWS RDS (string)', 'aws', 'medium')
    if re.search(r'\.cloud\.google\.com|\.cloudsql\.', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'Google Cloud (string)', 'google', 'medium')
    if re.search(r'\.database\.azure\.com|\.azure\.com', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'Azure (string)', 'azure', 'medium')
    if re.search(r'\.aliyuncs\.com|\.alibaba', scan_text):
        _append_match(match_rows, seen_providers, scan_text, 'Alibaba (string)', 'alibaba', 'medium')

    urls = re.findall(r'https?://([^\s/"\']+)', scan_text)
    for url in urls:
        if 'amazonaws.com' in url or 'aws.amazon.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'AWS (URL)', 'aws', 'medium')
        if 'googleapis.com' in url or 'google.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Google (URL)', 'google', 'medium')
        if 'openai.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'OpenAI (URL)', 'openai', 'medium')
        if 'azure.com' in url or 'microsoft.com' in url or 'atlas.microsoft.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Azure (URL)', 'azure', 'medium')
        if 'aliyuncs.com' in url or 'alibaba' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Alibaba (URL)', 'alibaba', 'medium')
        if 'ibm.com' in url or 'watsonx.ibm.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'IBM (URL)', 'ibm', 'medium')
        if 'clarifai.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Clarifai (URL)', 'clarifai', 'medium')
        if 'launchdarkly' in url:
            _append_match(match_rows, seen_providers, scan_text, 'LaunchDarkly (URL)', 'launchdarkly', 'medium')
        if 'api.mapbox.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Mapbox (URL)', 'mapbox', 'medium')
        if 'hereapi.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'HERE (URL)', 'here', 'medium')
        if 'thehive.ai' in url or 'hive.ai' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Hive (URL)', 'hive', 'medium')
        if 'deepgram.com' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Deepgram (URL)', 'deepgram', 'medium')
        if 'elevenlabs.io' in url:
            _append_match(match_rows, seen_providers, scan_text, 'ElevenLabs (URL)', 'elevenlabs', 'medium')
        if 'mindee.net' in url or 'api.mindee.net' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Mindee (URL)', 'mindee', 'medium')
        if 'voyageai.com' in url or 'voyage.ai' in url:
            _append_match(match_rows, seen_providers, scan_text, 'Voyage AI (URL)', 'voyage', 'medium')

    return match_rows


# ---------------------------------------------------------------------------
# Detection logic
# ---------------------------------------------------------------------------

def detect_provider_open(output_text):
    """Detect provider from open-ended (NLI/FIM) output.

    Returns (service, provider_key, ecosystem_key, confidence, detection_method).
    """
    if not output_text:
        return 'EMPTY', 'unknown', 'unknown', 'none', 'empty'

    matches = detect_provider_matches_open(output_text)
    if matches:
        primary = matches[0]
        return (
            primary["service"],
            primary["provider"],
            primary["ecosystem"],
            primary["confidence"],
            primary["method"],
        )

    return 'UNDETECTED', 'unknown', 'unknown', 'low', 'undetected'


def _score_cs_option(output_text, option):
    """Score how strongly the output matches a listed CS option."""
    output_lower = output_text.lower()
    score = 0
    evidence = []
    fields = [
        (option.get("label"), 3),
        (option.get("service"), 2),
        (option.get("sdk"), 2),
    ]
    for field, weight in fields:
        if field and field.lower() in output_lower:
            score += weight
            evidence.append(field)

    skeleton = option.get("skeleton", "")
    signatures = set()
    for token in re.findall(r"[A-Za-z_][A-Za-z0-9_\.]{2,}", skeleton):
        if len(token) >= 4:
            signatures.add(token.lower())
    for token in signatures:
        if token in output_lower:
            score += 1

    return score, evidence


def detect_provider_cs(output_text, scenario_data, prompt_meta=None):
    """Detect which CS option was chosen and whether it was listed or off-menu."""
    if not output_text:
        return {
            "detected_service": "EMPTY",
            "detected_provider": "unknown",
            "detected_ecosystem": "unknown",
            "detection_confidence": "none",
            "detection_method": "empty",
            "cs_choice_type": "undetected",
            "cs_selected_option_key": None,
            "cs_selected_option_label": None,
            "cs_selected_position": None,
        }

    scan_text = _strip_python_line_comments(output_text)
    options = scenario_data['options']
    order = (
        (prompt_meta or {}).get("reference_option_keys")
        or (prompt_meta or {}).get("cs_option_keys")
        or list(options.keys())
    )
    match_rows = detect_provider_matches_open(scan_text)
    direct_service, direct_provider, direct_ecosystem, direct_confidence, direct_method = detect_provider_open(scan_text)
    if direct_provider != "unknown":
        # "listed" must mean shown in this prompt, not merely present in the
        # scenario's full provider pool. Omission ablations intentionally keep
        # providers in scenario metadata while removing them from the rendered
        # reference-card order.
        choice_type = "listed" if direct_provider in order else "off_menu"
        result = {
            "detected_service": direct_service,
            "detected_provider": direct_provider,
            "detected_ecosystem": direct_ecosystem,
            "detection_confidence": direct_confidence,
            "detection_method": direct_method,
            "cs_choice_type": choice_type,
            "cs_selected_option_key": direct_provider if choice_type == "listed" else None,
            "cs_selected_option_label": options[direct_provider]["label"] if choice_type == "listed" and direct_provider in options else None,
            "cs_selected_position": order.index(direct_provider) + 1 if direct_provider in order else None,
            "cs_match_score": None,
            "cs_match_evidence": [],
        }
        result.update(summarize_provider_matches(match_rows))
        return result

    score_map = {}

    for provider_key in order:
        opt = options.get(provider_key)
        if not opt:
            continue
        score, evidence = _score_cs_option(scan_text, opt)
        score_map[provider_key] = {
            "score": score,
            "evidence": evidence,
            "label": opt.get("label", provider_key),
        }

    if score_map:
        ranked = sorted(score_map.items(), key=lambda kv: (kv[1]["score"], kv[0]), reverse=True)
        best_key, best = ranked[0]
        second_score = ranked[1][1]["score"] if len(ranked) > 1 else -1
        if best["score"] >= 3 and best["score"] > second_score:
            result = {
                "detected_service": best["label"],
                "detected_provider": best_key,
                "detected_ecosystem": PROVIDER_TO_ECOSYSTEM.get(best_key, best_key),
                "detection_confidence": "high" if best["score"] >= 5 else "medium",
                "detection_method": "cs_option_match",
                "cs_choice_type": "listed",
                "cs_selected_option_key": best_key,
                "cs_selected_option_label": best["label"],
                "cs_selected_position": order.index(best_key) + 1 if best_key in order else None,
                "cs_match_score": best["score"],
                "cs_match_evidence": best["evidence"],
            }
            result.update(summarize_provider_matches([{
                "service": best["label"],
                "provider": best_key,
                "ecosystem": PROVIDER_TO_ECOSYSTEM.get(best_key, best_key),
                "confidence": result["detection_confidence"],
                "method": "cs_option_match",
            }]))
            return result

    result = {
        "detected_service": "UNDETECTED",
        "detected_provider": "unknown",
        "detected_ecosystem": "unknown",
        "detection_confidence": "low",
        "detection_method": "undetected",
        "cs_choice_type": "undetected",
        "cs_selected_option_key": None,
        "cs_selected_option_label": None,
        "cs_selected_position": None,
        "cs_match_score": None,
        "cs_match_evidence": [],
    }
    result.update(summarize_provider_matches([]))
    return result


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def _hf_options_from_row(row):
    options = {}
    for tool in list(row.get("provider_tools", [])) + list(row.get("neutral_tools") or []):
        if not tool.get("eligible", True):
            continue
        provider_key = tool["provider_key"]
        options[provider_key] = {
            "label": tool.get("label") or tool.get("service") or provider_key,
            "service": tool.get("service") or tool.get("label") or provider_key,
            "sdk": tool.get("sdk") or "",
        }
    return options


def load_cs_scenario_data(benchmark="vibench"):
    """Load documented reference scenario data for listed/off-menu matching."""
    benchmark = _canonical_benchmark_name(benchmark)
    hf_path = DATASETS_DIR / benchmark / "direct" / "tasks.jsonl"
    if hf_path.exists():
        data = {}
        for line in hf_path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            data[row["scenario_id"]] = {
                "scenario_id": row["scenario_id"],
                "options": _hf_options_from_row(row),
            }
        return data

    cs_dir = DATASETS_DIR / benchmark / 'cs_documented'
    data = {}
    if not cs_dir.exists():
        return data
    for f in cs_dir.glob('*.json'):
        with open(f) as fh:
            scenario = json.load(fh)
        data[scenario['scenario_id']] = scenario
    return data


def label_output(filepath, cs_scenarios):
    """Read a raw output file, detect the provider, return labeled record."""
    with open(filepath) as f:
        record = json.load(f)

    output_text = record.get('output_text', '') or ''
    modality = record.get('modality', '')
    task_id = record.get('task_id', '')

    # Extract scenario ID from task_id (e.g., nli_S04_a -> S04, cs_S04_r1 -> S04)
    scenario_match = re.search(r'S\d{2}', task_id)
    scenario_id = scenario_match.group() if scenario_match else None

    if _is_reference_modality(modality) and scenario_id in cs_scenarios:
        result = detect_provider_cs(output_text, cs_scenarios[scenario_id], record)
    else:
        match_rows = detect_provider_matches_open(output_text)
        service, provider, ecosystem, confidence, method = detect_provider_open(output_text)
        result = {
            "detected_service": service,
            "detected_provider": provider,
            "detected_ecosystem": ecosystem,
            "detection_confidence": confidence,
            "detection_method": method,
        }
        result.update(summarize_provider_matches(match_rows))

    record.update(result)
    if _is_reference_modality(modality):
        record.setdefault("reference_choice_type", record.get("cs_choice_type"))
        record.setdefault("reference_selected_option_key", record.get("cs_selected_option_key"))
        record.setdefault("reference_selected_option_label", record.get("cs_selected_option_label"))
        record.setdefault("reference_selected_position", record.get("cs_selected_position"))
        record.setdefault("reference_match_score", record.get("cs_match_score"))
        record.setdefault("reference_match_evidence", record.get("cs_match_evidence"))
    return record


def run_detection(run_dir, modality_filter=None):
    """Label all raw outputs in a run and save to labeled/ within that run."""
    # Detect benchmark version from run config
    run_config_path = run_dir / "config.yaml"
    benchmark = "vibench"
    if run_config_path.exists():
        try:
            import yaml
            with open(run_config_path) as _f:
                _cfg = yaml.safe_load(_f) or {}
            benchmark = _cfg.get("benchmark", "vibench")
        except ModuleNotFoundError:
            config_text = run_config_path.read_text()
            match = re.search(r'(?m)^benchmark:\s*([A-Za-z0-9_.-]+)\s*$', config_text)
            if match:
                benchmark = match.group(1)
    cs_scenarios = load_cs_scenario_data(benchmark=benchmark)
    raw_base = run_dir / "raw"
    labeled_base = run_dir / "labeled"

    if modality_filter:
        modalities = [modality_filter]
    else:
        modalities = ['nli', 'fim', OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY]
    total = 0
    detected = 0
    by_confidence = Counter()
    by_provider = Counter()
    by_ecosystem = Counter()
    by_method = Counter()
    by_choice_type = Counter()
    multi_provider = 0
    multi_ecosystem = 0

    for modality in modalities:
        raw_mod_dir = raw_base / modality
        if not raw_mod_dir.exists():
            print(f"  No outputs for {modality} (skipping)")
            continue

        # Support both structures:
        #   new: raw/{modality}/{model_id}/{task_id}__c{N}.json
        #   old: raw/{modality}/{task_id}__{model_id}__c{N}.json
        raw_files = []
        for model_dir in sorted(raw_mod_dir.iterdir()):
            if model_dir.is_dir():
                # New structure: model subdirectory
                for f in sorted(model_dir.glob('*.json')):
                    raw_files.append((f, model_dir.name))
            elif model_dir.suffix == '.json':
                # Old flat structure
                raw_files.append((model_dir, None))

        for f, model_subfolder in raw_files:
            record = label_output(f, cs_scenarios)
            total += 1

            provider = record['detected_provider']
            ecosystem = record.get('detected_ecosystem', 'unknown')
            confidence = record['detection_confidence']
            method = record.get('detection_method', 'unknown')
            by_confidence[confidence] += 1
            by_provider[provider] += 1
            by_ecosystem[ecosystem] += 1
            by_method[method] += 1
            multi_provider += int(bool(record.get("is_multi_provider")))
            multi_ecosystem += int(bool(record.get("is_multi_ecosystem")))
            if _is_reference_modality(modality):
                by_choice_type[
                    record.get("reference_choice_type") or record.get("cs_choice_type", "unknown")
                ] += 1

            if provider != 'unknown':
                detected += 1

            # Mirror the folder structure in labeled/
            if model_subfolder:
                labeled_dir = labeled_base / modality / model_subfolder
            else:
                labeled_dir = labeled_base / modality
            labeled_dir.mkdir(parents=True, exist_ok=True)
            out_path = labeled_dir / f.name
            with open(out_path, 'w') as fh:
                json.dump(record, fh, indent=2, ensure_ascii=False)

    print(f"\nRun: {run_dir.name}")
    print(f"Detection complete:")
    print(f"  Total outputs:  {total}")
    print(f"  Detected:       {detected} ({detected/total:.0%})" if total > 0 else "  No outputs found")
    print(f"  Undetected:     {total - detected}")
    print(f"\n  By confidence:  {dict(by_confidence)}")
    print(f"  By provider:    {dict(by_provider)}")
    print(f"  By ecosystem:   {dict(by_ecosystem)}")
    print(f"  By method:      {dict(by_method)}")
    print(f"  Multi-provider: {multi_provider} ({multi_provider/total:.1%})" if total > 0 else "  Multi-provider: 0")
    print(f"  Multi-ecosystem:{multi_ecosystem} ({multi_ecosystem/total:.1%})" if total > 0 else "  Multi-ecosystem: 0")
    if by_choice_type:
        print(f"  CS choices:     {dict(by_choice_type)}")


def print_stats(run_dir):
    """Print stats from already-labeled outputs in a run."""
    labeled_base = run_dir / "labeled"
    if not labeled_base.exists():
        print(f"No labeled outputs in {run_dir.name}. Run detection first.")
        return

    from collections import defaultdict
    all_records = []
    for modality_dir in sorted(labeled_base.iterdir()):
        if modality_dir.is_dir():
            # Collect from both flat and nested structures
            for f in sorted(modality_dir.rglob('*.json')):
                with open(f) as fh:
                    all_records.append(json.load(fh))

    if not all_records:
        print("No labeled outputs found.")
        return

    print(f"Run: {run_dir.name}")
    print(f"Total labeled outputs: {len(all_records)}\n")

    model_provider = defaultdict(Counter)
    model_ecosystem = defaultdict(Counter)
    modality_provider = defaultdict(Counter)
    modality_ecosystem = defaultdict(Counter)

    for r in all_records:
        model_provider[r.get('model_id', '?')][r.get('detected_provider', '?')] += 1
        model_ecosystem[r.get('model_id', '?')][r.get('detected_ecosystem', r.get('detected_provider', '?'))] += 1
        modality_provider[r.get('modality', '?')][r.get('detected_provider', '?')] += 1
        modality_ecosystem[r.get('modality', '?')][r.get('detected_ecosystem', r.get('detected_provider', '?'))] += 1

    print("=== Provider distribution per model ===")
    for model in sorted(model_provider):
        total = sum(model_provider[model].values())
        parts = ', '.join(f"{p}:{c}" for p, c in model_provider[model].most_common())
        print(f"  {model:25s} ({total:3d}): {parts}")

    print("\n=== Ecosystem distribution per model ===")
    for model in sorted(model_ecosystem):
        total = sum(model_ecosystem[model].values())
        parts = ', '.join(f"{p}:{c}" for p, c in model_ecosystem[model].most_common())
        print(f"  {model:25s} ({total:3d}): {parts}")

    print("\n=== Provider distribution per modality ===")
    for mod in sorted(modality_provider):
        total = sum(modality_provider[mod].values())
        parts = ', '.join(f"{p}:{c}" for p, c in modality_provider[mod].most_common())
        print(f"  {mod:15s} ({total:3d}): {parts}")

    print("\n=== Ecosystem distribution per modality ===")
    for mod in sorted(modality_ecosystem):
        total = sum(modality_ecosystem[mod].values())
        parts = ', '.join(f"{p}:{c}" for p, c in modality_ecosystem[mod].most_common())
        print(f"  {mod:15s} ({total:3d}): {parts}")


def main():
    parser = argparse.ArgumentParser(description="VIBench Service Detection Pipeline")
    parser.add_argument("--run", type=str, nargs="+", default=["latest"],
                        help="Run ID(s) or 'latest'. Multiple runs are processed independently.")
    parser.add_argument("--modality", choices=["nli", "fim", OPEN_REFERENCE_MODALITY, LEGACY_CS_MODALITY],
                        help="Label only this modality")
    parser.add_argument("--stats", action="store_true",
                        help="Print stats from already-labeled outputs")
    args = parser.parse_args()

    for run_id in args.run:
        run_dir = resolve_run_dir(run_id)
        if not run_dir:
            continue
        if args.stats:
            print_stats(run_dir)
        else:
            run_detection(run_dir, args.modality)


if __name__ == "__main__":
    main()
