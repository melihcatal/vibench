PYTHON ?= python

# Hugging Face datasets used to distribute the large benchmark/results
# artifacts. GitHub tracks scripts/configs/docs; benchmark and output bundles
# live on HF.

DIRECT_RUN ?= direct/complete/full_5c
OPENCODE_RUN ?= agentic/complete/opencode_full_5c
AGENTS_SDK_RUN ?= agentic/complete/agents_sdk_full_5c
FIGURE_DIR ?= docs/figures/current
MPLCONFIGDIR ?= /tmp/matplotlib-vibench
EXPLORER_PORT ?= 8000
EXPLORER_ARGS ?=

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

# Versioned control-baseline bundle: lets a single new model be evaluated
# against the published control runs without re-running the controls.
BASELINE_ID ?= controls-2026q2
BASELINE_SOURCE_RUN ?= direct/complete/full_5c

.PHONY: help install env install-explorer install-analysis install-figures install-generation install-hf scenarios models runs browse explorer baseline-build eval-model validate snapshots snapshot-quality figures figures-svg audit-sample evaluate gini gini-all gini-vib gini-vib-prompts gen-smoke-all gen-smoke-direct gen-smoke-opencode gen-smoke-agents-sdk gen-model-all gen-direct-model gen-opencode-model gen-agents-sdk-model gen-direct-full gen-opencode-full gen-agents-sdk-full gen-proxies clean-cache

help:
	@printf "VIBench replication — code targets:\n"
	@printf "  make install              install everything\n"
	@printf "  make install-explorer     ... just Flask, for make explorer\n"
	@printf "  make install-analysis     ... just numpy, for the gini/appendix tables\n"
	@printf "  make install-figures      ... matplotlib + numpy, for make figures\n"
	@printf "  make install-generation   ... API clients, to produce new generations\n"
	@printf "  make install-hf           ... huggingface_hub, to read the HF mirrors\n"
	@printf "  make env                  create configs/.env from the template\n"
	@printf "  (browsing, make evaluate and the ablation tables need no packages at all)\n"
	@printf "  make scenarios            list the 20 benchmark scenarios\n"
	@printf "  make models               list the study models and their affiliations\n"
	@printf "  make runs                 list the runs present in outputs/\n"
	@printf "  make browse ARGS=...      show or compare generations (browse.py --help)\n"
	@printf "  make explorer             serve the offline explorer on EXPLORER_PORT\n"
	@printf "  make validate             validate benchmark alignment/evidence files\n"
	@printf "  make snapshots            refresh local provider-doc snapshots and audit quality\n"
	@printf "  make snapshot-quality     audit saved provider-doc snapshot quality only\n"
	@printf "  make figures              regenerate the high-resolution claude_*.png result charts\n"
	@printf "  make figures-svg          regenerate the compact SVG overview/multi-label charts\n"
	@printf "  make audit-sample         draw a fresh n=400 detector audit sample into outputs/audits/\n"
	@printf "  make evaluate             re-run direct + agentic evaluation on canonical runs\n"
	@printf "  make baseline-build       package a run's control outputs as outputs/control_sets/$(BASELINE_ID)/\n"
	@printf "  make eval-model MODEL=X   run + evaluate ONE registered model against a stored baseline\n"
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
	@printf "  make clean-cache          remove generated local caches\n"
	@printf "\nGeneration defaults: GEN_MODEL=$(GEN_MODEL), GEN_SCENARIO=$(GEN_SCENARIO), GEN_TASK=$(GEN_TASK), GEN_VARIANT=$(GEN_VARIANT), GEN_COMPLETIONS=$(GEN_COMPLETIONS)\n"
	@printf "\nInteractive browsing: https://huggingface.co/spaces/vibench-emnlp26/vibench\n"

# Reading the shipped results needs no third-party packages: browsing the
# benchmark, make evaluate, the ablation table generators and the validation
# report all run on the standard library. Install only what a task adds.
install:
	$(PYTHON) -m pip install -r requirements.txt

install-explorer:
	$(PYTHON) -m pip install -r requirements/explorer.txt

