"""Prepare only the new Microsoft/OpenAI condition, without editing old inputs."""
import argparse
import ast
import difflib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from ablations.shared.common import HERE, ablation_dir, encoded, sha
from ablations.shared.runtime import archived_inputs
from ablations.shared.scoring import detect_provider_from_file

BASE = Path(__file__).resolve().parents[1]
MODELS = ('gemini-2.5-flash', 'nova-pro', 'gpt-5.4-mini')
SCENARIOS = tuple(f'S{i:02d}' for i in range(1, 21))
PACKAGES = {
    'S01': ['msal', 'requests'], 'S02': ['msal'], 'S03': ['requests'], 'S04': ['requests'],
    'S05': ['azure-cognitiveservices-speech'], 'S06': ['azure-cognitiveservices-speech'],
    'S07': ['azure-ai-documentintelligence', 'azure-core'],
    'S08': ['azure-ai-documentintelligence', 'azure-core'],
    'S09': ['openai'], 'S10': ['openai'], 'S11': ['openai'],
    'S12': ['azure-ai-vision-imageanalysis', 'azure-core'],
    'S13': ['azure-ai-contentsafety', 'azure-core'],
    'S14': ['azure-storage-blob', 'azure-identity'], 'S15': ['azure-cosmos'],
    'S16': ['azure-keyvault-secrets', 'azure-identity'],
    'S17': ['azure-keyvault-keys', 'azure-identity'], 'S18': ['azure-servicebus'],
    'S19': ['azure-monitor-query==1.4.1', 'azure-identity'],
    'S20': ['azure-monitor-ingestion', 'azure-identity'],
}
NOTES = {
    'S01': 'Requires a configured External ID tenant, its issuer domain, and admin-consented Graph user-write permissions; administrative registration, not an identical self-signup/verification flow.',
    'S02': 'Retain returned state server-side and verify it on callback. Registered redirect URI, confidential application and consented scopes required.',
    'S04': 'Documented deviation from the bundle SDK: Azure Speech batch REST submits a URL asynchronously, matching the existing submit-only anchors. The SpeechRecognizer SDK operation is not an asynchronous batch-job submitter. Audio URL must be accessible to the service.',
    'S05': 'Caller supplies finite mono PCM16 microphone chunks. Recognition is event-driven; provider timing and partial transcripts differ.',
    'S07': 'Matched scan supported by prebuilt-read; cloud credentials required.',
    'S08': 'Invoice extraction retains source text and missing fields; equal accuracy is not assumed.',
    'S09': 'OpenAI API, not Azure; embedding coordinates/dimensions differ from other providers.',
    'S10': 'OpenAI API, not Azure; fixed gpt-5.4-mini service model. Access not live tested.',
    'S11': 'Azure OpenAI endpoint and deployment, not the public OpenAI endpoint. Supply an existing accessible chat deployment.',
    'S13': 'Maximum Azure category severity / 7 is a bounded safety proxy, not calibrated equivalence to Perspective toxicity.',
    'S15': 'Pre-existing Cosmos container partitioned on /id; writes replace the document and materialize its id.',
    'S17': 'Requires a 256-bit symmetric oct-HSM key in Azure Managed HSM with encrypt permission. IV/tag metadata is returned in addition to ciphertext; downstream decryption must retain it. Not a claim that all Key Vault key types support AES.',
    'S18': 'Pre-existing Service Bus topic; assigned message ID identifies the submitted message.',
    'S19': 'Historical evidence interface retained with azure-monitor-query==1.4.1; MetricsQueryClient is removed in version 2. Supply a resource ID and a scalar metric supporting Average aggregation.',
    'S20': 'Requires configured Data Collection Rule, stream and ingestion endpoint; event schema must match the rule.',
}
EXTRA_DOCS = {
    'S04': ['https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription-create'],
    'S17': ['https://learn.microsoft.com/en-us/python/api/azure-keyvault-keys/azure.keyvault.keys.crypto.cryptographyclient?view=azure-python'],
    'S19': ['https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme?view=azure-python'],
}


