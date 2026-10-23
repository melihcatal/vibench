
# VIBench Evaluation Report (vibench)
Total labeled outputs: 15600
Models: 13
Modalities: ['fim', 'nli', 'reference_open']

## 1. Overall Direct Provider Recommendation Rates (FRR)
Headline rates use share-normalized multi-provider scoring: each file contributes total mass 1 split across all detected providers.
Model                            alibaba   anthropic         aws       azurebackblaze_b2    clarifaicloudmersive   confluent    deepgram       deepl     doppler  elevenlabs      google         ibm independent      mindee      openai      pdf4me      rev_ai      sentryspeechmatics      tisanetransformers     unknownunstructured
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
deepseek-v3.2                      0.5%       0.6%      29.2%      11.0%       0.0%       0.0%       0.0%       0.0%       0.7%       0.0%       0.0%       0.3%      32.0%       0.2%       7.2%       0.5%      17.8%       0.0%       0.0%       0.0%       0.0%       0.1%       0.0%       0.0%       0.0%
gemini-2.5-flash                   0.0%       0.6%      14.7%       9.7%       0.0%       0.1%       0.0%       0.0%       1.5%       0.0%       0.0%       0.6%      47.0%       0.1%      12.2%       0.5%      12.4%       0.0%       0.0%       0.0%       0.0%       0.2%       0.0%       0.4%       0.1%
gemini-2.5-pro                     0.2%       1.6%      22.4%      10.4%       0.0%       0.0%       0.0%       0.0%       3.9%       0.0%       0.0%       0.6%      23.8%       0.9%      25.1%       1.3%       9.5%       0.0%       0.0%       0.0%       0.0%       0.1%       0.0%       0.2%       0.0%
gpt-5.4                            0.2%       0.3%      25.4%       8.7%       0.0%       0.0%       0.0%       0.0%       2.0%       0.0%       0.0%       1.6%      21.2%       0.4%      19.2%       0.8%      19.0%       0.0%       0.0%       0.0%       0.0%       0.2%       0.0%       1.0%       0.0%
gpt-5.4-mini                       0.1%       0.5%      20.5%      10.4%       0.0%       0.0%       0.0%       0.0%       1.5%       0.0%       0.0%       1.5%      23.6%       0.4%      14.2%       0.0%      24.7%       0.0%       0.1%       0.0%       0.0%       0.0%       0.0%       2.6%       0.0%
granite-4.0-h-small                0.7%       1.0%      14.4%       4.5%       0.0%       0.4%       0.0%       0.0%       1.1%       0.0%       0.0%       0.4%      41.7%       3.2%      10.8%       0.8%      12.8%       0.1%       0.1%       0.2%       0.0%       0.0%       0.5%       7.5%       0.0%
granite-4.0-h-tiny-local           1.0%       0.0%      13.9%       9.1%       0.0%       0.4%       0.0%       0.7%       0.4%       0.0%       0.2%       0.0%      25.4%       2.8%       7.8%       0.8%      14.7%       0.0%       0.0%       0.0%       0.0%       0.8%       0.0%      22.0%       0.0%
grok-4-1-fast-reasoning            0.1%       0.1%      32.3%       7.3%       0.0%       0.0%       0.0%       0.0%       1.8%       0.0%       0.0%       0.8%      18.9%       0.0%      18.8%       1.0%      18.5%       0.0%       0.0%       0.0%       0.0%       0.0%       0.0%       0.2%       0.0%
mistral-large-3                    0.2%       2.2%      15.5%      17.2%       0.1%       0.2%       0.0%       0.0%       2.2%       0.0%       0.0%       1.1%      33.7%       0.4%      16.5%       0.8%       9.8%       0.0%       0.0%       0.0%       0.2%       0.0%       0.0%       0.0%       0.0%
nova-2-lite                        0.6%       1.2%      11.8%      12.2%       0.0%       0.8%       0.0%       0.0%       1.7%       0.1%       0.0%       0.8%      44.7%       0.8%      15.0%       2.1%       6.2%       0.0%       0.0%       0.0%       0.0%       0.2%       0.3%       1.6%       0.0%
nova-pro                           1.5%       0.2%      37.9%       9.7%       0.0%       0.3%       0.6%       0.0%       0.4%       0.0%       0.0%       0.2%      23.3%       1.7%      10.6%       0.2%      10.3%       0.0%       0.0%       0.0%       0.0%       0.1%       0.0%       3.0%       0.1%
qwen3-coder-flash                  3.3%       2.8%      23.7%      10.0%       0.0%       0.2%       0.0%       0.0%       1.2%       0.0%       0.0%       0.4%      32.3%       1.2%       8.4%       2.5%      13.3%       0.0%       0.0%       0.0%       0.0%       0.0%       0.0%       0.5%       0.0%
qwen3.6-plus                       0.2%       0.1%      28.5%       7.8%       0.0%       0.0%       0.0%       0.0%       2.2%       0.0%       0.0%       0.8%      16.1%       0.0%      22.4%       2.0%      19.9%       0.0%       0.0%       0.0%       0.0%       0.0%       0.0%       0.0%       0.0%

## 2. Overall Ecosystem Recommendation Rates (FRR)
Ecosystem rates use the same share-normalized scoring. Files with no detected provider contribute fully to `unknown`.

Model                                alibaba       anthropic             aws          google             ibm     independentMicrosoft/OpenAI         unknown
------------------------------------------------------------------------------------------------------------------------------------------------------------
deepseek-v3.2                          0.5%           0.6%          29.2%          32.0%           0.2%           8.8%          28.7%           0.0%
gemini-2.5-flash                       0.0%           0.6%          14.7%          47.0%           0.1%          15.2%          22.0%           0.4%
gemini-2.5-pro                         0.2%           1.6%          22.4%          23.8%           0.9%          31.0%          19.9%           0.2%
gpt-5.4                                0.2%           0.3%          25.4%          21.2%           0.4%          23.7%          27.7%           1.0%
gpt-5.4-mini                           0.1%           0.5%          20.5%          23.6%           0.4%          17.2%          35.1%           2.6%
granite-4.0-h-small                    0.7%           1.0%          14.4%          41.7%           3.2%          14.4%          17.3%           7.5%
granite-4.0-h-tiny-local               1.0%           0.0%          13.9%          25.4%           2.8%          11.1%          23.8%          22.0%
grok-4-1-fast-reasoning                0.1%           0.1%          32.3%          18.9%           0.0%          22.4%          25.9%           0.2%
mistral-large-3                        0.2%           2.2%          15.5%          33.7%           0.4%          21.0%          27.0%           0.0%
nova-2-lite                            0.6%           1.2%          11.8%          44.7%           0.8%          20.9%          18.5%           1.6%
nova-pro                               1.5%           0.2%          37.9%          23.3%           1.7%          12.5%          20.0%           3.0%
qwen3-coder-flash                      3.3%           2.8%          23.7%          32.3%           1.2%          12.8%          23.3%           0.5%
qwen3.6-plus                           0.2%           0.1%          28.5%          16.1%           0.0%          27.4%          27.7%           0.0%

## 3. Vertical Integration Bias Scores (VIB)
VIB = model's affiliated ecosystem FRR - strict neutral baseline average FRR for same ecosystem
Strict neutral baseline = deepseek-v3.2 + mistral-large-3 + grok-4-1-fast-reasoning
FRR here is share-normalized multi-provider mass, not first-hit single-label scoring.
Cohen's h uses the affiliated-model rate vs the same control baseline rate. Cutoffs: 0.2 small, 0.5 medium, 0.8 large.
VIB > 0 = affiliated preference above baseline

  gemini-2.5-flash             → google          : VIB = +18.8%  (self=47.0%, ctrl=28.2%, h=+0.39 small)  [POSITIVE]
  nova-pro                     → aws             : VIB = +12.2%  (self=37.9%, ctrl=25.6%, h=+0.26 small)  [POSITIVE]
  gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +7.9%  (self=35.1%, ctrl=27.2%, h=+0.17 negligible)  [POSITIVE]
  qwen3-coder-flash            → alibaba         : VIB = +3.1%  (self=3.3%, ctrl=0.3%, h=+0.26 small)  [~ZERO]
  granite-4.0-h-small          → ibm             : VIB = +2.9%  (self=3.2%, ctrl=0.2%, h=+0.26 small)  [~ZERO]
  granite-4.0-h-tiny-local     → ibm             : VIB = +2.6%  (self=2.8%, ctrl=0.2%, h=+0.24 small)  [~ZERO]
  gpt-5.4                      → Microsoft/OpenAI: VIB = +0.5%  (self=27.7%, ctrl=27.2%, h=+0.01 negligible)  [~ZERO]
  qwen3.6-plus                 → alibaba         : VIB = -0.0%  (self=0.2%, ctrl=0.3%, h=-0.01 negligible)  [~ZERO]
  gemini-2.5-pro               → google          : VIB = -4.5%  (self=23.8%, ctrl=28.2%, h=-0.10 negligible)  [~ZERO]
  nova-2-lite                  → aws             : VIB = -13.8%  (self=11.8%, ctrl=25.6%, h=-0.36 small)  [NEGATIVE]

## 3a. VIB Baseline Sensitivity
Primary VIB uses the strict neutral baseline (deepseek + mistral + grok). This table checks whether conclusions move when alternative neutral baselines are used.
Individual range = max-min VIB over each single neutral baseline model; large values indicate baseline-sensitive findings.

  strict_controls  : deepseek-v3.2, mistral-large-3, grok-4-1-fast-reasoning
  independent_only : none
  broad_neutral    : deepseek-v3.2, mistral-large-3, grok-4-1-fast-reasoning

  Model                                    Affil     Self    Strict     Indep     Broad   IndivRange
  --------------------------------------------------------------------------------------------------
  gemini-2.5-flash                        google   47.0%   +18.8%       n/a    +18.8%       14.8%
  nova-pro                                   aws   37.9%   +12.2%       n/a    +12.2%       16.8%
  gpt-5.4-mini                  Microsoft/OpenAI   35.1%    +7.9%       n/a     +7.9%        2.9%
  qwen3-coder-flash                      alibaba    3.3%    +3.1%       n/a     +3.1%        0.4%
  granite-4.0-h-small                        ibm    3.2%    +2.9%       n/a     +2.9%        0.4%
  granite-4.0-h-tiny-local                   ibm    2.8%    +2.6%       n/a     +2.6%        0.4%
  gpt-5.4                       Microsoft/OpenAI   27.7%    +0.5%       n/a     +0.5%        2.9%
  qwen3.6-plus                           alibaba    0.2%    -0.0%       n/a     -0.0%        0.4%
  gemini-2.5-pro                          google   23.8%    -4.5%       n/a     -4.5%       14.8%
  nova-2-lite                                aws   11.8%   -13.8%       n/a    -13.8%       16.8%

  Pairwise neutral-baseline spread by affiliated ecosystem:
  Ecosystem          Min pair rate Max pair rate    Spread              Min pair              Max pair
  ----------------------------------------------------------------------------------------------------
  aws                       22.3%         30.7%      8.4%    deepseek + mistral       grok + deepseek
  google                    25.5%         32.9%      7.4%       grok + deepseek    deepseek + mistral
  Microsoft/OpenAI          26.4%         27.9%      1.4%        grok + mistral    deepseek + mistral
  alibaba                    0.2%          0.4%      0.2%        grok + mistral    deepseek + mistral
  ibm                        0.1%          0.3%      0.2%       grok + deepseek    deepseek + mistral

  Exhaustive neutral-subset robustness (all non-empty subsets; order ignored):
  Neutral pool (3): deepseek-v3.2, mistral-large-3, grok-4-1-fast-reasoning
  Subsets per model: 7
  Model                           Strict                  Range    Median               h range     Pos     Neg
  -------------------------------------------------------------------------------------------------------------------
  gemini-2.5-flash               +18.8%        [+13.3%,+28.1%]   +18.8%         [+0.27,+0.61]     7/7     0/7
  nova-2-lite                    -13.8%         [-20.4%,-3.6%]   -13.8%         [-0.51,-0.11]     0/7     7/7
  nova-pro                       +12.2%         [+5.6%,+22.4%]   +12.2%         [+0.12,+0.52]     7/7     0/7
  gpt-5.4-mini                    +7.9%          [+6.3%,+9.2%]    +7.9%         [+0.14,+0.20]     7/7     0/7
  gemini-2.5-pro                  -4.5%         [-10.0%,+4.8%]    -4.5%         [-0.22,+0.12]     1/7     6/7
  qwen3-coder-flash               +3.1%          [+2.8%,+3.2%]    +3.1%         [+0.23,+0.31]     7/7     0/7
  granite-4.0-h-small             +2.9%          [+2.7%,+3.1%]    +2.9%         [+0.23,+0.32]     7/7     0/7
  granite-4.0-h-tiny-local        +2.6%          [+2.4%,+2.7%]    +2.6%         [+0.21,+0.30]     7/7     0/7
  gpt-5.4                         +0.5%          [-1.1%,+1.8%]    +0.5%         [-0.02,+0.04]     5/7     2/7
  qwen3.6-plus                    -0.0%          [-0.2%,+0.2%]    -0.0%         [-0.04,+0.04]     2/7     4/7

