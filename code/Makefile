PYTHON ?= python

# Hugging Face datasets used to distribute the large benchmark/results
# artifacts. GitHub tracks scripts/configs/docs; benchmark and output bundles
# live on HF.
HF_USER ?= vibench-emnlp26
HF_BENCHMARK_REPO ?= $(HF_USER)/vibench
HF_RESULTS_REPO ?= $(HF_USER)/vibench-results

DIRECT_RUN ?= direct/complete/full_5c
OPENCODE_RUN ?= agentic/complete/opencode_full_5c
AGENTS_SDK_RUN ?= agentic/complete/agents_sdk_full_5c
FIGURE_DIR ?= docs/figures/current
MPLCONFIGDIR ?= /tmp/matplotlib-vibench

GEN_MODEL ?= gpt-5.4-mini
GEN_SCENARIO ?= S18
GEN_TASK ?= $(GEN_SCENARIO)
GEN_VARIANT ?= both
GEN_COMPLETIONS ?= 1
ifndef GEN_RUN_ROOT
GEN_RUN_ROOT := scratch/smoke_$(shell date +%Y%m%d_%H%M%S)
endif
GEN_DIRECT_SMOKE_RUN ?= $(GEN_RUN_ROOT)/direct_$(GEN_MODEL)_$(GEN_SCENARIO)
GEN_OPENCODE_SMOKE_RUN ?= $(GEN_RUN_ROOT)/opencode_$(GEN_MODEL)_$(GEN_TASK)
GEN_AGENTS_SDK_SMOKE_RUN ?= $(GEN_RUN_ROOT)/agents_sdk_$(GEN_MODEL)_$(GEN_TASK)
GEN_DIRECT_MODEL_RUN ?= reruns/direct_$(GEN_MODEL)_full_5c
GEN_OPENCODE_MODEL_RUN ?= reruns/agentic_opencode_$(GEN_MODEL)_full_5c
GEN_AGENTS_SDK_MODEL_RUN ?= reruns/agentic_agents_sdk_$(GEN_MODEL)_full_5c
GEN_DIRECT_FULL_RUN ?= reruns/direct_full_5c
GEN_OPENCODE_FULL_RUN ?= reruns/agentic_opencode_full_5c
GEN_AGENTS_SDK_FULL_RUN ?= reruns/agentic_agents_sdk_full_5c

.PHONY: help install validate snapshots snapshot-quality figures figures-svg audit-sample evaluate gini gini-all gini-vib gini-vib-prompts gen-smoke-all gen-smoke-direct gen-smoke-opencode gen-smoke-agents-sdk gen-model-all gen-direct-model gen-opencode-model gen-agents-sdk-model gen-direct-full gen-opencode-full gen-agents-sdk-full gen-proxies hf-stage hf-upload-benchmark hf-upload-results hf-upload clean-cache