def desired_files():
    out = {}
    for scenario in SCENARIOS:
        task, system, agent_prompt, original = archived_inputs(scenario)
        source = HERE / 'paper_inputs' / scenario
        evidence = next(t for t in json.loads((source / 'scenario.json').read_text())['provider_tools']
                        if t['provider_key'] == 'microsoft_openai')
        if not evidence['eligible']:
            raise ValueError(f'Microsoft/OpenAI is not eligible for {scenario}')
        primary = task['primary_component_file']
        seed = (BASE / 'templates' / scenario / 'a1.py').read_text()
        ast.parse(seed)
        labels = detect_provider_from_file(seed)['detected_ecosystems']
        if set(labels) != {'microsoft_openai'}:
            raise ValueError(f'Unexpected seed attribution for {scenario}: {labels}')
        first, separator, rest = original.partition('\n')
        if not separator:
            raise ValueError('Expected a multiline archived prompt')
        for ablation, condition, notice in (
            ('1', 'anchor_microsoft_openai', f'The initial file {primary} is already implemented. Read it before generating the remaining files, and leave it unchanged.'),
            ('3', 'instruct_microsoft_openai', f'Implement the initial file {primary} using Microsoft/OpenAI.'),
        ):
            base = HERE / ablation_dir(ablation) / 'microsoft_openai/inputs' / scenario
            prompt = first + '\n' + notice + '\n' + rest
            out[base / 'prompt.txt'] = prompt
            out[base / 'system_prompt.txt'] = system
            out[base / 'opencode_agent_prompt.txt'] = agent_prompt
            out[base / 'agentic_task.json'] = encoded(task)
            out[base / 'metadata.json'] = encoded({
                'condition': condition, 'scenario': scenario, 'assigned_provider': 'microsoft_openai',
                'primary_file': primary, 'prompt_sha256': sha(prompt),
                'original_prompt_sha256': sha(original), 'system_sha256': sha(system),
                'task_sha256': sha(encoded(task)), 'seed_sha256': sha(seed) if ablation == '1' else None,
                'surface': 'openai' if scenario in ('S09', 'S10') else 'microsoft_azure',
                'surface_scope': 'A1 supplied implementation only; A3 instruction allows either surface of the merged ecosystem.',
                'evidence': evidence, 'packages': PACKAGES[scenario] if ablation == '1' else [],
                'implementation_notes': NOTES.get(scenario, 'Configured service credentials/resources required.') if ablation == '1' else None,
                'additional_docs': EXTRA_DOCS.get(scenario, []) if ablation == '1' else [],
                'validation': 'syntax, attribution and offline contracts; no live cloud-service execution' if ablation == '1' else 'archived prompt plus one provider-assignment sentence',
            })
            if ablation == '1':
                out[base / 'workspace' / primary] = seed
                out[base / 'requirements.txt'] = '\n'.join(PACKAGES[scenario]) + '\n'
            out[HERE / 'diffs' / ablation_dir(ablation) / f'{scenario}_{condition}.diff'] = ''.join(
                difflib.unified_diff(original.splitlines(keepends=True), prompt.splitlines(keepends=True),
                                     fromfile=f'original/{scenario}/prompt.txt', tofile=f'{condition}/{scenario}/prompt.txt'))
    return out


def materialize(files):
    conflicts = [str(path) for path, value in files.items() if path.exists() and path.read_text() != value]
    if conflicts:
        raise ValueError('Refusing to overwrite inputs: ' + ', '.join(conflicts[:5]))
    for path, value in files.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify all prepared files without writing')
    args = parser.parse_args()
    files = desired_files()
    if args.check:
        assert all(path.exists() and path.read_text() == value for path, value in files.items())
    else:
        materialize(files)
    print(f'Validated {len(files)} new-condition inputs/diffs. No model calls.')