## 3b. Rival Ecosystem Avoidance / Negative Bias
Avoidance(A→B) = control-model rival-share for B minus affiliated-model rival-share for B.
Rival-share is competitor-conditional: among documented rival ecosystem mass (excluding the affiliated ecosystem, unknown, and independent options), how much goes to B?
Positive values mean under-selection of the rival ecosystem relative to controls; negative values mean over-selection.

Control baseline models: deepseek-v3.2, grok-4-1-fast-reasoning, mistral-large-3

Rows shown below require at least 300 affiliated-model exposures and 600 control-model exposures for the rival ecosystem.

Strongest rival under-selection:
  Model                                Affil             Rival   Avoid Δ     Model      Ctrl                95% CI        p          mass
  -----------------------------------------------------------------------------------------------------------------------------
  nova-2-lite                            aws  Microsoft/OpenAI   +19.8%     28.1%     47.9%       [+16.0%,+23.6%]        0    788.5/2044
  qwen3.6-plus                       alibaba            google   +12.1%     22.3%     34.3%        [+8.8%,+15.3%] 3.43e-13    867/2957.2
  granite-4.0-h-small                    ibm               aws   +12.0%     19.2%     31.2%        [+9.0%,+15.1%] 1.47e-14  898.9/2959.3
  granite-4.0-h-small                    ibm  Microsoft/OpenAI   +10.0%     23.1%     33.1%        [+6.8%,+13.3%] 1.15e-09  898.9/2959.3
  granite-4.0-h-tiny-local               ibm               aws    +9.5%     21.6%     31.2%        [+6.2%,+12.9%] 2.44e-08  769.2/2959.3
  gemini-2.5-flash                    google               aws    +8.0%     39.3%     47.3%        [+3.0%,+13.0%]  0.00184    449/1951.5
  gpt-5.4                     Microsoft/OpenAI            google    +6.4%     44.7%     51.1%        [+1.8%,+11.0%]  0.00678  570.5/1987.7
  gemini-2.5-pro                      google  Microsoft/OpenAI    +5.7%     44.5%     50.2%        [+1.0%,+10.5%]    0.018  536.5/1951.5
  nova-pro                               aws  Microsoft/OpenAI    +4.8%     43.1%     47.9%         [+0.1%,+9.4%]   0.0433    556.5/2044
  qwen3-coder-flash                  alibaba  Microsoft/OpenAI    +4.6%     28.5%     33.1%         [+1.3%,+7.9%]  0.00575    983/2957.2
  qwen3-coder-flash                  alibaba               aws    +2.3%     28.9%     31.2%         [-1.0%,+5.6%]    0.175    983/2957.2
  gpt-5.4-mini                Microsoft/OpenAI               aws    +0.7%     45.7%     46.4%         [-4.0%,+5.5%]    0.766    538/1987.7
  gemini-2.5-flash                    google           alibaba    +0.5%      0.0%      0.5%         [+0.2%,+0.8%]  0.00152    449/1951.5
  gpt-5.4-mini                Microsoft/OpenAI           alibaba    +0.3%      0.2%      0.5%         [-0.2%,+0.8%]    0.194    538/1987.7
  qwen3.6-plus                       alibaba               ibm    +0.3%      0.0%      0.3%         [+0.1%,+0.5%]  0.00506    753/2568.2
  gemini-2.5-flash                    google               ibm    +0.2%      0.3%      0.5%         [-0.4%,+0.8%]    0.473  395.5/1665.5
  gemini-2.5-pro                      google           alibaba    +0.1%      0.4%      0.5%         [-0.5%,+0.7%]    0.651  536.5/1951.5
  gpt-5.4                     Microsoft/OpenAI           alibaba    -0.0%      0.5%      0.5%         [-0.7%,+0.6%]    0.947  570.5/1987.7
  nova-2-lite                            aws           alibaba    -0.4%      0.9%      0.5%         [-1.1%,+0.3%]    0.279    788.5/2044
  nova-pro                               aws            google    -0.5%     50.2%     49.7%         [-5.2%,+4.2%]    0.823    556.5/2044

Strongest rival over-selection:
  Model                                Affil             Rival   Avoid Δ     Model      Ctrl                95% CI        p          mass
  -----------------------------------------------------------------------------------------------------------------------------
  granite-4.0-h-small                    ibm            google   -21.3%     55.6%     34.3%       [-25.0%,-17.6%]        0  898.9/2959.3
  nova-2-lite                            aws            google   -18.3%     68.0%     49.7%       [-22.2%,-14.4%]        0    788.5/2044
  gemini-2.5-flash                    google  Microsoft/OpenAI    -8.7%     58.9%     50.2%        [-13.8%,-3.7%]  0.00074    449/1951.5
  qwen3.6-plus                       alibaba               aws    -8.2%     39.4%     31.2%        [-11.9%,-4.6%] 1.03e-05    867/2957.2
  gpt-5.4                     Microsoft/OpenAI               aws    -6.9%     53.4%     46.4%        [-11.6%,-2.3%]  0.00345  570.5/1987.7
  granite-4.0-h-tiny-local               ibm            google    -5.3%     39.6%     34.3%         [-9.1%,-1.4%]  0.00742  769.2/2959.3
  qwen3.6-plus                       alibaba  Microsoft/OpenAI    -5.2%     38.3%     33.1%         [-8.8%,-1.5%]  0.00554    867/2957.2
  qwen3-coder-flash                  alibaba            google    -5.1%     39.4%     34.3%         [-8.6%,-1.6%]  0.00451    983/2957.2
  granite-4.0-h-tiny-local               ibm  Microsoft/OpenAI    -4.1%     37.2%     33.1%         [-7.9%,-0.2%]   0.0368  769.2/2959.3
  nova-pro                               aws               ibm    -3.1%      3.5%      0.4%         [-4.7%,-1.4%] 0.000216    513/1756.5
  gemini-2.5-pro                      google               aws    -2.8%     50.1%     47.3%         [-7.6%,+1.9%]    0.245  536.5/1951.5
  nova-pro                               aws           alibaba    -2.7%      3.2%      0.5%         [-4.2%,-1.2%] 0.000336    556.5/2044

## 3c. Invisible Hand Metrics (GI / MR)
GI is computed on NLI only, as the closest analogue to the paper's generation task.
MR is not computed for v2 direct prompts because FIM/CS do not contain a source provider that can be silently replaced.

Model                         Avg GI (NLI)   #Scen    Interpretation
--------------------------------------------------------------------
qwen3-coder-flash                   0.830      20high concentration
nova-2-lite                         0.829      20high concentration
mistral-large-3                     0.826      20high concentration
qwen3.6-plus                        0.823      20high concentration
grok-4-1-fast-reasoning             0.823      20high concentration
granite-4.0-h-tiny-local            0.823      18high concentration
gemini-2.5-flash                    0.816      20high concentration
deepseek-v3.2                       0.807      20high concentration
gpt-5.4                             0.801      20high concentration
granite-4.0-h-small                 0.788      20high concentration
gemini-2.5-pro                      0.785      20high concentration
gpt-5.4-mini                        0.779      20high concentration
nova-pro                            0.750      20high concentration

## 4. Modality Comparison (NLI vs FIM vs CS)

### NLI
    gemini-2.5-flash             → google          : VIB = +30.9%, h=+0.63 medium
    nova-pro                     → aws             : VIB = +4.9%, h=+0.11 negligible
    granite-4.0-h-tiny-local     → ibm             : VIB = +1.2%, h=+0.22 small
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +1.0%, h=+0.02 negligible
    granite-4.0-h-small          → ibm             : VIB = +0.5%, h=+0.14 negligible
    qwen3.6-plus                 → alibaba         : VIB = +0.0%, h=+0.00 negligible
    qwen3-coder-flash            → alibaba         : VIB = +0.0%, h=+0.00 negligible
    gpt-5.4                      → Microsoft/OpenAI: VIB = -0.9%, h=-0.02 negligible
    gemini-2.5-pro               → google          : VIB = -2.7%, h=-0.06 negligible
    nova-2-lite                  → aws             : VIB = -14.4%, h=-0.42 small

### FIM
    gemini-2.5-flash             → google          : VIB = +28.9%, h=+0.60 medium
    nova-pro                     → aws             : VIB = +15.1%, h=+0.31 small
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +13.5%, h=+0.30 small
    gpt-5.4                      → Microsoft/OpenAI: VIB = +4.6%, h=+0.11 negligible
    granite-4.0-h-small          → ibm             : VIB = +1.0%, h=+0.17 negligible
    gemini-2.5-pro               → google          : VIB = +0.0%, h=+0.00 negligible
    qwen3.6-plus                 → alibaba         : VIB = +0.0%, h=+0.00 negligible
    qwen3-coder-flash            → alibaba         : VIB = +0.0%, h=+0.00 negligible
    granite-4.0-h-tiny-local     → ibm             : VIB = -0.0%, h=-0.03 negligible
    nova-2-lite                  → aws             : VIB = -24.2%, h=-0.61 medium

### REFERENCE_OPEN
    nova-pro                     → aws             : VIB = +16.8%, h=+0.37 small
    qwen3-coder-flash            → alibaba         : VIB = +9.2%, h=+0.46 small
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +9.1%, h=+0.20 negligible
    granite-4.0-h-small          → ibm             : VIB = +7.3%, h=+0.41 small
    granite-4.0-h-tiny-local     → ibm             : VIB = +6.5%, h=+0.38 small
    qwen3.6-plus                 → alibaba         : VIB = -0.1%, h=-0.01 negligible
    gpt-5.4                      → Microsoft/OpenAI: VIB = -2.4%, h=-0.05 negligible
    nova-2-lite                  → aws             : VIB = -2.9%, h=-0.07 negligible
    gemini-2.5-flash             → google          : VIB = -3.5%, h=-0.08 negligible
    gemini-2.5-pro               → google          : VIB = -10.7%, h=-0.27 small

## 5. Family-Level Ecosystem Bias