install-analysis:
	$(PYTHON) -m pip install -r requirements/analysis.txt

install-figures:
	$(PYTHON) -m pip install -r requirements/figures.txt

install-generation:
	$(PYTHON) -m pip install -r requirements/generation.txt

install-hf:
	$(PYTHON) -m pip install -r requirements/hf.txt

# Credentials for generating new outputs. Never overwrites an existing .env:
# that file holds live API keys and is not recoverable from the template.
env:
	@if [ -f configs/.env ]; then \
		echo "configs/.env already exists — leaving it untouched."; \
		echo "Edit it in place, or remove it first to start from the template."; \
	else \
		cp configs/.env.template configs/.env; \
		echo "Created configs/.env from configs/.env.template."; \
		echo "Fill in only the keys for the models you plan to run; see configs/README.md."; \
	fi

# Reading the benchmark and the generated outputs. These need the repository
# only; browse.py --help lists every selector.
scenarios:
	$(PYTHON) scripts/browse.py scenarios

models:
	$(PYTHON) scripts/browse.py models

runs:
	$(PYTHON) scripts/browse.py runs

browse:
	$(PYTHON) scripts/browse.py $(ARGS)

# The explorer reads the repository by default; pass EXPLORER_ARGS to point it
# at the Hugging Face mirrors instead.
explorer:
	$(PYTHON) explorer/server.py $(EXPLORER_PORT) \
		--benchmark-source local --results-source local $(EXPLORER_ARGS)

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

# Draws a fresh sample into outputs/audits/. It will not match the shipped
# n=400 sample: that one was drawn from a smaller pool and is the sample the
# reviewer CSVs annotate, so it is reference data rather than a build product.
audit-sample:
	$(PYTHON) scripts/audit/generate_audit_sample.py \
		--n 400 \
		--seed 42 \
		--strategy random \
		--out ../outputs/audits/vibench_detector_audit_fresh.jsonl

evaluate:
	$(PYTHON) scripts/evaluation/core/evaluate.py \
		--run $(DIRECT_RUN) \
		--format md \
		--output ../outputs/runs/$(DIRECT_RUN)/report.md
	$(PYTHON) scripts/evaluation/core/evaluate_agentic.py \
		--run $(OPENCODE_RUN) \
		--direct-run $(DIRECT_RUN)

gini:
	$(PYTHON) scripts/evaluation/gini/evaluate_gini.py --run $(DIRECT_RUN)

gini-all:
	$(PYTHON) scripts/evaluation/gini/evaluate_gini_matrix.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN)

gini-vib:
	$(PYTHON) scripts/evaluation/gini/generate_gini_vib_comparison.py \
		--direct-run $(DIRECT_RUN) \
		--agentic-run $(OPENCODE_RUN)

gini-vib-prompts:
	$(PYTHON) scripts/evaluation/gini/generate_prompt_gini_vib_tables.py \
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

clean-cache:
	rm -rf scripts/__pycache__ scripts/utils/__pycache__

# --- Versioned control baselines -------------------------------------------
# Package the control-model outputs of a run as outputs/control_sets/<id>/.
baseline-build:
	$(PYTHON) scripts/evaluation/baselines/build_control_baseline.py \
		--run $(BASELINE_SOURCE_RUN) \
		--id $(BASELINE_ID)

# Generate and evaluate ONE newly registered model against a stored baseline,
# without re-running the controls.
eval-model:
	@test -n "$(MODEL)" || { echo "Usage: make eval-model MODEL=<registered-model-id> [BASELINE_ID=$(BASELINE_ID)]"; exit 1; }
	$(PYTHON) scripts/generation/run_direct.py \
		--config configs/vibench/direct/complete/full_5c.yaml \
		--model $(MODEL) \
		--name eval/$(MODEL) \
		--skip-from both \
		--retry-errors \
		--retry-empty
	$(PYTHON) scripts/evaluation/core/evaluate.py \
		--run eval/$(MODEL) \
		--baseline $(BASELINE_ID) \
		--format md