help:
	@printf "VIBench replication — code targets:\n"
	@printf "  make install              install Python dependencies\n"
	@printf "  make validate             validate benchmark alignment/evidence files\n"
	@printf "  make snapshots            refresh local provider-doc snapshots and audit quality\n"
	@printf "  make snapshot-quality     audit saved provider-doc snapshot quality only\n"
	@printf "  make figures              regenerate the high-resolution claude_*.png result charts\n"
	@printf "  make figures-svg          regenerate the compact SVG overview/multi-label charts\n"
	@printf "  make audit-sample         regenerate the seeded n=400 detector audit sample\n"
	@printf "  make evaluate             re-run direct + agentic evaluation on canonical runs\n"
	@printf "  make gini                 compute paper-style provider Gini indices for direct NLI results\n"
	@printf "  make gini-all             compute Gini indices across all direct and agentic prompt settings\n"
	@printf "  make gini-vib             compare per-model Gini and VIB with bootstrap intervals\n"
	@printf "  make gini-vib-prompts     build prompt-specific normalized-GI and VIB CI tables\n"
	@printf "  make gen-smoke-all        run small API generation checks for direct + both agentic runners\n"
	@printf "  make gen-smoke-direct     run one-scenario direct generation smoke check\n"
	@printf "  make gen-smoke-opencode   run one-task OpenCode agentic smoke check\n"
	@printf "  make gen-smoke-agents-sdk run one-task Agents SDK agentic smoke check\n"
	@printf "  make gen-model-all        run full direct + both agentic configs for one GEN_MODEL\n"
	@printf "  make gen-direct-model     run study direct config for one GEN_MODEL\n"
	@printf "  make gen-opencode-model   run study OpenCode config for one GEN_MODEL\n"
	@printf "  make gen-agents-sdk-model run study Agents SDK config for one GEN_MODEL\n"
	@printf "  make gen-proxies          start LiteLLM proxies for OpenCode Nova/Granite routes\n"
	@printf "  make gen-direct-full      run study direct generation into reruns/\n"
	@printf "  make gen-opencode-full    run study OpenCode generation into reruns/\n"
	@printf "  make gen-agents-sdk-full  run study Agents SDK generation into reruns/\n"
	@printf "  make hf-stage             stage HF benchmark/results upload folders (optional)\n"
	@printf "  make hf-upload            upload staged benchmark and results datasets (optional)\n"
	@printf "  make clean-cache          remove generated local caches\n"
	@printf "\nGeneration defaults: GEN_MODEL=$(GEN_MODEL), GEN_SCENARIO=$(GEN_SCENARIO), GEN_TASK=$(GEN_TASK), GEN_VARIANT=$(GEN_VARIANT), GEN_COMPLETIONS=$(GEN_COMPLETIONS)\n"
	@printf "\nInteractive browsing: https://huggingface.co/spaces/vibench-emnlp26/vibench\n"

install:
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/benchmark/validate_vibench_alignment.py

snapshots:
	$(PYTHON) scripts/benchmark/snapshot_provider_docs.py
	$(PYTHON) scripts/benchmark/check_snapshot_quality.py

snapshot-quality:
	$(PYTHON) scripts/benchmark/check_snapshot_quality.py

figures:
	MPLCONFIGDIR=$(MPLCONFIGDIR) $(PYTHON) scripts/plotting/plot_vibench_claude_charts.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN) \
		--output-root docs/figures

figures-svg:
	MPLCONFIGDIR=$(MPLCONFIGDIR) $(PYTHON) scripts/plotting/plot_vibench_overview_charts.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN) \
		--output-dir $(FIGURE_DIR)
	MPLCONFIGDIR=$(MPLCONFIGDIR) $(PYTHON) scripts/plotting/plot_vibench_multilabel_charts.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN) \
		--output-dir $(FIGURE_DIR)

audit-sample:
	$(PYTHON) scripts/audit/generate_audit_sample.py \
		--n 400 \
		--seed 42 \
		--strategy random \
		--out benchmark/vibench/audit/vibench_detector_audit.jsonl

evaluate:
	$(PYTHON) scripts/evaluation/evaluate.py \
		--run $(DIRECT_RUN) \
		--format md \
		--output outputs/runs/$(DIRECT_RUN)/report.md
	$(PYTHON) scripts/evaluation/evaluate_agentic.py \
		--run $(OPENCODE_RUN) \
		--direct-run $(DIRECT_RUN)

gini:
	$(PYTHON) scripts/evaluation/evaluate_gini.py --run $(DIRECT_RUN)

gini-all:
	$(PYTHON) scripts/evaluation/evaluate_gini_matrix.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN)

gini-vib:
	$(PYTHON) scripts/evaluation/generate_gini_vib_comparison.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN)

gini-vib-prompts:
	$(PYTHON) scripts/evaluation/generate_prompt_gini_vib_tables.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN)

gen-smoke-all: gen-smoke-direct gen-smoke-opencode gen-smoke-agents-sdk