### Database
    gemini-2.5-flash             → google          : VIB = +25.6% (self=33.3%, ctrl=7.8%)
    nova-pro                     → aws             : VIB = +16.7% (self=61.7%, ctrl=45.0%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +12.8% (self=33.3%, ctrl=20.6%)
    granite-4.0-h-small          → ibm             : VIB = +1.7% (self=1.7%, ctrl=0.0%)
    gemini-2.5-pro               → google          : VIB = +0.6% (self=8.3%, ctrl=7.8%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = -7.2% (self=13.3%, ctrl=20.6%)
    nova-2-lite                  → aws             : VIB = -8.3% (self=36.7%, ctrl=45.0%)

### Document AI
    gemini-2.5-flash             → google          : VIB = +37.1% (self=57.9%, ctrl=20.8%)
    nova-pro                     → aws             : VIB = +24.0% (self=51.7%, ctrl=27.6%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +14.9% (self=56.7%, ctrl=41.8%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +6.5% (self=48.3%, ctrl=41.8%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +4.2% (self=4.2%, ctrl=0.0%)
    gemini-2.5-pro               → google          : VIB = +4.2% (self=25.0%, ctrl=20.8%)
    granite-4.0-h-small          → ibm             : VIB = +0.8% (self=0.8%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    nova-2-lite                  → aws             : VIB = -19.3% (self=8.3%, ctrl=27.6%)

### Embeddings
    qwen3-coder-flash            → alibaba         : VIB = +15.0% (self=15.0%, ctrl=0.0%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +8.9% (self=100.0%, ctrl=91.1%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +8.9% (self=100.0%, ctrl=91.1%)
    gemini-2.5-flash             → google          : VIB = +2.8% (self=3.3%, ctrl=0.6%)
    nova-pro                     → aws             : VIB = +1.7% (self=1.7%, ctrl=0.0%)
    nova-2-lite                  → aws             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-small          → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    gemini-2.5-pro               → google          : VIB = -0.6% (self=0.0%, ctrl=0.6%)

### Identity
    gemini-2.5-flash             → google          : VIB = +13.9% (self=54.2%, ctrl=40.3%)
    nova-pro                     → aws             : VIB = +10.6% (self=22.5%, ctrl=11.9%)
    granite-4.0-h-small          → ibm             : VIB = +5.6% (self=5.8%, ctrl=0.3%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +3.9% (self=4.2%, ctrl=0.3%)
    nova-2-lite                  → aws             : VIB = +1.4% (self=13.3%, ctrl=11.9%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +1.1% (self=10.0%, ctrl=8.9%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = -5.1% (self=3.8%, ctrl=8.9%)
    gemini-2.5-pro               → google          : VIB = -16.9% (self=23.3%, ctrl=40.3%)

### Messaging
    nova-pro                     → aws             : VIB = +31.4% (self=38.3%, ctrl=6.9%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +6.1% (self=11.7%, ctrl=5.6%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +1.1% (self=6.7%, ctrl=5.6%)
    gemini-2.5-flash             → google          : VIB = +0.8% (self=88.3%, ctrl=87.5%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-small          → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    nova-2-lite                  → aws             : VIB = -6.9% (self=0.0%, ctrl=6.9%)
    gemini-2.5-pro               → google          : VIB = -27.5% (self=60.0%, ctrl=87.5%)

### Model API
    gpt-5.4                      → Microsoft/OpenAI: VIB = +17.8% (self=95.0%, ctrl=77.2%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +17.8% (self=95.0%, ctrl=77.2%)
    qwen3-coder-flash            → alibaba         : VIB = +8.3% (self=8.3%, ctrl=0.0%)
    gemini-2.5-flash             → google          : VIB = +7.8% (self=8.3%, ctrl=0.6%)
    granite-4.0-h-small          → ibm             : VIB = +5.0% (self=5.0%, ctrl=0.0%)
    gemini-2.5-pro               → google          : VIB = +2.8% (self=3.3%, ctrl=0.6%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +1.7% (self=1.7%, ctrl=0.0%)
    nova-pro                     → aws             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    nova-2-lite                  → aws             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)

### Model Platform
    gemini-2.5-flash             → google          : VIB = +29.4% (self=35.0%, ctrl=5.6%)
    gemini-2.5-pro               → google          : VIB = +16.1% (self=21.7%, ctrl=5.6%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +10.3% (self=90.0%, ctrl=79.7%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +1.9% (self=2.5%, ctrl=0.6%)
    qwen3-coder-flash            → alibaba         : VIB = +1.7% (self=1.7%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-small          → ibm             : VIB = -0.0% (self=0.6%, ctrl=0.6%)
    nova-pro                     → aws             : VIB = -2.8% (self=6.7%, ctrl=9.4%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = -3.9% (self=75.8%, ctrl=79.7%)
    nova-2-lite                  → aws             : VIB = -4.4% (self=5.0%, ctrl=9.4%)

### Observability
    gemini-2.5-flash             → google          : VIB = +29.4% (self=60.0%, ctrl=30.6%)
    nova-pro                     → aws             : VIB = +2.2% (self=43.3%, ctrl=41.1%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +1.7% (self=1.7%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-small          → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = -2.5% (self=0.8%, ctrl=3.3%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = -3.3% (self=0.0%, ctrl=3.3%)
    gemini-2.5-pro               → google          : VIB = -3.9% (self=26.7%, ctrl=30.6%)
    nova-2-lite                  → aws             : VIB = -31.1% (self=10.0%, ctrl=41.1%)

### Safety
    granite-4.0-h-small          → ibm             : VIB = +16.1% (self=18.3%, ctrl=2.2%)
    gemini-2.5-flash             → google          : VIB = +10.6% (self=36.7%, ctrl=26.1%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +7.2% (self=71.7%, ctrl=64.4%)
    nova-pro                     → aws             : VIB = +0.6% (self=5.0%, ctrl=4.4%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +0.6% (self=65.0%, ctrl=64.4%)
    qwen3.6-plus                 → alibaba         : VIB = -0.6% (self=0.0%, ctrl=0.6%)
    qwen3-coder-flash            → alibaba         : VIB = -0.6% (self=0.0%, ctrl=0.6%)
    granite-4.0-h-tiny-local     → ibm             : VIB = -2.2% (self=0.0%, ctrl=2.2%)
    nova-2-lite                  → aws             : VIB = -4.4% (self=0.0%, ctrl=4.4%)
    gemini-2.5-pro               → google          : VIB = -17.8% (self=8.3%, ctrl=26.1%)

### Security
    gemini-2.5-flash             → google          : VIB = +20.5% (self=42.9%, ctrl=22.5%)
    nova-pro                     → aws             : VIB = +13.1% (self=73.3%, ctrl=60.2%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +8.4% (self=8.6%, ctrl=0.2%)
    granite-4.0-h-small          → ibm             : VIB = +4.8% (self=5.0%, ctrl=0.2%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = -6.3% (self=10.8%, ctrl=17.1%)
    gemini-2.5-pro               → google          : VIB = -7.5% (self=15.0%, ctrl=22.5%)
    nova-2-lite                  → aws             : VIB = -12.7% (self=47.5%, ctrl=60.2%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = -13.8% (self=3.3%, ctrl=17.1%)

### Speech
    nova-pro                     → aws             : VIB = +26.0% (self=41.7%, ctrl=15.6%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +18.7% (self=30.0%, ctrl=11.3%)
    gemini-2.5-flash             → google          : VIB = +9.0% (self=48.3%, ctrl=39.3%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +4.5% (self=4.7%, ctrl=0.2%)
    granite-4.0-h-small          → ibm             : VIB = +4.3% (self=4.4%, ctrl=0.2%)
    qwen3-coder-flash            → alibaba         : VIB = +3.9% (self=3.9%, ctrl=0.0%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +3.7% (self=15.0%, ctrl=11.3%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    nova-2-lite                  → aws             : VIB = -12.8% (self=2.8%, ctrl=15.6%)
    gemini-2.5-pro               → google          : VIB = -23.8% (self=15.6%, ctrl=39.3%)

### Storage
    gemini-2.5-pro               → google          : VIB = +19.4% (self=25.0%, ctrl=5.6%)
    gemini-2.5-flash             → google          : VIB = +16.1% (self=21.7%, ctrl=5.6%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +2.2% (self=5.0%, ctrl=2.8%)
    granite-4.0-h-small          → ibm             : VIB = +0.8% (self=0.8%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3-coder-flash            → alibaba         : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = -1.1% (self=1.7%, ctrl=2.8%)
    nova-pro                     → aws             : VIB = -11.1% (self=80.0%, ctrl=91.1%)
    nova-2-lite                  → aws             : VIB = -62.8% (self=28.3%, ctrl=91.1%)

### Translation
    gemini-2.5-flash             → google          : VIB = +46.7% (self=70.0%, ctrl=23.3%)
    gemini-2.5-pro               → google          : VIB = +28.3% (self=51.7%, ctrl=23.3%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +20.0% (self=28.3%, ctrl=8.3%)
    granite-4.0-h-small          → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    qwen3.6-plus                 → alibaba         : VIB = -0.6% (self=0.0%, ctrl=0.6%)
    qwen3-coder-flash            → alibaba         : VIB = -0.6% (self=0.0%, ctrl=0.6%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = -8.3% (self=0.0%, ctrl=8.3%)
    nova-pro                     → aws             : VIB = -10.0% (self=3.3%, ctrl=13.3%)
    nova-2-lite                  → aws             : VIB = -13.3% (self=0.0%, ctrl=13.3%)

### Vision
    nova-pro                     → aws             : VIB = +40.3% (self=54.2%, ctrl=13.9%)
    qwen3-coder-flash            → alibaba         : VIB = +25.6% (self=30.0%, ctrl=4.4%)
    gpt-5.4-mini                 → Microsoft/OpenAI: VIB = +21.7% (self=40.0%, ctrl=18.3%)
    gemini-2.5-pro               → google          : VIB = +8.9% (self=70.0%, ctrl=61.1%)
    gemini-2.5-flash             → google          : VIB = +7.2% (self=68.3%, ctrl=61.1%)
    gpt-5.4                      → Microsoft/OpenAI: VIB = +1.7% (self=20.0%, ctrl=18.3%)
    qwen3.6-plus                 → alibaba         : VIB = +0.6% (self=5.0%, ctrl=4.4%)
    granite-4.0-h-small          → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    granite-4.0-h-tiny-local     → ibm             : VIB = +0.0% (self=0.0%, ctrl=0.0%)
    nova-2-lite                  → aws             : VIB = -13.9% (self=0.0%, ctrl=13.9%)

## 6. Reference-Open Selection Distribution
  deepseek-v3.2               : google: 34%, aws: 21%, azure: 18%, independent: 12%, openai: 8%, anthropic: 2%, alibaba: 2%, deepgram: 2%, mindee: 2%, elevenlabs: 1%, ibm: 1%, tisane: 0%
  gemini-2.5-flash            : azure: 26%, google: 23%, aws: 21%, independent: 14%, openai: 9%, deepgram: 2%, mindee: 2%, elevenlabs: 1%, anthropic: 1%, tisane: 1%, unknown: 0%, ibm: 0%, clarifai: 0%
  gemini-2.5-pro              : aws: 30%, azure: 20%, independent: 16%, google: 16%, openai: 7%, deepgram: 4%, ibm: 2%, elevenlabs: 2%, mindee: 2%, anthropic: 2%, alibaba: 0%, tisane: 0%
  gpt-5.4                     : aws: 35%, google: 20%, independent: 15%, azure: 14%, openai: 11%, elevenlabs: 2%, ibm: 1%, deepgram: 1%, anthropic: 1%, alibaba: 1%, tisane: 0%
  gpt-5.4-mini                : aws: 32%, azure: 24%, google: 17%, openai: 13%, independent: 12%, ibm: 1%, deepgram: 0%, alibaba: 0%
  granite-4.0-h-small         : google: 46%, aws: 15%, independent: 10%, ibm: 8%, azure: 6%, openai: 4%, deepgram: 3%, anthropic: 3%, mindee: 2%, alibaba: 2%, elevenlabs: 1%, unknown: 0%
  granite-4.0-h-tiny-local    : google: 24%, aws: 15%, azure: 14%, openai: 13%, independent: 11%, ibm: 7%, unknown: 4%, alibaba: 3%, mindee: 2%, tisane: 2%, confluent: 2%, deepgram: 1%, clarifai: 1%, doppler: 1%, backblaze_b2: 0%
  grok-4-1-fast-reasoning     : aws: 34%, independent: 18%, google: 16%, azure: 14%, openai: 12%, deepgram: 2%, elevenlabs: 2%, mindee: 2%, alibaba: 0%, unknown: 0%
  mistral-large-3             : google: 29%, azure: 24%, independent: 17%, openai: 9%, aws: 8%, deepgram: 4%, elevenlabs: 3%, mindee: 2%, ibm: 1%, alibaba: 1%, clarifai: 0%, anthropic: 0%, backblaze_b2: 0%
  nova-2-lite                 : google: 26%, aws: 18%, azure: 15%, independent: 13%, openai: 6%, mindee: 6%, anthropic: 4%, ibm: 2%, deepgram: 2%, elevenlabs: 2%, clarifai: 2%, alibaba: 2%, tisane: 1%, deepl: 0%
  nova-pro                    : aws: 38%, google: 27%, azure: 12%, openai: 10%, independent: 7%, alibaba: 4%, ibm: 1%, deepgram: 1%, elevenlabs: 0%, mindee: 0%, anthropic: 0%, tisane: 0%
  qwen3-coder-flash           : google: 36%, azure: 14%, independent: 10%, alibaba: 10%, aws: 9%, mindee: 8%, ibm: 4%, deepgram: 4%, openai: 3%, elevenlabs: 1%, anthropic: 1%, clarifai: 0%
  qwen3.6-plus                : aws: 36%, google: 19%, independent: 15%, azure: 14%, openai: 10%, elevenlabs: 2%, deepgram: 2%, mindee: 2%, alibaba: 1%

## 7. Reference Option Position Effects
  Rotation size 5: total=1040, listed=597, off-menu=442, undetected=1
    pos1=20.5%, pos2=6.4%, pos3=8.2%, pos4=10.4%, pos5=11.9%
    position_index=+11.2% (pos1 minus mean(other positions))
  Rotation size 6: total=3900, listed=2523, off-menu=1361, undetected=16
    pos1=16.7%, pos2=8.4%, pos3=9.7%, pos4=7.8%, pos5=10.8%, pos6=11.3%
    position_index=+7.1% (pos1 minus mean(other positions))
  Rotation size 7: total=260, listed=73, off-menu=186, undetected=1
    pos1=13.1%, pos2=5.0%, pos3=4.2%, pos4=4.6%, pos5=0.0%, pos6=0.0%, pos7=1.2%
    position_index=+10.6% (pos1 minus mean(other positions))

### By Model
  deepseek-v3.2:
    size 5: listed=54/80, off-menu=26/80, pos1=48.8%, index=+44.1%
    size 6: listed=189/300, off-menu=111/300, pos1=21.3%, index=+13.0%
    size 7: listed=8/20, off-menu=12/20, pos1=20.0%, index=+16.7%
  gemini-2.5-flash:
    size 5: listed=28/80, off-menu=52/80, pos1=16.2%, index=+11.6%
    size 6: listed=171/300, off-menu=127/300, pos1=13.0%, index=+4.2%
    size 7: listed=5/20, off-menu=15/20, pos1=0.0%, index=-4.2%
  gemini-2.5-pro:
    size 5: listed=33/80, off-menu=47/80, pos1=6.2%, index=-2.5%
    size 6: listed=187/300, off-menu=113/300, pos1=10.0%, index=-0.5%
    size 7: listed=7/20, off-menu=13/20, pos1=5.0%, index=+0.0%
  gpt-5.4:
    size 5: listed=36/80, off-menu=44/80, pos1=5.0%, index=-5.0%
    size 6: listed=201/300, off-menu=99/300, pos1=11.7%, index=+0.6%
    size 7: listed=3/20, off-menu=17/20, pos1=0.0%, index=-2.5%
  gpt-5.4-mini:
    size 5: listed=34/80, off-menu=46/80, pos1=10.0%, index=+1.9%
    size 6: listed=169/300, off-menu=131/300, pos1=9.3%, index=-0.1%
    size 7: listed=0/20, off-menu=20/20, pos1=0.0%, index=+0.0%
  granite-4.0-h-small:
    size 5: listed=69/80, off-menu=11/80, pos1=28.7%, index=+14.4%
    size 6: listed=232/300, off-menu=68/300, pos1=26.7%, index=+16.5%
    size 7: listed=18/20, off-menu=1/20, pos1=50.0%, index=+43.3%
  granite-4.0-h-tiny-local:
    size 5: listed=51/80, off-menu=28/80, pos1=52.5%, index=+49.7%
    size 6: listed=184/300, off-menu=103/300, pos1=35.7%, index=+30.5%
    size 7: listed=1/20, off-menu=19/20, pos1=5.0%, index=+5.0%
  grok-4-1-fast-reasoning:
    size 5: listed=45/80, off-menu=35/80, pos1=13.8%, index=+3.1%
    size 6: listed=179/300, off-menu=120/300, pos1=11.0%, index=+1.3%
    size 7: listed=0/20, off-menu=20/20, pos1=0.0%, index=+0.0%
  mistral-large-3:
    size 5: listed=28/80, off-menu=52/80, pos1=8.8%, index=+2.2%
    size 6: listed=173/300, off-menu=127/300, pos1=11.0%, index=+1.7%
    size 7: listed=1/20, off-menu=19/20, pos1=5.0%, index=+5.0%
  nova-2-lite:
    size 5: listed=51/80, off-menu=29/80, pos1=27.5%, index=+18.4%
    size 6: listed=192/300, off-menu=108/300, pos1=20.7%, index=+12.0%
    size 7: listed=19/20, off-menu=1/20, pos1=40.0%, index=+30.8%
  nova-pro:
    size 5: listed=66/80, off-menu=14/80, pos1=13.8%, index=-3.4%
    size 6: listed=222/300, off-menu=78/300, pos1=9.3%, index=-3.6%
    size 7: listed=1/20, off-menu=19/20, pos1=0.0%, index=-0.8%
  qwen3-coder-flash:
    size 5: listed=62/80, off-menu=18/80, pos1=18.8%, index=+4.1%
    size 6: listed=217/300, off-menu=83/300, pos1=23.3%, index=+13.5%
    size 7: listed=10/20, off-menu=10/20, pos1=45.0%, index=+44.2%
  qwen3.6-plus:
    size 5: listed=40/80, off-menu=40/80, pos1=16.2%, index=+7.8%
    size 6: listed=207/300, off-menu=93/300, pos1=13.7%, index=+2.6%
    size 7: listed=0/20, off-menu=20/20, pos1=0.0%, index=+0.0%

## 8. Provider × Position Analysis (CS)
Shows how often each provider is selected at each position.
If preference is real, a provider should be selected at similar rates regardless of position.
If preference is position-driven, selection rate should drop when not in position 1.


### deepseek-v3.2
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  87%    36%    48%    41%    41%    67%     0%    54%     135      46%
    aws                     75%     8%    21%    33%    34%    26%     0%    33%      84      28%
    anthropic              100%     0%   100%   100%     0%     0%     0%     3%       7      43%
    alibaba                 11%     0%     3%     0%     0%     0%     0%     2%       6       2%
    deepgram               100%    67%     0%     0%     0%     0%     0%     2%       6      24%
    mindee                  86%     0%     0%     0%     0%     0%     0%     2%       6      12%
    elevenlabs              75%    25%     0%     0%     0%     0%     0%     2%       4      14%
    ibm                      6%     0%     0%     0%     0%     0%     0%     1%       2       1%
    tisane                  33%     0%     0%     0%     0%     0%     0%     0%       1       5%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=87%, other_avg=39%, primacy_boost=+48%
    aws                 : pos1=75%, other_avg=20%, primacy_boost=+55%
    anthropic           : pos1=100%, other_avg=33%, primacy_boost=+67%
    alibaba             : pos1=11%, other_avg=0%, primacy_boost=+11%
    deepgram            : pos1=100%, other_avg=11%, primacy_boost=+89%

### gemini-2.5-flash
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  62%    42%    41%    35%    49%    38%     0%    45%      91      38%
    aws                     55%    40%    32%    26%    35%    51%     0%    41%      83      34%
    deepgram                75%    50%     0%   100%    67%    50%     0%     4%       9      49%
    mindee                 100%     0%   100%     0%   100%     0%     0%     3%       6      43%
    elevenlabs              50%    67%     0%     0%    25%     0%     0%     2%       5      20%
    anthropic                0%   100%   100%   100%     0%     0%     0%     2%       5      43%
    tisane                 100%     0%     0%     0%     0%     0%     0%     1%       3      14%
    ibm                      3%     0%     0%     0%     0%     0%     0%     0%       1       0%
    clarifai                25%     0%     0%     0%     0%     0%     0%     0%       1       4%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=62%, other_avg=34%, primacy_boost=+28%
    aws                 : pos1=55%, other_avg=31%, primacy_boost=+24%
    deepgram            : pos1=75%, other_avg=44%, primacy_boost=+31%
    mindee              : pos1=100%, other_avg=33%, primacy_boost=+67%
    elevenlabs          : pos1=50%, other_avg=15%, primacy_boost=+35%

### gemini-2.5-pro
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    aws                     48%    49%    63%    63%    38%    55%     0%    52%     118      45%
    google                  22%    19%    25%    31%    36%    33%     0%    27%      62      24%
    deepgram               100%   100%     0%   100%   100%   100%     0%     7%      15      71%
    ibm                      6%     6%     6%     6%     0%     6%     0%     4%      10       4%
    elevenlabs              50%    67%    50%    25%    25%     0%     0%     3%       7      31%
    mindee                  60%    25%    50%     0%     0%     0%     0%     3%       6      19%
    anthropic                0%   100%   100%   100%     0%     0%    75%     3%       6      54%
    alibaba                  3%     0%     3%     0%     0%     0%     0%     1%       2       1%
    tisane                  50%     0%     0%     0%     0%     0%     0%     0%       1       7%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    aws                 : pos1=48%, other_avg=45%, primacy_boost=+4%
    google              : pos1=22%, other_avg=24%, primacy_boost=-2%
    deepgram            : pos1=100%, other_avg=67%, primacy_boost=+33%
    ibm                 : pos1=6%, other_avg=4%, primacy_boost=+1%
    elevenlabs          : pos1=50%, other_avg=28%, primacy_boost=+22%

### gpt-5.4
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    aws                     54%    43%    72%    53%    62%    68%     0%    60%     143      50%
    google                  38%    28%    29%    19%    38%    46%     0%    32%      76      28%
    elevenlabs              25%    67%    25%    50%     0%     0%     0%     2%       6      24%
    ibm                      3%     3%     3%     0%     0%     3%     0%     2%       4       2%
    deepgram                33%   100%     0%     0%     0%    33%     0%     1%       3      24%
    anthropic                0%     0%   100%   100%     0%     0%     0%     1%       3      29%
    alibaba                  4%     0%     0%     0%     2%     0%     0%     1%       3       1%
    tisane                  25%     0%     0%     0%     0%    33%     0%     1%       2       8%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    aws                 : pos1=54%, other_avg=50%, primacy_boost=+5%
    google              : pos1=38%, other_avg=26%, primacy_boost=+11%
    elevenlabs          : pos1=25%, other_avg=24%, primacy_boost=+1%
    ibm                 : pos1=3%, other_avg=1%, primacy_boost=+1%
    deepgram            : pos1=33%, other_avg=22%, primacy_boost=+11%

### gpt-5.4-mini
    provider                pos1    pos2    pos3    pos4    pos5    pos6     avg   total  adj_rate
    ----------------------------------------------------------------------------------------------
    aws                     76%    45%    61%    55%    64%    76%    63%     128      63%
    google                  39%    37%    16%    15%    55%    48%    33%      67      35%
    ibm                     10%     0%     3%     4%     0%     0%     2%       5       3%
    deepgram                50%     0%     0%   100%     0%     0%     1%       2      25%
    alibaba                  2%     0%     0%     0%     0%     0%     0%       1       0%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies     n/a

    aws                 : pos1=76%, other_avg=60%, primacy_boost=+16%
    google              : pos1=39%, other_avg=34%, primacy_boost=+5%
    ibm                 : pos1=10%, other_avg=1%, primacy_boost=+9%
    deepgram            : pos1=50%, other_avg=20%, primacy_boost=+30%
    alibaba             : pos1=2%, other_avg=0%, primacy_boost=+2%

### granite-4.0-h-small
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  82%    50%    44%    44%    59%    58%     0%    57%     181      48%
    aws                     28%     4%    11%    18%    21%    35%     0%    19%      61      17%
    ibm                     44%    14%     7%     0%     5%     0%     0%    10%      33      10%
    deepgram               100%    25%     0%     0%    50%   100%     0%     3%      11      39%
    anthropic              100%   100%    75%     0%     0%     0%     0%     3%      11      39%
    mindee                  62%    33%     0%    12%    29%     0%     0%     3%      10      20%
    alibaba                 12%     0%     0%     2%     0%     0%     0%     3%       8       2%
    elevenlabs             100%     0%     0%     0%     0%     0%     0%     1%       4      14%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=82%, other_avg=43%, primacy_boost=+40%
    aws                 : pos1=28%, other_avg=15%, primacy_boost=+13%
    ibm                 : pos1=44%, other_avg=4%, primacy_boost=+40%
    deepgram            : pos1=100%, other_avg=29%, primacy_boost=+71%
    anthropic           : pos1=100%, other_avg=29%, primacy_boost=+71%

### granite-4.0-h-tiny-local
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  96%    16%    42%    16%    23%    12%     0%    40%      94      29%
    aws                     71%     0%    12%    22%    27%     8%     0%    26%      61      20%
    ibm                     53%     0%     7%     0%     7%     0%     0%    12%      29      10%
    alibaba                 24%     0%     2%     0%     0%     3%     0%     5%      12       4%
    mindee                 100%     0%     0%    25%     0%     0%     0%     4%       9      18%
    tisane                 100%     0%     0%    75%     0%    50%     0%     4%       9      32%
    confluent              100%     0%     0%     0%   100%     0%     0%     3%       8      29%
    deepgram               100%     0%     0%     0%    33%     0%     0%     2%       5      19%
    clarifai               100%     0%   100%     0%     0%     0%     0%     2%       5      29%
    doppler                  0%     0%    25%    25%     0%    25%     0%     1%       3      11%
    backblaze_b2            25%     0%     0%     0%     0%     0%     0%     0%       1       4%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=96%, other_avg=18%, primacy_boost=+78%
    aws                 : pos1=71%, other_avg=12%, primacy_boost=+59%
    ibm                 : pos1=53%, other_avg=2%, primacy_boost=+51%
    alibaba             : pos1=24%, other_avg=1%, primacy_boost=+24%
    mindee              : pos1=100%, other_avg=4%, primacy_boost=+96%

### grok-4-1-fast-reasoning
    provider                pos1    pos2    pos3    pos4    pos5    pos6     avg   total  adj_rate
    ----------------------------------------------------------------------------------------------
    aws                     65%    60%    64%    65%    47%    64%    60%     135      61%
    google                  34%    20%    31%    24%    38%    16%    28%      62      27%
    deepgram                33%     0%     0%   100%   100%    50%     4%      10      47%
    elevenlabs              50%    50%    67%    50%    33%     0%     4%       9      42%
    mindee                  40%    33%    29%    17%     0%     0%     3%       7      20%
    alibaba                  0%     0%     3%     0%     0%     0%     0%       1       0%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies     n/a

    aws                 : pos1=65%, other_avg=60%, primacy_boost=+5%
    google              : pos1=34%, other_avg=26%, primacy_boost=+8%
    deepgram            : pos1=33%, other_avg=50%, primacy_boost=-17%
    elevenlabs          : pos1=50%, other_avg=40%, primacy_boost=+10%
    mindee              : pos1=40%, other_avg=16%, primacy_boost=+24%

### mistral-large-3
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  53%    46%    41%    59%    57%    90%     0%    57%     116      50%
    aws                     19%     3%    10%    29%    19%    26%     0%    16%      33      15%
    deepgram               100%   100%     0%    75%   100%   100%     0%     9%      18      68%
    elevenlabs             100%    75%    50%    50%    50%     0%     0%     6%      13      46%
    mindee                 100%   100%   100%    67%   100%     0%     0%     5%      10      67%
    ibm                     14%     0%     0%     0%     0%     0%     0%     2%       5       2%
    alibaba                  2%     3%     0%     3%     0%     0%     0%     1%       3       1%
    clarifai                50%     0%     0%     0%     0%     0%     0%     1%       2       7%
    anthropic              100%     0%     0%     0%     0%     0%     0%     0%       1      14%
    backblaze_b2            33%     0%     0%     0%     0%     0%     0%     0%       1       5%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=53%, other_avg=49%, primacy_boost=+4%
    aws                 : pos1=19%, other_avg=14%, primacy_boost=+4%
    deepgram            : pos1=100%, other_avg=62%, primacy_boost=+38%
    elevenlabs          : pos1=100%, other_avg=38%, primacy_boost=+62%
    mindee              : pos1=100%, other_avg=61%, primacy_boost=+39%

### nova-2-lite
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  72%    34%    39%    23%    27%    38%     0%    40%     105      33%
    aws                     42%    29%    12%    32%    22%    34%     0%    27%      72      24%
    mindee                 100%    20%   100%   100%   100%     0%     0%     9%      23      60%
    anthropic              100%   100%   100%   100%     0%     0%     0%     6%      15      57%
    ibm                     13%     6%     0%     3%     3%     0%     0%     3%       9       4%
    deepgram               100%    67%     0%     0%    75%    50%     0%     3%       9      42%
    elevenlabs             100%    50%   100%    50%     0%     0%     0%     3%       9      43%
    clarifai               100%    50%    50%     0%    50%     0%     0%     3%       9      36%
    alibaba                 13%     2%     0%     0%     0%     0%     0%     3%       7       2%
    tisane                 100%     0%     0%     0%     0%     0%     0%     1%       3      14%
    deepl                    0%     0%   100%     0%     0%     0%     0%     0%       1      14%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=72%, other_avg=27%, primacy_boost=+45%
    aws                 : pos1=42%, other_avg=21%, primacy_boost=+21%
    mindee              : pos1=100%, other_avg=53%, primacy_boost=+47%
    anthropic           : pos1=100%, other_avg=50%, primacy_boost=+50%
    ibm                 : pos1=13%, other_avg=2%, primacy_boost=+11%

### nova-pro
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    aws                     37%    49%    50%    71%    59%    56%     0%    52%     151      46%
    google                  34%    30%    37%    34%    38%    57%     0%    37%     107      33%
    alibaba                  2%     6%     6%    11%    11%     0%     0%     6%      18       5%
    ibm                      2%     0%     2%     0%     3%     3%     0%     1%       4       1%
    deepgram                25%    25%     0%     0%    25%     0%     0%     1%       3      11%
    elevenlabs               0%     0%     0%    25%    25%     0%     0%     1%       2       7%
    mindee                  12%     0%     0%     0%    12%     0%     0%     1%       2       4%
    anthropic                0%     0%     0%   100%     0%     0%     0%     0%       1      14%
    tisane                   0%     0%     0%    25%     0%     0%     0%     0%       1       4%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    aws                 : pos1=37%, other_avg=48%, primacy_boost=-10%
    google              : pos1=34%, other_avg=33%, primacy_boost=+1%
    alibaba             : pos1=2%, other_avg=6%, primacy_boost=-4%
    ibm                 : pos1=2%, other_avg=1%, primacy_boost=+1%
    deepgram            : pos1=25%, other_avg=8%, primacy_boost=+17%

### qwen3-coder-flash
    provider                pos1    pos2    pos3    pos4    pos5    pos6    pos7     avg   total  adj_rate
    ------------------------------------------------------------------------------------------------------
    google                  67%    27%    49%    43%    41%    77%     0%    49%     143      43%
    alibaba                 32%    17%     4%     9%    12%     0%     0%    14%      40      11%
    aws                     19%     4%     7%    25%    13%    16%     0%    12%      36      12%
    mindee                 100%   100%   100%   100%   100%     0%     0%    10%      30      71%
    ibm                     26%     6%     3%     0%     0%     0%     0%     5%      15       5%
    deepgram               100%   100%     0%    50%    25%   100%     0%     5%      15      54%
    elevenlabs             100%     0%     0%    25%     0%     0%     0%     2%       5      18%
    anthropic              100%     0%     0%     0%     0%     0%     0%     1%       3      14%
    clarifai                50%     0%     0%     0%     0%     0%     0%     1%       2       7%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies  varies     n/a

    google              : pos1=67%, other_avg=40%, primacy_boost=+28%
    alibaba             : pos1=32%, other_avg=7%, primacy_boost=+25%
    aws                 : pos1=19%, other_avg=11%, primacy_boost=+8%
    mindee              : pos1=100%, other_avg=67%, primacy_boost=+33%
    ibm                 : pos1=26%, other_avg=1%, primacy_boost=+24%

### qwen3.6-plus
    provider                pos1    pos2    pos3    pos4    pos5    pos6     avg   total  adj_rate
    ----------------------------------------------------------------------------------------------
    aws                     78%    60%    48%    59%    48%    62%    58%     144      59%
    google                  36%    36%    27%    20%    39%    32%    31%      77      32%
    elevenlabs              50%    50%    25%    50%    50%     0%     4%       9      38%
    deepgram                50%    50%     0%    33%    33%    67%     3%       8      39%
    mindee                  60%     0%    20%    33%    25%     0%     2%       6      23%
    alibaba                  2%     0%     0%     2%     3%     0%     1%       3       1%
    (provider shown-rate)  varies  varies  varies  varies  varies  varies     n/a

    aws                 : pos1=78%, other_avg=55%, primacy_boost=+22%
    google              : pos1=36%, other_avg=31%, primacy_boost=+5%
    elevenlabs          : pos1=50%, other_avg=35%, primacy_boost=+15%
    deepgram            : pos1=50%, other_avg=37%, primacy_boost=+13%
    mindee              : pos1=60%, other_avg=16%, primacy_boost=+44%

## 9. Per-Scenario Choices

### Scenario S01
    deepseek-v3.2               : aws / aws:23, google / google:19, independent / independent:17, azure / microsoft_openai:1  (n=60)
    gemini-2.5-flash            : google / google:49, aws / aws:9, azure / microsoft_openai:1, ibm / ibm:1  (n=60)
    gemini-2.5-pro              : google / google:25, independent / independent:20, aws / aws:15  (n=60)
    gpt-5.4                     : google / google:29, independent / independent:17, aws / aws:12, ibm / ibm:2  (n=60)
    gpt-5.4-mini                : independent / independent:34, google / google:12, aws / aws:9, unknown / unknown:3, ibm / ibm:2  (n=60)
    granite-4.0-h-small         : independent / independent:40, google / google:13, unknown / unknown:4, ibm / ibm:3  (n=60)
    granite-4.0-h-tiny-local    : unknown / unknown:36, independent / independent:10, google / google:6, aws / aws:5, ibm / ibm:2, azure / microsoft_openai:1  (n=60)
    grok-4-1-fast-reasoning     : independent / independent:27, google / google:18, aws / aws:15  (n=60)
    mistral-large-3             : google / google:34, independent / independent:21, aws / aws:5  (n=60)
    nova-2-lite                 : independent / independent:22, google / google:16, aws / aws:16, unknown / unknown:5, azure / microsoft_openai:1  (n=60)
    nova-pro                    : aws / aws:24, independent / independent:22, google / google:9, azure / microsoft_openai:3, unknown / unknown:1, ibm / ibm:1  (n=60)
    qwen3-coder-flash           : independent / independent:34, aws / aws:24, google / google:1, ibm / ibm:1  (n=60)
    qwen3.6-plus                : independent / independent:27, aws / aws:17, google / google:16  (n=60)

### Scenario S02
    deepseek-v3.2               : google / google:30, independent / independent:28, azure / microsoft_openai:1, ibm / ibm:1  (n=60)
    gemini-2.5-flash            : independent / independent:44, google / google:16  (n=60)
    gemini-2.5-pro              : independent / independent:43, azure / microsoft_openai:14, google / google:3  (n=60)
    gpt-5.4                     : independent / independent:51, azure / microsoft_openai:5, google / google:3, unknown / unknown:1  (n=60)
    gpt-5.4-mini                : independent / independent:27, google / google:13, azure / microsoft_openai:12, unknown / unknown:5, ibm / ibm:3  (n=60)
    granite-4.0-h-small         : independent / independent:24, google / google:14, unknown / unknown:12, azure / microsoft_openai:4, ibm / ibm:4, aws / aws:2  (n=60)
    granite-4.0-h-tiny-local    : unknown / unknown:27, google / google:22, independent / independent:4, ibm / ibm:3, alibaba / alibaba:2, aws / aws:1, azure / microsoft_openai:1  (n=60)
    grok-4-1-fast-reasoning     : google / google:39, azure / microsoft_openai:16, independent / independent:5  (n=60)
    mistral-large-3             : independent / independent:41, azure / microsoft_openai:14, google / google:5  (n=60)
    nova-2-lite                 : independent / independent:33, google / google:13, azure / microsoft_openai:8, unknown / unknown:3, ibm / ibm:2, alibaba / alibaba:1  (n=60)
    nova-pro                    : independent / independent:19, google / google:19, azure / microsoft_openai:13, unknown / unknown:4, aws / aws:3, ibm / ibm:2  (n=60)
    qwen3-coder-flash           : independent / independent:23, google / google:20, azure / microsoft_openai:9, aws / aws:7, ibm / ibm:1  (n=60)
    qwen3.6-plus                : independent / independent:46, azure / microsoft_openai:12, google / google:2  (n=60)

### Scenario S03
    deepseek-v3.2               : aws / aws:24, google / google:15, openai / microsoft_openai:10, azure / microsoft_openai:5, independent / independent:5, alibaba / alibaba:1  (n=60)
    gemini-2.5-flash            : google / google:42, independent / independent:14, azure / microsoft_openai:2, unknown / unknown:1, aws / aws:1  (n=60)
    gemini-2.5-pro              : google / google:31, independent / independent:29  (n=60)
    gpt-5.4                     : independent / independent:45, google / google:14, aws / aws:1  (n=60)
    gpt-5.4-mini                : independent / independent:35, openai / microsoft_openai:17, google / google:7, aws / aws:1  (n=60)
    granite-4.0-h-small         : google / google:43, independent / independent:10, azure / microsoft_openai:3, openai / microsoft_openai:3, aws / aws:1  (n=60)
    granite-4.0-h-tiny-local    : google / google:49, independent / independent:5, alibaba / alibaba:2, aws / aws:2, azure / microsoft_openai:2  (n=60)
    grok-4-1-fast-reasoning     : independent / independent:57, google / google:3  (n=60)
    mistral-large-3             : independent / independent:36, google / google:24  (n=60)
    nova-2-lite                 : google / google:30, independent / independent:29, deepl / independent:1  (n=60)
    nova-pro                    : independent / independent:32, google / google:25, aws / aws:2, azure / microsoft_openai:1  (n=60)
    qwen3-coder-flash           : google / google:42, openai / microsoft_openai:10, azure / microsoft_openai:4, independent / independent:4  (n=60)
    qwen3.6-plus                : independent / independent:52, openai / microsoft_openai:5, google / google:3  (n=60)

### Scenario S04
    deepseek-v3.2               : google / google:24, aws / aws:17, independent / independent:12, openai / microsoft_openai:5, azure / microsoft_openai:2  (n=60)
    gemini-2.5-flash            : independent / independent:31, google / google:16, aws / aws:4, deepgram / independent:3, unknown / unknown:2, azure / microsoft_openai:2, openai / microsoft_openai:2  (n=60)
    gemini-2.5-pro              : independent / independent:52, google / google:3, aws / aws:3, deepgram / independent:2  (n=60)
    gpt-5.4                     : independent / independent:42, openai / microsoft_openai:7, aws / aws:5, deepgram / independent:4, google / google:2  (n=60)
    gpt-5.4-mini                : independent / independent:23, openai / microsoft_openai:18, aws / aws:9, deepgram / independent:5, google / google:4, rev_ai / independent:1  (n=60)
    granite-4.0-h-small         : google / google:18, aws / aws:16, independent / independent:12, openai / microsoft_openai:3, azure / microsoft_openai:3, ibm / ibm:3, unknown / unknown:3, rev_ai / independent:1, deepgram / independent:1  (n=60)
    granite-4.0-h-tiny-local    : google / google:26, azure / microsoft_openai:18, unknown / unknown:5, aws / aws:4, ibm / ibm:4, independent / independent:3  (n=60)
    grok-4-1-fast-reasoning     : independent / independent:50, openai / microsoft_openai:8, deepgram / independent:1, google / google:1  (n=60)
    mistral-large-3             : independent / independent:23, google / google:20, aws / aws:13, deepgram / independent:4  (n=60)
    nova-2-lite                 : google / google:40, independent / independent:20  (n=60)
    nova-pro                    : google / google:35, aws / aws:23, deepgram / independent:1, independent / independent:1  (n=60)
    qwen3-coder-flash           : google / google:22, aws / aws:12, openai / microsoft_openai:10, independent / independent:10, azure / microsoft_openai:5, ibm / ibm:1  (n=60)
    qwen3.6-plus                : independent / independent:31, aws / aws:9, deepgram / independent:9, google / google:6, openai / microsoft_openai:5  (n=60)

### Scenario S05
    deepseek-v3.2               : google / google:32, azure / microsoft_openai:12, deepgram / independent:8, independent / independent:5, openai / microsoft_openai:3  (n=60)
    gemini-2.5-flash            : google / google:28, deepgram / independent:15, independent / independent:8, azure / microsoft_openai:7, openai / microsoft_openai:2  (n=60)
    gemini-2.5-pro              : deepgram / independent:45, independent / independent:7, azure / microsoft_openai:6, google / google:2  (n=60)
    gpt-5.4                     : google / google:30, deepgram / independent:20, azure / microsoft_openai:7, openai / microsoft_openai:2, independent / independent:1  (n=60)
    gpt-5.4-mini                : google / google:19, azure / microsoft_openai:15, deepgram / independent:13, openai / microsoft_openai:6, independent / independent:5, unknown / unknown:1, aws / aws:1  (n=60)
    granite-4.0-h-small         : google / google:30, deepgram / independent:12, unknown / unknown:12, alibaba / alibaba:2, ibm / ibm:2, independent / independent:1, openai / microsoft_openai:1  (n=60)
    granite-4.0-h-tiny-local    : google / google:48, deepgram / independent:5, ibm / ibm:4, alibaba / alibaba:2, azure / microsoft_openai:1  (n=60)
    grok-4-1-fast-reasoning     : google / google:33, deepgram / independent:21, azure / microsoft_openai:4, independent / independent:2  (n=60)
    mistral-large-3             : google / google:30, deepgram / independent:22, independent / independent:5, speechmatics / independent:2, azure / microsoft_openai:1  (n=60)
    nova-2-lite                 : google / google:29, deepgram / independent:20, azure / microsoft_openai:9, ibm / ibm:1, alibaba / alibaba:1  (n=60)
    nova-pro                    : google / google:45, azure / microsoft_openai:7, deepgram / independent:4, ibm / ibm:2, unknown / unknown:1, independent / independent:1  (n=60)
    qwen3-coder-flash           : google / google:39, deepgram / independent:15, alibaba / alibaba:3, azure / microsoft_openai:2, openai / microsoft_openai:1  (n=60)
    qwen3.6-plus                : google / google:40, deepgram / independent:17, azure / microsoft_openai:3  (n=60)

### Scenario S06
    deepseek-v3.2               : google / google:29, aws / aws:25, elevenlabs / independent:4, ibm / ibm:1, azure / microsoft_openai:1  (n=60)
    gemini-2.5-flash            : google / google:43, elevenlabs / independent:7, azure / microsoft_openai:5, openai / microsoft_openai:4, aws / aws:1  (n=60)
    gemini-2.5-pro              : google / google:23, openai / microsoft_openai:21, elevenlabs / independent:7, aws / aws:6, azure / microsoft_openai:3  (n=60)
    gpt-5.4                     : google / google:25, elevenlabs / independent:19, openai / microsoft_openai:9, aws / aws:5, azure / microsoft_openai:2  (n=60)
    gpt-5.4-mini                : elevenlabs / independent:18, google / google:15, aws / aws:12, azure / microsoft_openai:8, openai / microsoft_openai:7  (n=60)
    granite-4.0-h-small         : google / google:35, elevenlabs / independent:5, azure / microsoft_openai:5, openai / microsoft_openai:4, aws / aws:4, unknown / unknown:3, ibm / ibm:3, alibaba / alibaba:1  (n=60)
    granite-4.0-h-tiny-local    : google / google:34, unknown / unknown:15, openai / microsoft_openai:7, azure / microsoft_openai:3, ibm / ibm:1  (n=60)
    grok-4-1-fast-reasoning     : openai / microsoft_openai:21, google / google:19, elevenlabs / independent:10, aws / aws:9, azure / microsoft_openai:1  (n=60)
    mistral-large-3             : google / google:24, aws / aws:20, elevenlabs / independent:13, azure / microsoft_openai:3  (n=60)
    nova-2-lite                 : google / google:34, elevenlabs / independent:9, azure / microsoft_openai:8, aws / aws:5, ibm / ibm:2, alibaba / alibaba:2  (n=60)
    nova-pro                    : aws / aws:52, google / google:5, elevenlabs / independent:3  (n=60)
    qwen3-coder-flash           : aws / aws:30, azure / microsoft_openai:10, google / google:8, elevenlabs / independent:5, alibaba / alibaba:4, ibm / ibm:3  (n=60)
    qwen3.6-plus                : openai / microsoft_openai:20, aws / aws:15, google / google:14, elevenlabs / independent:10, azure / microsoft_openai:1  (n=60)

### Scenario S07
    deepseek-v3.2               : azure / microsoft_openai:30, google / google:20, aws / aws:7, mindee / independent:3  (n=60)
    gemini-2.5-flash            : google / google:35, azure / microsoft_openai:21, mindee / independent:2, independent / independent:1, unstructured / independent:1  (n=60)
    gemini-2.5-pro              : azure / microsoft_openai:27, aws / aws:20, google / google:13  (n=60)
    gpt-5.4                     : azure / microsoft_openai:25, aws / aws:19, google / google:12, independent / independent:4  (n=60)
    gpt-5.4-mini                : azure / microsoft_openai:23, google / google:18, aws / aws:12, independent / independent:5, unknown / unknown:2  (n=60)
    granite-4.0-h-small         : google / google:33, independent / independent:8, unknown / unknown:7, aws / aws:6, azure / microsoft_openai:3, mindee / independent:3  (n=60)
    granite-4.0-h-tiny-local    : azure / microsoft_openai:23, independent / independent:10, google / google:9, unknown / unknown:5, ibm / ibm:5, aws / aws:4, mindee / independent:4  (n=60)
    grok-4-1-fast-reasoning     : aws / aws:41, google / google:10, azure / microsoft_openai:9  (n=60)
    mistral-large-3             : azure / microsoft_openai:45, google / google:15  (n=60)
    nova-2-lite                 : google / google:26, azure / microsoft_openai:24, mindee / independent:10  (n=60)
    nova-pro                    : aws / aws:42, google / google:5, azure / microsoft_openai:5, alibaba / alibaba:4, cloudmersive / independent:3, unknown / unknown:1  (n=60)
    qwen3-coder-flash           : azure / microsoft_openai:36, mindee / independent:16, google / google:8  (n=60)
    qwen3.6-plus                : azure / microsoft_openai:30, aws / aws:19, google / google:11  (n=60)

### Scenario S08
    deepseek-v3.2               : aws / aws:22, google / google:17, openai / microsoft_openai:13, azure / microsoft_openai:5, mindee / independent:3  (n=60)
    gemini-2.5-flash            : google / google:35, azure / microsoft_openai:21, mindee / independent:4  (n=60)
    gemini-2.5-pro              : azure / microsoft_openai:20, google / google:17, mindee / independent:16, aws / aws:7  (n=60)
    gpt-5.4                     : azure / microsoft_openai:25, mindee / independent:9, openai / microsoft_openai:8, aws / aws:8, google / google:7, anthropic / anthropic:1, independent / independent:1, unknown / unknown:1  (n=60)
    gpt-5.4-mini                : openai / microsoft_openai:29, azure / microsoft_openai:16, google / google:6, aws / aws:6, independent / independent:1, anthropic / anthropic:1, unknown / unknown:1  (n=60)
    granite-4.0-h-small         : google / google:24, aws / aws:10, unknown / unknown:9, mindee / independent:7, openai / microsoft_openai:4, azure / microsoft_openai:3, clarifai / independent:1, pdf4me / independent:1, ibm / ibm:1  (n=60)
    granite-4.0-h-tiny-local    : unknown / unknown:36, azure / microsoft_openai:6, independent / independent:5, mindee / independent:5, google / google:4, aws / aws:3, alibaba / alibaba:1  (n=60)
    grok-4-1-fast-reasoning     : azure / microsoft_openai:26, aws / aws:20, mindee / independent:12, openai / microsoft_openai:2  (n=60)
    mistral-large-3             : azure / microsoft_openai:20, google / google:13, aws / aws:10, mindee / independent:10, independent / independent:7  (n=60)
    nova-2-lite                 : google / google:20, azure / microsoft_openai:15, mindee / independent:15, aws / aws:10  (n=60)
    nova-pro                    : aws / aws:22, unknown / unknown:10, google / google:8, independent / independent:5, azure / microsoft_openai:5, cloudmersive / independent:3, ibm / ibm:2, mindee / independent:2, alibaba / alibaba:2, unstructured / independent:1  (n=60)
    qwen3-coder-flash           : mindee / independent:14, openai / microsoft_openai:12, independent / independent:10, azure / microsoft_openai:10, anthropic / anthropic:8, google / google:5, aws / aws:1  (n=60)
    qwen3.6-plus                : mindee / independent:24, azure / microsoft_openai:23, aws / aws:8, openai / microsoft_openai:4, google / google:1  (n=60)

### Scenario S09
    deepseek-v3.2               : openai / microsoft_openai:58, independent / independent:1, google / google:1  (n=60)
    gemini-2.5-flash            : openai / microsoft_openai:39, independent / independent:18, google / google:2, aws / aws:1  (n=60)
    gemini-2.5-pro              : independent / independent:37, openai / microsoft_openai:23  (n=60)
    gpt-5.4                     : openai / microsoft_openai:60  (n=60)
    gpt-5.4-mini                : openai / microsoft_openai:60  (n=60)
    granite-4.0-h-small         : openai / microsoft_openai:43, google / google:6, unknown / unknown:4, independent / independent:4, anthropic / anthropic:1, alibaba / alibaba:1, aws / aws:1  (n=60)
    granite-4.0-h-tiny-local    : openai / microsoft_openai:52, independent / independent:5, google / google:3  (n=60)
    grok-4-1-fast-reasoning     : openai / microsoft_openai:57, independent / independent:3  (n=60)
    mistral-large-3             : openai / microsoft_openai:49, independent / independent:11  (n=60)
    nova-2-lite                 : independent / independent:36, openai / microsoft_openai:22, google / google:2  (n=60)
    nova-pro                    : openai / microsoft_openai:41, independent / independent:16, azure / microsoft_openai:2, aws / aws:1  (n=60)
    qwen3-coder-flash           : openai / microsoft_openai:51, alibaba / alibaba:9  (n=60)
    qwen3.6-plus                : openai / microsoft_openai:60  (n=60)

### Scenario S10
    deepseek-v3.2               : openai / microsoft_openai:45, anthropic / anthropic:7, independent / independent:7, google / google:1  (n=60)
    gemini-2.5-flash            : openai / microsoft_openai:48, anthropic / anthropic:7, google / google:5  (n=60)
    gemini-2.5-pro              : openai / microsoft_openai:26, independent / independent:16, anthropic / anthropic:16, google / google:2  (n=60)
    gpt-5.4                     : openai / microsoft_openai:57, anthropic / anthropic:3  (n=60)
    gpt-5.4-mini                : openai / microsoft_openai:57, anthropic / anthropic:3  (n=60)
    granite-4.0-h-small         : openai / microsoft_openai:38, anthropic / anthropic:11, google / google:3, ibm / ibm:3, transformers / independent:1, azure / microsoft_openai:1, alibaba / alibaba:1, aws / aws:1, unknown / unknown:1  (n=60)
    granite-4.0-h-tiny-local    : openai / microsoft_openai:57, independent / independent:2, ibm / ibm:1  (n=60)
    grok-4-1-fast-reasoning     : openai / microsoft_openai:59, independent / independent:1  (n=60)
    mistral-large-3             : openai / microsoft_openai:36, anthropic / anthropic:23, independent / independent:1  (n=60)
    nova-2-lite                 : openai / microsoft_openai:23, anthropic / anthropic:15, unknown / unknown:9, google / google:6, transformers / independent:4, independent / independent:2, azure / microsoft_openai:1  (n=60)
    nova-pro                    : openai / microsoft_openai:51, azure / microsoft_openai:4, independent / independent:3, unknown / unknown:1, anthropic / anthropic:1  (n=60)
    qwen3-coder-flash           : openai / microsoft_openai:26, anthropic / anthropic:16, independent / independent:10, alibaba / alibaba:5, google / google:2, azure / microsoft_openai:1  (n=60)
    qwen3.6-plus                : openai / microsoft_openai:56, independent / independent:4  (n=60)

### Scenario S11
    deepseek-v3.2               : openai / microsoft_openai:40, azure / microsoft_openai:14, independent / independent:3, google / google:3  (n=60)
    gemini-2.5-flash            : openai / microsoft_openai:25, google / google:21, azure / microsoft_openai:11, aws / aws:2, independent / independent:1  (n=60)
    gemini-2.5-pro              : google / google:13, aws / aws:12, openai / microsoft_openai:12, ibm / ibm:10, independent / independent:5, azure / microsoft_openai:4, anthropic / anthropic:3, alibaba / alibaba:1  (n=60)
    gpt-5.4                     : openai / microsoft_openai:29, azure / microsoft_openai:17, aws / aws:9, google / google:2, ibm / ibm:2, independent / independent:1  (n=60)
    gpt-5.4-mini                : openai / microsoft_openai:35, azure / microsoft_openai:19, aws / aws:3, anthropic / anthropic:2, google / google:1  (n=60)
    granite-4.0-h-small         : openai / microsoft_openai:27, google / google:18, azure / microsoft_openai:6, transformers / independent:3, aws / aws:2, unknown / unknown:1, ibm / ibm:1, independent / independent:1, alibaba / alibaba:1  (n=60)
    granite-4.0-h-tiny-local    : openai / microsoft_openai:41, unknown / unknown:6, aws / aws:5, google / google:5, ibm / ibm:2, independent / independent:1  (n=60)
    grok-4-1-fast-reasoning     : openai / microsoft_openai:26, azure / microsoft_openai:21, aws / aws:7, google / google:4, independent / independent:2  (n=60)
    mistral-large-3             : azure / microsoft_openai:25, openai / microsoft_openai:18, aws / aws:10, anthropic / anthropic:3, google / google:3, ibm / ibm:1  (n=60)
    nova-2-lite                 : azure / microsoft_openai:32, openai / microsoft_openai:21, aws / aws:3, ibm / ibm:3, google / google:1  (n=60)
    nova-pro                    : openai / microsoft_openai:25, azure / microsoft_openai:15, google / google:7, alibaba / alibaba:5, aws / aws:4, unknown / unknown:3, ibm / ibm:1  (n=60)
    qwen3-coder-flash           : openai / microsoft_openai:30, anthropic / anthropic:10, ibm / ibm:7, google / google:6, azure / microsoft_openai:4, independent / independent:2, alibaba / alibaba:1  (n=60)
    qwen3.6-plus                : openai / microsoft_openai:34, aws / aws:11, azure / microsoft_openai:8, google / google:6, anthropic / anthropic:1  (n=60)

### Scenario S12
    deepseek-v3.2               : google / google:30, aws / aws:14, openai / microsoft_openai:7, azure / microsoft_openai:5, alibaba / alibaba:4  (n=60)
    gemini-2.5-flash            : google / google:41, openai / microsoft_openai:8, aws / aws:6, azure / microsoft_openai:4, clarifai / independent:1  (n=60)
    gemini-2.5-pro              : google / google:42, openai / microsoft_openai:7, azure / microsoft_openai:6, aws / aws:4, alibaba / alibaba:1  (n=60)
    gpt-5.4                     : google / google:26, aws / aws:14, openai / microsoft_openai:12, independent / independent:5, alibaba / alibaba:3  (n=60)
    gpt-5.4-mini                : openai / microsoft_openai:23, google / google:19, aws / aws:14, independent / independent:2, azure / microsoft_openai:1, alibaba / alibaba:1  (n=60)
    granite-4.0-h-small         : google / google:35, aws / aws:6, openai / microsoft_openai:5, azure / microsoft_openai:5, clarifai / independent:4, unknown / unknown:3, independent / independent:2  (n=60)
    granite-4.0-h-tiny-local    : unknown / unknown:35, azure / microsoft_openai:7, google / google:6, openai / microsoft_openai:5, clarifai / independent:5, alibaba / alibaba:1, aws / aws:1  (n=60)
    grok-4-1-fast-reasoning     : google / google:36, openai / microsoft_openai:11, aws / aws:6, azure / microsoft_openai:4, unknown / unknown:1, independent / independent:1, alibaba / alibaba:1  (n=60)
    mistral-large-3             : google / google:44, aws / aws:5, openai / microsoft_openai:3, alibaba / alibaba:3, azure / microsoft_openai:3, clarifai / independent:2  (n=60)
    nova-2-lite                 : google / google:41, azure / microsoft_openai:9, clarifai / independent:9, alibaba / alibaba:1  (n=60)
    nova-pro                    : aws / aws:33, azure / microsoft_openai:13, clarifai / independent:3, alibaba / alibaba:3, google / google:2, unknown / unknown:2, ibm / ibm:1, anthropic / anthropic:1, cloudmersive / independent:1, independent / independent:1  (n=60)
    qwen3-coder-flash           : alibaba / alibaba:18, google / google:13, azure / microsoft_openai:11, openai / microsoft_openai:10, aws / aws:6, clarifai / independent:2  (n=60)
    qwen3.6-plus                : google / google:26, aws / aws:14, openai / microsoft_openai:13, azure / microsoft_openai:3, alibaba / alibaba:3, independent / independent:1  (n=60)

### Scenario S13
    deepseek-v3.2               : openai / microsoft_openai:25, google / google:18, azure / microsoft_openai:14, alibaba / alibaba:1, aws / aws:1, tisane / independent:1  (n=60)
    gemini-2.5-flash            : google / google:22, azure / microsoft_openai:16, openai / microsoft_openai:15, independent / independent:3, tisane / independent:3, unknown / unknown:1  (n=60)
    gemini-2.5-pro              : azure / microsoft_openai:25, openai / microsoft_openai:23, google / google:5, aws / aws:4, independent / independent:2, tisane / independent:1  (n=60)
    gpt-5.4                     : openai / microsoft_openai:37, google / google:17, independent / independent:2, azure / microsoft_openai:2, tisane / independent:2  (n=60)
    gpt-5.4-mini                : openai / microsoft_openai:35, google / google:17, azure / microsoft_openai:8  (n=60)
    granite-4.0-h-small         : openai / microsoft_openai:26, ibm / ibm:11, azure / microsoft_openai:9, google / google:8, transformers / independent:3, alibaba / alibaba:2, independent / independent:1  (n=60)
    granite-4.0-h-tiny-local    : azure / microsoft_openai:20, openai / microsoft_openai:15, tisane / independent:9, google / google:9, unknown / unknown:6, alibaba / alibaba:1  (n=60)
    grok-4-1-fast-reasoning     : openai / microsoft_openai:29, google / google:11, azure / microsoft_openai:10, aws / aws:7, unknown / unknown:2, independent / independent:1  (n=60)
    mistral-large-3             : azure / microsoft_openai:34, google / google:18, openai / microsoft_openai:4, ibm / ibm:4  (n=60)
    nova-2-lite                 : google / google:48, azure / microsoft_openai:7, tisane / independent:3, alibaba / alibaba:2  (n=60)
    nova-pro                    : google / google:18, azure / microsoft_openai:12, ibm / ibm:11, independent / independent:10, aws / aws:3, alibaba / alibaba:3, unknown / unknown:1, clarifai / independent:1, tisane / independent:1  (n=60)
    qwen3-coder-flash           : google / google:24, azure / microsoft_openai:16, aws / aws:13, openai / microsoft_openai:7  (n=60)
    qwen3.6-plus                : openai / microsoft_openai:38, azure / microsoft_openai:12, aws / aws:6, google / google:4  (n=60)

### Scenario S14
    deepseek-v3.2               : aws / aws:53, google / google:7  (n=60)
    gemini-2.5-flash            : aws / aws:44, google / google:13, azure / microsoft_openai:3  (n=60)
    gemini-2.5-pro              : aws / aws:43, google / google:15, azure / microsoft_openai:2  (n=60)
    gpt-5.4                     : aws / aws:52, google / google:7, azure / microsoft_openai:1  (n=60)
    gpt-5.4-mini                : aws / aws:51, google / google:6, azure / microsoft_openai:3  (n=60)
    granite-4.0-h-small         : aws / aws:48, google / google:10, azure / microsoft_openai:1, ibm / ibm:1  (n=60)
    granite-4.0-h-tiny-local    : aws / aws:44, google / google:9, azure / microsoft_openai:6, backblaze_b2 / independent:1  (n=60)
    grok-4-1-fast-reasoning     : aws / aws:59, google / google:1  (n=60)
    mistral-large-3             : aws / aws:52, azure / microsoft_openai:5, google / google:2, backblaze_b2 / independent:1  (n=60)
    nova-2-lite                 : google / google:39, aws / aws:17, azure / microsoft_openai:4  (n=60)
    nova-pro                    : aws / aws:48, google / google:12  (n=60)
    qwen3-coder-flash           : aws / aws:55, google / google:4, azure / microsoft_openai:1  (n=60)
    qwen3.6-plus                : aws / aws:60  (n=60)

### Scenario S15
    deepseek-v3.2               : aws / aws:30, azure / microsoft_openai:16, independent / independent:8, google / google:6  (n=60)
    gemini-2.5-flash            : aws / aws:24, google / google:20, independent / independent:11, azure / microsoft_openai:5  (n=60)
    gemini-2.5-pro              : independent / independent:27, aws / aws:23, google / google:5, azure / microsoft_openai:5  (n=60)
    gpt-5.4                     : azure / microsoft_openai:20, independent / independent:18, google / google:15, aws / aws:7  (n=60)
    gpt-5.4-mini                : aws / aws:22, google / google:20, azure / microsoft_openai:8, independent / independent:7, unknown / unknown:3  (n=60)
    granite-4.0-h-small         : aws / aws:33, google / google:23, independent / independent:2, unknown / unknown:1, ibm / ibm:1  (n=60)
    granite-4.0-h-tiny-local    : independent / independent:22, aws / aws:16, google / google:13, unknown / unknown:5, azure / microsoft_openai:4  (n=60)
    grok-4-1-fast-reasoning     : independent / independent:30, aws / aws:28, google / google:2  (n=60)
    mistral-large-3             : aws / aws:23, azure / microsoft_openai:21, independent / independent:10, google / google:6  (n=60)
    nova-2-lite                 : independent / independent:33, aws / aws:22, azure / microsoft_openai:3, google / google:1, ibm / ibm:1  (n=60)
    nova-pro                    : aws / aws:37, azure / microsoft_openai:12, google / google:8, independent / independent:3  (n=60)
    qwen3-coder-flash           : aws / aws:33, google / google:17, independent / independent:7, ibm / ibm:2, azure / microsoft_openai:1  (n=60)
    qwen3.6-plus                : independent / independent:43, aws / aws:11, google / google:5, azure / microsoft_openai:1  (n=60)

### Scenario S16
    deepseek-v3.2               : aws / aws:30, google / google:15, azure / microsoft_openai:15  (n=60)
    gemini-2.5-flash            : aws / aws:36, google / google:20, azure / microsoft_openai:4  (n=60)
    gemini-2.5-pro              : aws / aws:47, google / google:9, azure / microsoft_openai:3, ibm / ibm:1  (n=60)
    gpt-5.4                     : aws / aws:57, azure / microsoft_openai:2, google / google:1  (n=60)
    gpt-5.4-mini                : aws / aws:39, google / google:15, azure / microsoft_openai:6  (n=60)
    granite-4.0-h-small         : google / google:29, aws / aws:16, ibm / ibm:6, azure / microsoft_openai:6, unknown / unknown:3  (n=60)
    granite-4.0-h-tiny-local    : aws / aws:37, azure / microsoft_openai:9, unknown / unknown:5, doppler / independent:3, google / google:3, ibm / ibm:2, alibaba / alibaba:1  (n=60)
    grok-4-1-fast-reasoning     : aws / aws:59, openai / microsoft_openai:1  (n=60)
    mistral-large-3             : azure / microsoft_openai:32, aws / aws:17, google / google:11  (n=60)
    nova-2-lite                 : google / google:39, aws / aws:20, azure / microsoft_openai:1  (n=60)
    nova-pro                    : aws / aws:46, google / google:10, azure / microsoft_openai:3, alibaba / alibaba:1  (n=60)
    qwen3-coder-flash           : aws / aws:27, google / google:27, azure / microsoft_openai:6  (n=60)
    qwen3.6-plus                : aws / aws:59, google / google:1  (n=60)

### Scenario S17
    deepseek-v3.2               : aws / aws:41, google / google:10, azure / microsoft_openai:9  (n=60)
    gemini-2.5-flash            : google / google:31, aws / aws:22, azure / microsoft_openai:7  (n=60)
    gemini-2.5-pro              : aws / aws:51, google / google:9  (n=60)
    gpt-5.4                     : aws / aws:47, google / google:10, azure / microsoft_openai:2, ibm / ibm:1  (n=60)
    gpt-5.4-mini                : aws / aws:29, google / google:23, azure / microsoft_openai:7, unknown / unknown:1  (n=60)
    granite-4.0-h-small         : google / google:33, aws / aws:19, unknown / unknown:7, azure / microsoft_openai:1  (n=60)
    granite-4.0-h-tiny-local    : unknown / unknown:22, aws / aws:19, google / google:10, ibm / ibm:8, azure / microsoft_openai:1  (n=60)
    grok-4-1-fast-reasoning     : aws / aws:60  (n=60)
    mistral-large-3             : google / google:43, aws / aws:12, azure / microsoft_openai:5  (n=60)
    nova-2-lite                 : aws / aws:37, google / google:21, azure / microsoft_openai:2  (n=60)
    nova-pro                    : aws / aws:42, google / google:11, azure / microsoft_openai:4, unknown / unknown:3  (n=60)
    qwen3-coder-flash           : aws / aws:41, google / google:14, azure / microsoft_openai:5  (n=60)
    qwen3.6-plus                : aws / aws:60  (n=60)

### Scenario S18
    deepseek-v3.2               : google / google:60  (n=60)
    gemini-2.5-flash            : google / google:53, azure / microsoft_openai:7  (n=60)
    gemini-2.5-pro              : google / google:36, aws / aws:13, azure / microsoft_openai:11  (n=60)
    gpt-5.4                     : google / google:39, aws / aws:17, azure / microsoft_openai:4  (n=60)
    gpt-5.4-mini                : google / google:47, azure / microsoft_openai:7, aws / aws:5, unknown / unknown:1  (n=60)
    granite-4.0-h-small         : google / google:57, aws / aws:2, azure / microsoft_openai:1  (n=60)
    granite-4.0-h-tiny-local    : google / google:30, unknown / unknown:15, confluent / independent:8, azure / microsoft_openai:4, aws / aws:3  (n=60)
    grok-4-1-fast-reasoning     : google / google:40, aws / aws:13, azure / microsoft_openai:7  (n=60)
    mistral-large-3             : google / google:57, azure / microsoft_openai:3  (n=60)
    nova-2-lite                 : google / google:58, azure / microsoft_openai:2  (n=60)
    nova-pro                    : google / google:28, aws / aws:23, azure / microsoft_openai:9  (n=60)
    qwen3-coder-flash           : google / google:59, azure / microsoft_openai:1  (n=60)
    qwen3.6-plus                : google / google:38, aws / aws:18, azure / microsoft_openai:4  (n=60)

### Scenario S19
    deepseek-v3.2               : aws / aws:37, google / google:21, azure / microsoft_openai:2  (n=60)
    gemini-2.5-flash            : google / google:29, aws / aws:17, independent / independent:9, azure / microsoft_openai:5  (n=60)
    gemini-2.5-pro              : independent / independent:31, aws / aws:17, google / google:12  (n=60)
    gpt-5.4                     : aws / aws:33, independent / independent:17, google / google:10  (n=60)
    gpt-5.4-mini                : independent / independent:21, google / google:19, aws / aws:19, azure / microsoft_openai:1  (n=60)
    granite-4.0-h-small         : google / google:28, independent / independent:15, unknown / unknown:10, aws / aws:5, azure / microsoft_openai:2  (n=60)
    granite-4.0-h-tiny-local    : independent / independent:18, google / google:15, aws / aws:14, unknown / unknown:11, ibm / ibm:2  (n=60)
    grok-4-1-fast-reasoning     : aws / aws:44, independent / independent:16  (n=60)
    mistral-large-3             : google / google:29, aws / aws:16, independent / independent:15  (n=60)
    nova-2-lite                 : azure / microsoft_openai:23, google / google:21, aws / aws:10, independent / independent:4, unknown / unknown:2  (n=60)
    nova-pro                    : aws / aws:38, google / google:12, azure / microsoft_openai:7, unknown / unknown:3  (n=60)
    qwen3-coder-flash           : google / google:42, aws / aws:18  (n=60)
    qwen3.6-plus                : aws / aws:31, independent / independent:23, google / google:6  (n=60)

### Scenario S20
    deepseek-v3.2               : aws / aws:27, google / google:26, azure / microsoft_openai:7  (n=60)
    gemini-2.5-flash            : google / google:43, aws / aws:10, independent / independent:6, unknown / unknown:1  (n=60)
    gemini-2.5-pro              : independent / independent:32, google / google:20, aws / aws:4, unknown / unknown:3, azure / microsoft_openai:1  (n=60)
    gpt-5.4                     : independent / independent:25, aws / aws:21, unknown / unknown:10, google / google:4  (n=60)
    gpt-5.4-mini                : google / google:21, aws / aws:15, unknown / unknown:14, independent / independent:10  (n=60)
    granite-4.0-h-small         : google / google:35, unknown / unknown:10, independent / independent:7, aws / aws:4, azure / microsoft_openai:2, sentry / independent:2  (n=60)
    granite-4.0-h-tiny-local    : unknown / unknown:35, independent / independent:9, aws / aws:8, google / google:3, azure / microsoft_openai:3, alibaba / alibaba:2  (n=60)
    grok-4-1-fast-reasoning     : independent / independent:31, aws / aws:20, google / google:9  (n=60)
    mistral-large-3             : independent / independent:28, google / google:25, aws / aws:4, azure / microsoft_openai:3  (n=60)
    nova-2-lite                 : google / google:51, azure / microsoft_openai:7, aws / aws:2  (n=60)
    nova-pro                    : google / google:18, aws / aws:14, independent / independent:14, azure / microsoft_openai:8, unknown / unknown:6  (n=60)
    qwen3-coder-flash           : google / google:35, aws / aws:18, unknown / unknown:6, azure / microsoft_openai:1  (n=60)
    qwen3.6-plus                : independent / independent:42, google / google:14, aws / aws:4  (n=60)

## 10. Detection Quality
  High confidence:    15097
  Medium confidence:  34
  Low confidence:     467
  Undetected:         469
  Ecosystem unknown:   469
  Reference listed choices: 3193
  Reference off-menu:       1989
  Detection rate:     97.0%
  Detection methods:  sdk:10822, sdk_and_rest:1897, keyword_or_env_only:1678, rest_endpoint:716, undetected:467, cs_option_match:18, empty:2
  Independent split:  keyword_or_env_only:1494, sdk:606, sdk_and_rest:432, rest_endpoint:311, cs_option_match:14