gen-smoke-direct:
	$(PYTHON) scripts/generation/run_direct.py \
		--config configs/vibench/direct/complete/full_5c.yaml \
		--name $(GEN_DIRECT_SMOKE_RUN) \
		--model $(GEN_MODEL) \
		--scenario $(GEN_SCENARIO) \
		--completions $(GEN_COMPLETIONS) \
		--sequential \
		-v

gen-smoke-opencode:
	$(PYTHON) scripts/generation/run_agentic.py \
		--config configs/vibench/agentic/complete/opencode_full_5c.yaml \
		--name $(GEN_OPENCODE_SMOKE_RUN) \
		--model $(GEN_MODEL) \
		--task $(GEN_TASK) \
		--variant $(GEN_VARIANT) \
		--completions $(GEN_COMPLETIONS) \
		--sequential \
		-v

gen-smoke-agents-sdk:
	$(PYTHON) scripts/generation/run_agentic_litellm_agents.py \
		--config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
		--name $(GEN_AGENTS_SDK_SMOKE_RUN) \
		--model $(GEN_MODEL) \
		--task $(GEN_TASK) \
		--variant $(GEN_VARIANT) \
		--completions $(GEN_COMPLETIONS) \
		--sequential \
		-v

gen-model-all: gen-direct-model gen-opencode-model gen-agents-sdk-model

gen-direct-model:
	$(PYTHON) scripts/generation/run_direct.py \
		--config configs/vibench/direct/complete/full_5c.yaml \
		--name $(GEN_DIRECT_MODEL_RUN) \
		--model $(GEN_MODEL) \
		--skip-from both \
		--retry-errors \
		--retry-empty

gen-opencode-model:
	$(PYTHON) scripts/generation/run_agentic.py \
		--config configs/vibench/agentic/complete/opencode_full_5c.yaml \
		--name $(GEN_OPENCODE_MODEL_RUN) \
		--model $(GEN_MODEL) \
		--retry-errors \
		--retry-empty \
		--retry-incomplete

gen-agents-sdk-model:
	$(PYTHON) scripts/generation/run_agentic_litellm_agents.py \
		--config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
		--name $(GEN_AGENTS_SDK_MODEL_RUN) \
		--model $(GEN_MODEL) \
		--retry-errors \
		--retry-empty \
		--retry-incomplete

gen-proxies:
	scripts/generation/start_litellm_proxies.sh

gen-direct-full:
	$(PYTHON) scripts/generation/run_direct.py \
		--config configs/vibench/direct/complete/full_5c.yaml \
		--name $(GEN_DIRECT_FULL_RUN) \
		--skip-from both \
		--retry-errors \
		--retry-empty

gen-opencode-full:
	$(PYTHON) scripts/generation/run_agentic.py \
		--config configs/vibench/agentic/complete/opencode_full_5c.yaml \
		--name $(GEN_OPENCODE_FULL_RUN) \
		--retry-errors \
		--retry-empty \
		--retry-incomplete

gen-agents-sdk-full:
	$(PYTHON) scripts/generation/run_agentic_litellm_agents.py \
		--config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
		--name $(GEN_AGENTS_SDK_FULL_RUN) \
		--retry-errors \
		--retry-empty \
		--retry-incomplete

hf-stage: figures
	$(PYTHON) scripts/utils/prepare_hf_upload.py --clean

hf-upload-benchmark: hf-stage
	hf upload $(HF_BENCHMARK_REPO) .hf_upload/vibench . \
		--type dataset \
		--private \
		--commit-message "Upload VIBench benchmark"

hf-upload-results: hf-stage
	hf upload-large-folder $(HF_RESULTS_REPO) .hf_upload/vibench-results \
		--type dataset \
		--private \
		--num-workers 8 \
		--no-bars

hf-upload: hf-upload-benchmark hf-upload-results

clean-cache:
	rm -rf .hf_upload scripts/__pycache__ scripts/utils/__pycache__
