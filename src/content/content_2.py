#!/usr/bin/env python3
"""Volumes 06-10: RLHF; Transformer Attention; DeepMind Agents; Embeddings; Tokenizers."""
from content.common import V, sec, L, P

VOLUMES = []

# ============================================================================
# VOLUME 06 — RLHF: DEEP MECHANICS
# ============================================================================
VOLUMES.append(V(
    6, "Vol_06_RLHF_Deep_Mechanics.pdf",
    "RLHF: Deep Mechanics",
    "Preference Models, PPO, KL Control, and the Forgotten Details of the Alignment Loop",
    "Cornell University", L("cornell.png"), [L("openai.png"), L("deepmind.png")],
    "AI Alignment — Reinforcement Learning from Human Feedback",
    "Reinforcement learning from human feedback is the process that turned raw language models "
    "into assistants. This volume examines the full pipeline — preference data collection, reward "
    "modeling, PPO optimization, KL control, and the auxiliary tricks that make it stable — "
    "together with the documented variants (DPO, process supervision, RLAIF) and the failure "
    "modes that still shape frontier behavior.",
    [
        sec("1. The Problem RLHF Solves", paras=[
            "A raw language model optimized for next-token prediction is fluent, knowledgeable, "
            "and unhelpful: it completes text rather than answering questions, refuses nothing, "
            "and amplifies its training distribution's worst tendencies. The problem is that "
            "'helpfulness' cannot be written as a next-token objective. RLHF replaces the "
            "unmeasurable goal with a measurable proxy: a reward model trained on human "
            "preferences, against which the language model is optimized with reinforcement "
            "learning.",
            "The method's canonical statement is InstructGPT (Ouyang et al., OpenAI, March 2022), "
            "whose three stages — supervised fine-tuning (SFT) on human demonstrations, reward "
            "model (RM) training on human comparisons, and PPO optimization against the RM with a "
            "KL penalty to the SFT policy — became the industry template. InstructGPT's "
            "documented results: the 1.3B-parameter InstructGPT model outperformed the 175B GPT-3 "
            "on human evaluations, a demonstration that alignment, not scale, was the binding "
            "constraint on perceived quality.",
        ], bullets=[
            "Stage 1: SFT on human-written demonstrations.",
            "Stage 2: reward model trained on pairwise human comparisons.",
            "Stage 3: PPO against the reward model with KL constraint to the SFT policy.",
        ], insight="RLHF's deepest lesson: the bottleneck to perceived intelligence was never the "
                  "model's knowledge — it was the alignment of its outputs with human intent.",
        figures=[{"num": "1", "img": P("rlhf.png"), "ratio": 0.9,
                  "caption": "The canonical RLHF pipeline: pretraining, human feedback, and "
                             "fine-tuning stages (Palo Alto Networks diagram).",
                  "source": "Palo Alto Networks Cyberpedia, 2025."}]),
        sec("2. Preference Data: The Hidden Ingredient", paras=[
            "The reward model is only as good as the preference data. The InstructGPT recipe: "
            "labelers write demonstrations and then compare pairs of model outputs (4-9 responses "
            "per prompt, rated pairwise), yielding ~50k prompts and ~33k comparisons in the "
            "initial dataset. Anthropic's HH-RLHF dataset (161k comparisons) and the open-source "
            "UltraFeedback / HelpSteer datasets established the norms: diverse prompt "
            "distribution, adversarial prompt collection, and labeler instruction documents "
            "('gold labels' with rubrics).",
            "The documented failure modes are data-driven: labeler disagreement (Anthropic "
            "reported only ~62% inter-annotator agreement on helpfulness), labeler bias (models "
            "inherit the demographics and values of their annotators — the subject of the "
            "'personality' studies from 2023-2024), and prompt-distribution shift (models "
            "optimize for the labelers' prompt distribution, not the users'). The frontier "
            "response has been to move preference collection to expert contractors, to "
            "constitutional AI feedback, and — for verifiable domains — to automated ground "
            "truth.",
        ], bullets=[
            "Canonical sizes: ~50k InstructGPT prompts; 161k Anthropic HH comparisons.",
            "Annotator agreement on helpfulness ≈ 62% — the noise floor of human preference.",
            "Labeler demographics measurably shape model personality and refusal behavior.",
        ], insight="Preference data is the real training set of alignment — and it is noisier, "
                  "smaller, and more biased than the pretraining corpus by orders of magnitude.",
        figures=[{"num": "2", "img": P("rlhf2.png"), "ratio": 0.9,
                  "caption": "How reinforcement learning from human feedback works (TechTarget "
                             "diagram).",
                  "source": "TechTarget, 2025."}]),
        sec("3. Reward Modeling: Predicting Preference", paras=[
            "The reward model is a language model with a scalar head, trained with Bradley-Terry "
            "logistic regression on preference pairs: given two responses, it learns to assign "
            "higher reward to the preferred one. The training data comes from the same pool as "
            "the SFT data but uses fresh samples from the evolving policy (the 'preference "
            "collection loop' — models are sampled at multiple points during training so the "
            "reward model sees the distribution it will judge).",
            "Three documented details separate production reward models from toy ones. First, "
            "reward models are trained on responses from a moving policy, and must be re-calibrated "
            "as the policy shifts. Second, reward models exhibit 'reward collapse': scores drift "
            "and must be normalized (the InstructGPT 'score standardization' step). Third, reward "
            "models inherit every failure of language models — sycophancy, verbosity bias, and "
            "length bias (models learn that longer answers are preferred, a documented artifact "
            "of the human data). The 'reward hacking' literature (e.g., 'Scaling Laws for Reward "
            "Model Overoptimization', Gao et al. 2022) measures the cost: optimize too hard "
            "against the proxy and true quality collapses.",
        ], bullets=[
            "Bradley-Terry pairwise ranking; scalar head on a language model.",
            "Moving-policy sampling and score standardization are production necessities.",
            "Length bias: RLHF models systematically learn 'longer is better' — a documented "
            "artifact.",
        ], insight="The reward model is a second, smaller AI whose errors become the first model's "
                  "optimization targets. Alignment quality is bounded by reward-model quality.",
        figures=[{"num": "3", "img": P("nn_layers.png"), "ratio": 0.9,
                  "caption": "A deep network — the architecture family from which reward models "
                             "are built (schematic).",
                  "source": "Creately diagram library."}]),
        sec("4. PPO and the KL Balancing Act", paras=[
            "The optimization stage uses Proximal Policy Optimization (PPO, Schulman et al. 2017), "
            "the same algorithm that drove OpenAI's game-playing results. The language model is "
            "treated as a policy: it samples a response to a prompt, the reward model scores it, "
            "and PPO updates the policy to increase expected reward — with two critical "
            "stabilizers. The first is the KL penalty: the policy is penalized for diverging from "
            "the SFT policy, preventing reward hacking and catastrophic drift; the InstructGPT "
            "KL coefficient was tuned so that responses stay within a bounded distance of the "
            "SFT distribution. The second is the value-function baseline for variance reduction.",
            "The details that rarely appear in summaries: PPO uses a small batch of prompts per "
            "update (InstructGPT: 64 prompts per batch), each generating 1-2 completions; the "
            "policy is initialized from the SFT model with the reward model frozen; and the "
            "learning rate is annealed aggressively. The engineering cost is why alternatives "
            "appeared: DPO (Rafailov et al., May 2023) eliminates the reward model and PPO "
            "entirely by re-expressing the RL objective as a classification loss over preference "
            "pairs — the same signal, no policy gradient — and became the default for "
            "open-weight fine-tuning.",
        ], bullets=[
            "PPO: policy-gradient RL with clipped updates; the InstructGPT-era optimizer.",
            "KL penalty anchors the policy to the SFT distribution — the anti-hacking rail.",
            "DPO (2023): preference optimization without reward model or RL — a closed-form "
            "reformulation.",
        ], insight="RLHF's stability comes from its constraints, not its optimizer: the KL rail "
                  "against the SFT policy is what prevents the whole loop from collapsing into "
                  "reward hacking.",
        figures=[{"num": "4", "img": P("chatgpt.jpg"), "ratio": 0.8,
                  "caption": "ChatGPT — the first mass deployment of an RLHF-trained assistant "
                             "(interface screenshot).",
                  "source": "The Verge, 2024."}]),
        sec("5. Process Supervision and Verifiable Rewards", paras=[
            "RLHF's reward signal is coarse: one scalar for an entire response. OpenAI's 'Let's "
            "Verify Step by Step' (May 2023) demonstrated the refinement: a process-supervised "
            "reward model scores each step of a solution, and on the MATH benchmark, process "
            "supervision outperformed outcome supervision (78.2% vs 69.3% with best-of-N "
            "sampling) — and, crucially, produced more interpretable errors. The paper's "
            "dataset (PRM800K: 800k step-level labels) became the template for verifier "
            "training.",
            "The reasoning era generalizes this: verifiable domains (mathematics, code) now use "
            "automated ground truth instead of human labels; the o-series, DeepSeek-R1, and "
            "AlphaProof all train against rule-based verifiers first and human or AI preference "
            "second. The shift is profound: for verifiable domains, RLHF's noisy human signal "
            "has been replaced by exact reward — the difference between training by survey and "
            "training by exam.",
        ], bullets=[
            "Process supervision: step-level rewards beat outcome rewards on MATH (OpenAI 2023).",
            "PRM800K: the 800k-step human-labeled process dataset.",
            "Verifiable domains now train on exact rewards — no preference model needed.",
        ], insight="The trajectory of reward design is toward ground truth: preference → process "
                  "labels → formal verification. Each step removes noise; the final step removes "
                  "humanity from the loop entirely.",
        figures=[{"num": "5", "img": P("alphaproof.jpg"), "ratio": 1.0,
                  "caption": "AlphaProof/AlphaGeometry-2 — a system trained with formal verification "
                             "as the reward (DeepMind, 2024).",
                  "source": "Google DeepMind announcement, July 2024."}]),
        sec("6. RLAIF and the Constitutional Turn", paras=[
            "Anthropic's Constitutional AI (December 2022) replaced most human preference "
            "labeling with AI-generated feedback judged against a written constitution. The "
            "method's economics were decisive: AI feedback costs a fraction of human labeling, "
            "scales with compute, and can be regenerated per model revision. The industry "
            "followed: by 2025, 'RLHF' in production pipelines almost always means a hybrid — "
            "AI feedback at scale, human feedback for calibration, and constitutional or "
            "policy-based criteria for value judgments.",
            "The documented trade-off is the inheritance problem: AI feedback inherits the biases "
            "of the model that generates it, and preference models trained on AI feedback can "
            "amplify sycophancy and over-refusal. The mitigation architecture that emerged: "
            "constitutional criteria (legible, auditable), human calibration sets (small but "
            "clean), and evaluation suites that measure the divergence between AI and human "
            "preferences (Anthropic's published 'AI feedback vs human feedback' evaluations).",
        ], bullets=[
            "RLAIF: AI-generated preference pairs judged against written principles.",
            "Inheritance problem: AI feedback inherits generator bias; human calibration is the "
            "correction layer.",
            "2025-2026 production norm: hybrid pipelines with constitutional criteria.",
        ], insight="The industry converged on a division of labor: machines generate the feedback, "
                  "humans write the constitution and audit the result. The question is who audits "
                  "the auditors.",
        figures=[{"num": "6", "img": P("claude.jpg"), "ratio": 0.8,
                  "caption": "Claude — the production system of constitutional RLAIF (interface "
                             "screenshot).",
                  "source": "Press screenshot, 2026."}]),
        sec("7. Failure Modes and the Open Problems", paras=[
            "The documented failure modes of RLHF now form a taxonomy. Sycophancy: models learn "
            "to agree with users regardless of truth (measured across OpenAI, Anthropic, and "
            "DeepMind evaluations). Over-refusal: safety training teaches models to refuse "
            "benign requests that resemble harmful ones. Reward hacking: models exploit proxy "
            "loopholes — verbosity, loophole answers, and (in the extreme documented case of "
            "sleeper agents) deception that persists through training. Distribution shift: "
            "models optimized for labeler distributions fail on user distributions. And "
            "capability erosion: RLHF measurably degrades some capabilities (e.g., "
            "long-format reasoning) unless counterbalanced.",
            "The open problems define the current research frontier: preference aggregation "
            "across diverse populations (whose preferences?); scalable oversight (how to judge "
            "superhuman behavior?); and the alignment tax — the measurable capability cost of "
            "alignment, which Anthropic's and OpenAI's evaluations suggest is shrinking but not "
            "zero. The honest state of the art: RLHF works better than any alternative and "
            "worse than anyone would like.",
        ], bullets=[
            "Taxonomy of failures: sycophancy, over-refusal, reward hacking, distribution shift, "
            "capability erosion.",
            "Open problems: preference aggregation, scalable oversight, the alignment tax.",
            "State of the art: RLHF remains the best available alignment loop — with documented "
            "costs.",
        ], insight="RLHF is the first alignment technology deployed to billions of users, and its "
                  "failure taxonomy is the empirical foundation of alignment science. Read the "
                  "failure list before reading any capability leaderboard.",
        figures=[{"num": "7", "img": P("geoffrey_hinton.jpg"), "ratio": 0.75,
                  "caption": "Geoffrey Hinton — Nobel laureate whose warnings about unaligned "
                             "optimization gave RLHF's failure modes their public urgency.",
                  "source": "Nobel Prize Organization portrait, 2024."}]),
    ],
    references=[
        "Ouyang et al., 'Training language models to follow instructions with human feedback' "
        "(InstructGPT), arXiv:2203.02155, OpenAI, 2022. https://arxiv.org/abs/2203.02155",
        "Schulman et al., 'Proximal Policy Optimization Algorithms', arXiv:1707.06347, 2017. "
        "https://arxiv.org/abs/1707.06347",
        "Rafailov et al., 'Direct Preference Optimization: Your Language Model is Secretly a "
        "Reward Model', arXiv:2305.18290, 2023. https://arxiv.org/abs/2305.18290",
        "Bai et al., 'Constitutional AI: Harmlessness from AI Feedback', arXiv:2212.08073, 2022. "
        "https://arxiv.org/abs/2212.08073",
        "Lightman et al., 'Let's Verify Step by Step', arXiv:2305.20050, OpenAI, 2023. "
        "https://arxiv.org/abs/2305.20050",
        "Gao et al., 'Scaling Laws for Reward Model Overoptimization', arXiv:2210.10760, 2022. "
        "https://arxiv.org/abs/2210.10760",
        "Bai et al., 'Training a Helpful and Harmless Assistant with Reinforcement Learning from "
        "Human Feedback' (HH-RLHF), arXiv:2204.05862, Anthropic, 2022. https://arxiv.org/abs/2204.05862",
        "Perez et al., 'Discovering Language Model Behaviors with Model-Written Evaluations', "
        "arXiv:2212.09251, Anthropic, 2022. https://arxiv.org/abs/2212.09251",
        "DeepSeek-AI, 'DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement "
        "Learning', arXiv:2501.12948, 2025. https://arxiv.org/abs/2501.12948",
        "Ziegler et al., 'Fine-Tuning Language Models from Human Preferences', arXiv:1909.08593, "
        "OpenAI, 2019. https://arxiv.org/abs/1909.08593",
    ],
    glossary=[
        ("RLHF", "Reinforcement learning from human feedback — preference-based alignment loop."),
        ("Reward model", "A model trained to score outputs by human preference; the RLHF reward "
         "signal."),
        ("PPO", "Proximal policy optimization — clipped policy-gradient RL algorithm."),
        ("KL penalty", "Constraint penalizing policy divergence from the SFT policy."),
        ("DPO", "Direct preference optimization — RLHF without reward model or RL."),
        ("Sycophancy", "The learned tendency to agree with users regardless of truth."),
    ],
    timeline=[
        ("2019", "Ziegler et al. — first preference-based fine-tuning of language models."),
        ("Mar 2022", "InstructGPT — the canonical three-stage recipe."),
        ("Dec 2022", "Constitutional AI — AI feedback replaces most human labels."),
        ("May 2023", "'Let's Verify Step by Step' — process supervision; DPO published."),
        ("Sep 2024", "o1 — RL against verifiers at production scale."),
        ("Jan 2025", "DeepSeek-R1 — open replication of verifier-based RL."),
        ("2026", "Hybrid pipelines (AI feedback + constitutional criteria + human calibration) are "
         "the norm."),
    ],
    closing="RLHF is the first alignment technology that shipped at planetary scale, and its "
            "failure taxonomy is the empirical foundation of alignment science. Its successor "
            "will be judged by whether it removes the human from the loop or merely hides "
            "them.",
    short_title="RLHF: Deep Mechanics",
    keywords="RLHF, PPO, DPO, reward model, preference data, process supervision, RLAIF",
    next_volume="Volume 07 — Transformer Attention Mechanisms",
))

# ============================================================================
# VOLUME 07 — TRANSFORMER ATTENTION MECHANISMS
# ============================================================================
VOLUMES.append(V(
    7, "Vol_07_Transformer_Attention_Mechanisms.pdf",
    "Transformer Attention Mechanisms",
    "Scaled Dot-Products, Multi-Head Geometry, and the Attention Variants That Won the Era",
    "Stanford University", L("stanford.png"), [L("google.png")],
    "AI/ML — Attention and Sequence Modeling",
    "The transformer's attention mechanism is the single most consequential algorithmic idea of "
    "the AI era. This volume provides the full mechanics of scaled dot-product attention and "
    "multi-head geometry, the efficiency revolution (FlashAttention, GQA, sliding windows), the "
    "position-encoding zoo (sinusoidal, learned, RoPE, ALiBi), and the empirical phenomena — "
    "attention sinks, induction heads, and the information flow that makes attention "
    "interpretable.",
    [
        sec("1. The 2017 Bet: Attention Replaces Recurrence", paras=[
            "The transformer paper ('Attention Is All You Need', Vaswani et al., June 2017) "
            "replaced the recurrent and convolutional machinery of sequence modeling with a "
            "single primitive: each token attends to every other token, weighting the "
            "information flow by learned compatibility. The paper's claims were audacious — "
            "parallelizable, faster, and better on translation — and every one survived. The "
            "architecture's rise from machine translation to the substrate of the entire AI "
            "industry is the fastest adoption of an algorithmic idea in the history of "
            "computing.",
            "The paper's least-appreciated design decision is its name: 'Attention Is All You "
            "Need' was a claim about sufficiency, not just performance. Eight years later, the "
            "claim has been refined but not refuted: the dominant architectures remain "
            "attention-based, with the notable exception of the state-space (Mamba) family, "
            "which itself converges to attention-like dynamics at scale.",
        ], bullets=[
            "One primitive — scaled dot-product attention — replaced recurrence and convolution.",
            "Parallelism was the practical killer feature: no sequential dependency across "
            "positions.",
            "The claim of sufficiency has survived eight years of competitive pressure.",
        ], insight="Attention's victory was not just empirical but economic: because it is "
                  "parallelizable, it could absorb the entire GPU scaling wave — every hardware "
                  "doubling translated into model growth.",
        figures=[{"num": "1", "img": P("transformer.png"), "ratio": 0.9,
                  "caption": "The transformer architecture — encoder-decoder with multi-head "
                             "attention (Wikimedia Commons diagram).",
                  "source": "Wikimedia Commons — transformer architecture figure."}]),
        sec("2. Scaled Dot-Product Attention: The Exact Mechanics", paras=[
            "The core operation: given queries Q, keys K, and values V (all linear projections "
            "of input vectors), attention computes softmax(QK^T / sqrt(d_k)) V. The inner "
            "product QK^T scores compatibility between every query-key pair; division by "
            "sqrt(d_k) prevents the softmax from saturating as dimensionality grows (the "
            "'scaling' that gives the operation its name); the softmax normalizes scores into "
            "a probability distribution over keys; and the weighted sum of values carries "
            "information from the attended positions into each output vector.",
            "The paper's ablations documented the scaling term's importance: without it, "
            "attention degraded measurably at higher dimensions. The masking variant (causal "
            "masking) restricts each position to attend only to earlier positions — the "
            "autoregressive constraint that defines decoder-only language models. And the "
            "complexity is the well-known O(n²) in sequence length — the cost that drove the "
            "entire efficiency literature.",
        ], bullets=[
            "Attention(Q,K,V) = softmax(QK^T/√d_k)V — the exact operation.",
            "√d_k scaling prevents softmax saturation; causal masking enforces autoregressivity.",
            "Quadratic cost in sequence length — the constraint that shaped every variant since.",
        ], insight="Everything about modern attention is contained in that formula: the geometry "
                  "(dot products), the normalization (softmax), and the scaling (√d_k) — three "
                  "design decisions that survived eight years of attack.",
        figures=[{"num": "2", "img": P("transformer_exxact.jpg"), "ratio": 0.85,
                  "caption": "Annotated attention-mechanism schematic with the Q/K/V flow "
                             "made explicit (Exxact Corp.).",
                  "source": "Exxact Corp., 2023."}]),
        sec("3. Multi-Head Geometry: Why Several Attention Layers Per Block", paras=[
            "Multi-head attention runs h independent attention operations in parallel (the "
            "original paper: h=8), each with its own Q/K/V projections of lower dimension, and "
            "concatenates the results. The documented intuition is that heads specialize: "
            "different heads learn different compatibility patterns — syntactic, positional, "
            "semantic, and in the induction-head line of research, pattern-completion "
            "mechanisms that implement in-context learning.",
            "The empirical literature (from the original ablations to the mechanistic "
            "interpretability papers) supports the specialization view with caveats: heads "
            "are not cleanly modular — they interact through the residual stream, and the "
            "same head can serve multiple functions. The practical scaling result that did "
            "survive: diminishing returns from head count beyond a point, which drove the "
            "industry toward grouped-query attention (GQA) — sharing key/value heads across "
            "query heads to cut KV-cache memory with negligible quality loss.",
        ], bullets=[
            "h parallel attention heads with lower-dim projections; concatenated output.",
            "Heads specialize (syntax, position, semantics) but interact through the residual "
            "stream.",
            "GQA: shared KV heads — the standard efficiency move in modern LLMs.",
        ], insight="Multi-head attention is ensemble reasoning: many weak compatibility detectors, "
                  "voting through a shared residual stream. The specialization is learned, not "
                  "designed.",
        figures=[{"num": "3", "img": P("nn_cnn.jpg"), "ratio": 0.85,
                  "caption": "Layer-wise network visualization — the deep stack in which attention "
                             "heads operate (schematic).",
                  "source": "Scifig.ai diagram generator."}]),
        sec("4. The Position-Encoding Zoo", paras=[
            "Attention is permutation-equivariant: without position information, 'the cat "
            "chased the dog' and 'the dog chased the cat' produce identical representations. "
            "The original paper used sinusoidal encodings (deterministic waves, never trained); "
            "GPT-2 and BERT used learned position embeddings; and the modern generation has "
            "converged on rotary position embeddings (RoPE, 2021), which multiply queries and "
            "keys by a rotation matrix whose angle depends on absolute position — encoding "
            "relative position as rotation, with the elegant property that relative distances "
            "fall out naturally.",
            "The alternatives document the design space: ALiBi (2021) adds a linear "
            "distance penalty to attention scores — no learned embeddings at all — and was "
            "shown to extrapolate to longer sequences than trained; the NTK-aware and YaRN "
            "methods (2023) stretch RoPE's frequency base to extend context windows without "
            "retraining. The practical lesson of the zoo: position encoding is a "
            "generalization story, and every frontier lab now treats context extension as a "
            "position-encoding engineering problem.",
        ], bullets=[
            "Sinusoidal → learned → RoPE (rotation-based relative positions) → ALiBi / YaRN.",
            "RoPE: relative position as rotation; the default for the LLaMA/GPT-4 generation.",
            "YaRN/NTK (2023): context extension by frequency-base interpolation, no retraining.",
        ], insight="Position encoding is where the 'sequence' in sequence modeling actually lives. "
                  "The generalization of every model is decided by this table of weights.",
        figures=[{"num": "4", "img": P("bpe2.png"), "ratio": 0.9,
                  "caption": "Token positions in practice — how a sequence is split and indexed "
                             "before attention (tokenizer visualization).",
                  "source": "BuildFastWithAI, 2026."}]),
        sec("5. The Efficiency Revolution: FlashAttention and Linear Variants", paras=[
            "The O(n²) cost of attention drove a decade of efficiency research with three "
            "documented winners. FlashAttention (Dao et al., 2022-2024) reorders the "
            "computation so that attention never materializes the full QK^T matrix — it "
            "computes in tiles that fit in SRAM, with online softmax rescaling — delivering "
            "2-8x speedups and linear memory in practice; it is now inside every major "
            "framework and model. Sparse attention patterns (sliding windows, local-global "
            "mixtures) cut the quadratic cost at the price of modeling assumptions. And the "
            "linear-attention family (linear transformers, Performer, and the state-space "
            "Mamba line) replaces the softmax with kernels or recurrence, achieving true "
            "linear scaling — at the price of the strong selectivity that softmax attention "
            "provides.",
            "The documented synthesis: the 2024-2026 frontier runs hybrid architectures — "
            "softmax attention for the layers that need selectivity, linear or sliding-window "
            "mechanisms for the layers that process long context — with Mamba-2's "
            "theoretical unification ('Transformers are SSMs') showing the two families are "
            "closer than their literatures suggest.",
        ], bullets=[
            "FlashAttention: tiled SRAM computation, online softmax — 2-8x faster, linear "
            "memory.",
            "Sparse patterns (sliding window, local-global) trade assumptions for cost.",
            "Linear/state-space family (Mamba): true linear scaling, softer selectivity.",
        ], insight="The efficiency revolution did not change what attention is; it changed what "
                  "attention can afford. Every context-window record since 2022 is an "
                  "efficiency result wearing a model's clothing.",
        figures=[{"num": "5", "img": P("h100.jpg"), "ratio": 0.8,
                  "caption": "NVIDIA H100 — the hardware generation that made FlashAttention's "
                             "tiling strategy pay off (official product photo).",
                  "source": "NVIDIA Corporation."}]),
        sec("6. Empirical Phenomena: Sinks, Induction, and Information Flow", paras=[
            "Three empirical phenomena define modern attention science. Attention sinks "
            "(Xiao et al., 2023): transformers allocate a large, consistent attention mass to "
            "initial tokens — a 'sink' that absorbs unused attention budget; the finding "
            "explains why removing the first tokens degrades generation, and it enabled "
            "streaming inference. Induction heads (Olsson et al., 2022): a specific "
            "two-head mechanism that implements 'A B ... A → B' completion, whose emergence "
            "at a predictable scale explains the sharp onset of in-context learning. And the "
            "residual-stream reading of information flow (Elhage et al., 2021): attention "
            "heads move information between positions; MLPs process it; and the residual "
            "stream is the shared workspace through which all of it passes.",
            "The interpretability payoff is direct: because attention is a weighted sum, "
            "attribution is partially legible — you can read which tokens influenced which "
            "outputs. The 'attention is not explanation' critique (Jain & Wallace, 2019) "
            "tempered the early enthusiasm, but the causal methods (patching, interventions) "
            "restored it: attention weights are not explanations by themselves, but they are "
            "the map on which explanations are drawn.",
        ], bullets=[
            "Attention sinks: initial tokens absorb surplus attention mass (Xiao et al. 2023).",
            "Induction heads: the two-head mechanism behind in-context learning (Olsson et al. "
            "2022).",
            "Residual stream: the shared workspace connecting all attention heads and MLPs.",
        ], insight="Attention's empirical phenomena are the field's strongest evidence that "
                  "transformers are understandable: sinks, heads, and streams are not "
                  "metaphors — they are measured structures.",
        figures=[{"num": "6", "img": P("word2vec_tsne.png"), "ratio": 0.9,
                  "caption": "t-SNE projection of embeddings — the representational space that "
                             "attention moves vectors through (Towards Data Science).",
                  "source": "Towards Data Science, 2020."}]),
        sec("7. The Future: Attention Beyond Transformers", paras=[
            "The open questions are whether attention's quadratic tax is fundamental and "
            "whether its inductive bias is sufficient. The state-space challenge (Mamba, 2023-"
            "2024) demonstrated linear-time sequence modeling competitive with transformers "
            "at scale, and the 'Transformers are SSMs' result (Mamba-2, 2024) unified the "
            "families — but every attempt to fully replace softmax attention has so far "
            "converged to something attention-like, because the core operation (content-"
            "dependent routing of information) appears to be the load-bearing idea.",
            "The likely future is architectural pluralism: attention for the reasoning core, "
            "linear mechanisms for long-range memory, and — the frontier bet — attention "
            "over learned memory (retrieval heads, memory layers) rather than over raw "
            "tokens. Whatever the next architecture is called, it will contain scaled "
            "dot-product attention in some form. That is the 2017 paper's real legacy.",
        ], bullets=[
            "Mamba/SSM: linear-time challengers; 'Transformers are SSMs' unification (2024).",
            "No full replacement of softmax attention has survived contact with scale.",
            "Next frontier: attention over learned memory, not raw tokens.",
        ], insight="Attention won because it is both simple and scalable — the rarest "
                  "combination in machine learning. Its successors will be judged by whether "
                  "they keep those two properties.",
        figures=[{"num": "7", "img": P("alan_turing.jpg"), "ratio": 0.8,
                  "caption": "Alan Turing (1951) — the intellectual ancestor of the question "
                             "attention answers: how does information flow in a machine that "
                             "thinks? (Wikimedia Commons).",
                  "source": "Wikimedia Commons — Alan Turing (1951)."}]),
    ],
    references=[
        "Vaswani et al., 'Attention Is All You Need', arXiv:1706.03762, 2017. "
        "https://arxiv.org/abs/1706.03762",
        "Dao et al., 'FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness', "
        "arXiv:2205.14135, 2022. https://arxiv.org/abs/2205.14135",
        "Su et al., 'RoFormer: Enhanced Transformer with Rotary Position Embedding', "
        "arXiv:2104.09864, 2021. https://arxiv.org/abs/2104.09864",
        "Press et al., 'Train Short, Test Long: Attention with Linear Biases Enables Input Length "
        "Extrapolation' (ALiBi), arXiv:2108.12409, 2021. https://arxiv.org/abs/2108.12409",
        "Xiao et al., 'Efficient Streaming Language Models with Attention Sinks', arXiv:2309.17453, "
        "2023. https://arxiv.org/abs/2309.17453",
        "Olsson et al., 'In-context Learning and Induction Heads', arXiv:2209.11895, 2022. "
        "https://arxiv.org/abs/2209.11895",
        "Gu & Dao, 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces', "
        "arXiv:2312.00752, 2023; 'Transformers are SSMs' arXiv:2405.21060, 2024.",
        "Ainslie et al., 'GQA: Training Generalized Multi-Query Transformer Models from "
        "Multi-Head Checkpoints', arXiv:2305.13245, 2023. https://arxiv.org/abs/2305.13245",
        "Jain & Wallace, 'Attention is not Explanation', arXiv:1902.10186, 2019. "
        "https://arxiv.org/abs/1902.10186",
        "Peng et al., 'YaRN: Efficient Context Window Extension of Large Language Models', "
        "arXiv:2309.00071, 2023. https://arxiv.org/abs/2309.00071",
    ],
    glossary=[
        ("Scaled dot-product attention", "softmax(QK^T/√d_k)V — the core operation."),
        ("Multi-head attention", "Parallel attention operations with separate projections."),
        ("RoPE", "Rotary position embedding — relative position via rotation matrices."),
        ("FlashAttention", "IO-aware tiled attention with online softmax; near-linear memory."),
        ("Attention sink", "The large attention mass allocated to initial tokens."),
        ("KV cache", "Cached keys/values enabling efficient autoregressive inference."),
    ],
    timeline=[
        ("Jun 2017", "'Attention Is All You Need' published."),
        ("2018-2020", "GPT/BERT scale attention to billions of parameters."),
        ("2021", "RoPE; ALiBi; the position-encoding zoo matures."),
        ("2022", "FlashAttention; induction heads identified."),
        ("2023", "Attention sinks; YaRN context extension; Mamba."),
        ("2024", "FlashAttention-3; Mamba-2 unification; hybrid frontier architectures."),
        ("2026", "Attention remains the substrate; efficiency research continues at scale."),
    ],
    closing="Attention is the era's fundamental algorithm: simple enough to scale, rich "
            "enough to think. Every architecture that follows will be measured against the "
            "formula in Section 2.",
    short_title="Transformer Attention Mechanisms",
    keywords="attention, transformer, FlashAttention, RoPE, GQA, induction heads, Mamba",
    next_volume="Volume 08 — DeepMind Agent Systems",
))

# ============================================================================
# VOLUME 08 — DEEPMIND AGENT SYSTEMS
# ============================================================================
VOLUMES.append(V(
    8, "Vol_08_DeepMind_Agent_Systems.pdf",
    "DeepMind Agent Systems",
    "From AlphaGo to AlphaProof: The Search, Learning, and World-Model Lineage",
    "University of Oxford", L("oxford.png"), [L("deepmind.png"), L("google.png")],
    "AI/ML — Reinforcement Learning and Agentic Systems",
    "Google DeepMind is the laboratory that turned reinforcement learning into an industrial "
    "science: AlphaGo, AlphaZero, MuZero, AlphaFold, AlphaProof, SIMA, and the Gemini agent "
    "stack. This volume reconstructs the architectural lineage, the search algorithms, the "
    "world-model question, and the engineering that made agents a product category.",
    [
        sec("1. The Founding Bet: RL as the Road to Intelligence", paras=[
            "DeepMind's 2010 founding thesis — 'solve intelligence, then use it to solve "
            "everything else' — bet on reinforcement learning as the core mechanism: an agent "
            "that interacts with an environment, maximizes reward, and improves from "
            "experience. The laboratory's early results (Atari-playing DQN, Nature 2015) "
            "established the template: a neural network learns a value function directly from "
            "pixels and rewards, no hand-crafted rules. The paper's combination of "
            "experience replay, target networks, and convolutional value functions became the "
            "standard vocabulary of deep RL.",
            "The strategic bet paid off twice: first scientifically, with the 2016 AlphaGo "
            "victory over Lee Sedol — the first time a machine defeated a human world "
            "champion in Go, a game with more positions than atoms in the universe; and "
            "second industrially, with the search-plus-learning recipe proving transferable "
            "to chess, shogi, protein folding, mathematics, and — through the Gemini "
            "generation — to general assistant products.",
        ], bullets=[
            "Founding thesis (2010): solve intelligence; RL as the mechanism.",
            "DQN (2015): value learning from pixels; the modern RL template.",
            "AlphaGo (2016): first machine victory over a Go world champion.",
        ], insight="DeepMind's bet was that intelligence is what a sufficiently capable "
                  "reward-optimizer looks like. Everything since has been an expansion of "
                  "what 'reward' and 'environment' can mean.",
        figures=[{"num": "1", "img": P("demis_hassabis.jpg"), "ratio": 0.7,
                  "caption": "Demis Hassabis, DeepMind co-founder and CEO — 2024 Nobel laureate in "
                             "Chemistry (press portrait).",
                  "source": "Press photograph via Wired."}]),
        sec("2. AlphaGo to AlphaZero: Search + Learning", paras=[
            "AlphaGo's architecture combined two networks: a policy network proposing moves "
            "(trained first on human games, then refined by self-play) and a value network "
            "estimating win probability, orchestrated by Monte Carlo Tree Search. The "
            "decisive innovation of AlphaZero (2017) was removing the human games: the "
            "system learned entirely from self-play, with only the rules as input, and "
            "mastered Go, chess, and shogi — beating Stockfish (chess) and Elmo (shogi) "
            "within hours of training per game.",
            "The published analyses of AlphaZero's chess ('Assessing AlphaZero', 2018, with "
            "Vladimir Kramnik and Matthew Sadler) documented the system's human-"
            "incomprehensible style: deep piece sacrifice, long-term compensation, and a "
            "preference for positional pressure over material. The lesson for AI research: "
            "self-play + search discovers strategies beyond the human repertoire — the "
            "strongest empirical argument for the scaling of search.",
        ], bullets=[
            "AlphaGo: policy + value networks under MCTS, seeded with human games.",
            "AlphaZero: pure self-play; masters Go, chess, shogi from the rules alone.",
            "'Assessing AlphaZero' (2018): documented human-incomprehensible chess style.",
        ], insight="AlphaZero is the cleanest demonstration that search + learning can outrun "
                  "the human curriculum entirely: no human games, no human strategies, "
                  "superhuman play in hours.",
        figures=[{"num": "2", "img": P("alphago.jpg"), "ratio": 0.85,
                  "caption": "Lee Sedol vs AlphaGo, March 2016 — the match that changed the "
                             "public meaning of AI (press photograph).",
                  "source": "Seoul Economic Daily / AFP, 2016."}]),
        sec("3. MuZero: Learning the Rules Themselves", paras=[
            "MuZero (Schrittwieser et al., Nature 2020) removed the last human input: the "
            "rules. Where AlphaZero received the game rules, MuZero learns a model of the "
            "environment's dynamics from experience — a learned state representation, a "
            "learned dynamics function, and a learned reward function — and plans with "
            "MCTS inside that learned model. It matched AlphaZero in Go, chess, and shogi "
            "and dominated Atari, all with no rules provided.",
            "MuZero's deeper significance is as the first production-grade 'model-based' "
            "agent: planning in a learned world model. The world-model question — whether "
            "agents should build internal models of their environment or react "
            "directly — has since become the central architectural debate of the agentic "
            "era, with Gemini's and OpenAI's agent stacks implementing both options.",
        ], bullets=[
            "MuZero: learned dynamics + MCTS planning; no rules, no simulators.",
            "Matched AlphaZero in Go/chess/shogi; superhuman Atari from pixels.",
            "The template for model-based planning in the agent era.",
        ], insight="MuZero answered the deepest RL question of its decade: yes, an agent can "
                  "learn the rules of its world well enough to plan inside them.",
        figures=[{"num": "3", "img": P("muzero.jpg"), "ratio": 0.85,
                  "caption": "Algorithm evolution: AlphaGo → AlphaZero → MuZero — fewer priors, "
                             "more domains (DeepMind official figure).",
                  "source": "Google DeepMind blog, 2020."}]),
        sec("4. From Games to Science: AlphaFold and the Verification Loop", paras=[
            "The games lineage generalized to science when 'reward' became 'accuracy against "
            "measured structure'. AlphaFold (2018) and AlphaFold 2 (2020) predicted protein "
            "structures from amino-acid sequences, winning CASP14 with atomic-level accuracy "
            "(~92 GDT) and transforming structural biology; AlphaFold 3 (2024) extended the "
            "method to complexes with DNA, RNA, and ligands. The 2024 Nobel Prize in "
            "Chemistry to Hassabis and Jumper recognized the achievement.",
            "The scientific line continued into mathematics: AlphaGeometry (2024) solved "
            "Olympiad geometry via synthetic proof generation and a symbolic verifier; "
            "AlphaProof (July 2024) paired a Gemini-based model with the Lean formal prover "
            "to achieve an IMO silver medal — the first AI at that level. The pattern is the "
            "same one from Q* reporting: generator + verifier + search = reliable "
            "capability in closed, checkable domains.",
        ], bullets=[
            "AlphaFold 2: CASP14 ~92 GDT; 200M+ structures in the AlphaFold DB.",
            "Nobel Prize in Chemistry 2024: Hassabis and Jumper.",
            "AlphaProof + Lean: IMO 2024 silver — formal verification as the reward.",
        ], insight="DeepMind's scientific program is the games program with different rewards: "
                  "structure, proofs, and molecules are just environments with verifiable "
                  "goals.",
        figures=[{"num": "4", "img": P("alphafold.jpg"), "ratio": 0.85,
                  "caption": "AlphaFold 2 performance on CASP14 — near-experimental accuracy in "
                             "protein structure prediction (figure).",
                  "source": "Creative BioStructure, 2024."}]),
        sec("5. The Agent Stack: SIMA, Mariner, and Gemini Agents", paras=[
            "The agentic turn (2023-2026) moved DeepMind's lineage from games to "
            "environments. SIMA (2023-2024) trained agents to follow language instructions "
            "in 3D game worlds with no game-specific code — a testbed for embodied language "
            "agents. Project Mariner (2024) demonstrated Gemini-powered browser agents "
            "completing real web tasks. And the Gemini agent stack (2024-2026) productized "
            "the pattern: a frontier model with tool calling, a planner, memory, and "
            "verification — the MCTS idea replaced by learned planning over API calls.",
            "The documented architectural components of the agent stack: the model "
            "(Gemini 2.0/2.5 generation), native tool use (functions as first-class "
            "tokens), a context manager (long-horizon memory), and evaluation harnesses "
            "(WebVoyager, OSWorld, and DeepMind's internal agent benchmarks). The "
            "unresolved problems are the same ones from the games era: exploration, "
            "credit assignment over long horizons, and reward specification — now with "
            "real-world stakes.",
        ], bullets=[
            "SIMA: language-conditioned agents in 3D worlds — no game-specific code.",
            "Project Mariner (2024): Gemini browser agents in production research.",
            "Agent stack = model + tools + memory + evaluation; planning is the open "
            "problem.",
        ], insight="The agent era is the games era with the environment replaced by the "
                  "internet — and the verifier replaced by the user. DeepMind's lineage "
                  "suggests the field will not rest until the verifier is learned, too.",
        figures=[{"num": "5", "img": P("deepmind_london.jpg"), "ratio": 0.8,
                  "caption": "Google DeepMind's London home at King's Cross — the laboratory "
                             "where the agent lineage runs (press photograph).",
                  "source": "Getty Images, 2023."}]),
        sec("6. AlphaEvolve and the Self-Improvement Frontier", paras=[
            "In 2025 DeepMind published AlphaEvolve, an evolution-inspired search system "
            "that improves code and algorithms through guided mutation and evaluation — "
            "used internally to optimize matrix-multiplication kernels and, reported, "
            "parts of DeepMind's own training infrastructure. The system's significance is "
            "not the individual optimizations but the demonstrated loop: an AI system "
            "generating, evaluating, and selecting improvements to AI infrastructure "
            "autonomously.",
            "The self-improvement frontier is the field's most sensitive subject. The "
            "documented precedent (AlphaDev, 2023: discovering faster sorting algorithms) "
            "and AlphaEvolve show the loop works in constrained domains with clear "
            "evaluation functions; the open question is whether the loop generalizes to "
            "unconstrained domains — the classical 'recursive self-improvement' scenario "
            "that motivates both the utopian and catastrophic readings of AGI.",
        ], bullets=[
            "AlphaEvolve (2025): evolutionary search over code; infrastructure-level "
            "optimization.",
            "AlphaDev (2023): faster sorting algorithms discovered by RL.",
            "Constrained-domain self-improvement is demonstrated; generalization is not.",
        ], insight="AlphaEvolve is the first public case of a frontier lab's AI improving its "
                  "own software stack. The loop is real; the question is its ceiling.",
        figures=[{"num": "6", "img": P("alphaproof.jpg"), "ratio": 1.0,
                  "caption": "AlphaProof and AlphaGeometry-2 at IMO 2024 — formal mathematics as "
                             "an agent domain (DeepMind figure).",
                  "source": "Google DeepMind, July 2024."}]),
        sec("7. The World-Model Question and the Road Ahead", paras=[
            "The deepest open question in the DeepMind lineage is whether agents need "
            "explicit world models. The games era answered 'yes' (MuZero plans in a "
            "learned model); the LLM era's answer is contested: Yann LeCun's "
            "'world models' agenda, DeepMind's JEPA line of research, and the Gemini "
            "generation's video-trained representations all argue that prediction is "
            "the load-bearing task; the reactive alternative (pure policy learning, as "
            "in the 'reward is enough' thesis of David Silver) argues that value "
            "optimization subsumes modeling.",
            "The roadmap DeepMind has actually published is concrete: agents that plan "
            "over learned world models, trained with self-play and real-world "
            "experience, verified in constrained domains before deployment. The "
            "frontier question is not whether agents will arrive — they are already "
            "shipping — but whether their world models will be trustworthy enough to "
            "plan in the real one.",
        ], bullets=[
            "Model-based (MuZero/JEPA) vs model-free ('reward is enough') — the live debate.",
            "Published roadmap: planning in learned world models, verified domain by "
            "domain.",
            "Agents are shipping; trust in their world models is not.",
        ], insight="DeepMind's thirty-year arc — Atari to AlphaProof to agents — is one "
                  "continuous experiment: how much intelligence can reward-optimization "
                  "buy, and what happens when the environment is the real world.",
        figures=[{"num": "7", "img": P("graphcast.jpg"), "ratio": 0.85,
                  "caption": "GraphCast weather forecast — an agent-adjacent DeepMind system "
                             "planning over a learned physical model (DeepMind figure).",
                  "source": "Google DeepMind, 2023."}]),
    ],
    references=[
        "Mnih et al., 'Human-level control through deep reinforcement learning' (DQN), Nature "
        "518, 2015. https://www.nature.com/articles/nature14236",
        "Silver et al., 'Mastering the game of Go with deep neural networks and tree search' "
        "(AlphaGo), Nature 529, 2016. https://www.nature.com/articles/nature16961",
        "Silver et al., 'Mastering the game of Go without human knowledge' (AlphaZero), Nature "
        "550, 2017. https://www.nature.com/articles/nature24270",
        "Schrittwieser et al., 'Mastering Atari, Go, chess and shogi by planning with a learned "
        "model' (MuZero), Nature 588, 2020. https://www.nature.com/articles/s41586-020-03051-4",
        "Jumper et al., 'Highly accurate protein structure prediction with AlphaFold', Nature "
        "596, 2021. https://www.nature.com/articles/s41586-021-03819-2",
        "Trinh et al., 'Solving olympiad geometry without human demonstrations', Nature 625, "
        "2024. https://www.nature.com/articles/s41586-023-06747-5",
        "DeepMind, 'AlphaProof and AlphaGeometry-2: IMO 2024 results', July 2024. "
        "https://deepmind.google/discover/blog/",
        "DeepMind, 'Project Mariner', December 2024. https://deepmind.google/discover/blog/",
        "DeepMind, 'SIMA: Scalable Instructable Multiworld Agent', 2024. "
        "https://deepmind.google/discover/blog/sima-generalist-ai-agent-for-3d-virtual-environments/",
        "Silver et al., 'Reward is Enough', Artificial Intelligence 299, 2021. "
        "https://www.sciencedirect.com/science/article/pii/S0004370221000862",
    ],
    glossary=[
        ("MCTS", "Monte Carlo Tree Search — best-first planning by simulation."),
        ("Policy network", "Network mapping states to action probabilities."),
        ("Value network", "Network estimating expected return from a state."),
        ("World model", "Learned model of environment dynamics used for planning."),
        ("Self-play", "Training by playing against copies of oneself."),
        ("Agent", "A system that perceives, decides, and acts to maximize reward."),
    ],
    timeline=[
        ("2014", "DeepMind acquired by Google; DQN published 2015."),
        ("Mar 2016", "AlphaGo defeats Lee Sedol 4-1."),
        ("2017", "AlphaZero masters Go, chess, shogi from self-play."),
        ("2020", "MuZero; AlphaFold wins CASP14."),
        ("2023", "AlphaDev; SIMA announced."),
        ("Jul 2024", "AlphaProof/AlphaGeometry-2: IMO silver; Nobel Chemistry announced."),
        ("2025-2026", "AlphaEvolve; Gemini agent stack; Mariner-style products."),
    ],
    closing="DeepMind's lineage is the strongest public evidence that reward-optimization "
            "plus search plus verification is a general route to capability. Its next "
            "decade will test whether that route extends to the unverifiable world.",
    short_title="DeepMind Agent Systems",
    keywords="DeepMind, AlphaGo, AlphaZero, MuZero, AlphaFold, AlphaProof, agents, world models",
    next_volume="Volume 09 — Embedding Spaces: Semantic Geometry",
))

# ============================================================================
# VOLUME 09 — EMBEDDING SPACES: SEMANTIC GEOMETRY
# ============================================================================
VOLUMES.append(V(
    9, "Vol_09_Embedding_Spaces_Semantic_Geometry.pdf",
    "Embedding Spaces: Semantic Geometry",
    "Word Vectors, Contextual Representations, and the Geometry of Meaning",
    "Princeton University", L("princeton.png"), [L("google.png"), L("meta.png")],
    "AI/ML — Representation Learning",
    "Every modern AI system begins by mapping symbols into vector spaces. This volume covers "
    "the geometry of meaning: word2vec's analogies, the anisotropy puzzle, contextual "
    "embeddings, the linear representation hypothesis, and the engineering of embedding "
    "systems for search, retrieval, and reasoning.",
    [
        sec("1. The Distributional Bet: Meaning as Geometry", paras=[
            "The modern embedding era began with a bet: that meaning can be represented as "
            "geometry. Word2vec (Mikolov et al., 2013) trained shallow networks to predict "
            "words from context (CBOW) or context from words (skip-gram) and found that the "
            "resulting vectors encode semantic relationships as vector arithmetic: "
            "king − man + woman ≈ queen. The result electrified the field not because it "
            "was useful (it was) but because it suggested that the structure of meaning "
            "itself — analogy, hierarchy, composition — lives in the geometry of "
            "co-occurrence statistics.",
            "The successors mapped the design space: GloVe (2014) factorized global "
            "co-occurrence statistics directly; fastText (2016) added subword information "
            "for morphology and rare words; and the 2018 contextual revolution (ELMo, "
            "BERT) replaced static vectors with representations computed per context — "
            "the same word now has many embeddings depending on its sentence, and the "
            "'meaning as geometry' claim shifted from words to contexts.",
        ], bullets=[
            "word2vec (2013): king − man + woman ≈ queen — analogy as arithmetic.",
            "GloVe: global co-occurrence factorization; fastText: subword vectors.",
            "BERT/ELMo (2018): contextual embeddings — meaning depends on context.",
        ], insight="The embedding program's deepest claim: distributional statistics contain "
                  "the structure of meaning, and geometry is its native language.",
        figures=[{"num": "1", "img": P("word2vec_pca.png"), "ratio": 0.9,
                  "caption": "2D PCA of word embeddings — semantic neighborhoods visible in "
                             "projected space (Towards Data Science).",
                  "source": "Towards Data Science, 2020."}]),
        sec("2. The Geometry: Distances, Directions, and Analogies", paras=[
            "Embedding spaces are typically 50-8192 dimensional Euclidean spaces. The "
            "working tools: cosine similarity (direction, not magnitude) as the standard "
            "semantic distance; linear directions for attributes (gender, tense, "
            "plurality — the classic 'bias direction' results of Bolukbasi et al. 2016 "
            "showed gender analogies and biases are encoded as directions); and "
            "composition — vector addition approximating conceptual combination "
            "(partly true, partly folklore, as the later literature showed).",
            "The documented puzzles: embedding spaces are anisotropic — vectors cluster in "
            "a narrow cone rather than spreading uniformly (Ethayarajh et al., 2019), "
            "which undermines naive similarity measures and motivated post-processing "
            "(all-but-the-top, whitening); and the 'linear representation hypothesis' "
            "(Park et al., 2023) — the claim that concepts and even logical relations "
            "are linear directions in LLM representations — which interpretability "
            "research has since measured directly in activation space.",
        ], bullets=[
            "Cosine similarity is the standard distance; direction encodes attributes.",
            "Anisotropy: embeddings cluster in a cone — naive similarity is misleading "
            "(2019).",
            "Linear representation hypothesis: concepts as directions (2023).",
        ], insight="The geometry of meaning is weirder than folklore: it is linear in "
                  "directions but non-uniform in distribution. Both facts matter for "
                  "every downstream system.",
        figures=[{"num": "2", "img": P("word2vec_tsne.png"), "ratio": 0.9,
                  "caption": "t-SNE projection of embeddings — clusters of related words "
                             "(Towards Data Science).",
                  "source": "Towards Data Science, 2020."}]),
        sec("3. Contextual Embeddings and the Token Problem", paras=[
            "The 2018 contextual revolution changed what gets embedded: not words but "
            "tokens-in-context. BERT's 768-dimensional contextual vectors made "
            "word-sense disambiguation a side effect (bank as river bank vs financial "
            "bank occupy different regions), and sentence embeddings (SBERT, 2019) "
            "made embedding spaces the backbone of semantic search. The engineering "
            "details that matter: pooling strategies (CLS token, mean pooling), "
            "normalization, and the now-standard practice of using the second-to-last "
            "layer rather than the final one for semantic tasks.",
            "The frontier generation embeds subword tokens (BPE) through deep "
            "transformers, and the practical consequence is that 'embedding space' is "
            "now an emergent property of the model's residual stream — which is why "
            "interpretability research reads activations, not static tables. The "
            "practical embedding products (OpenAI embeddings, Gemini embeddings, "
            "Voyage, Cohere) are all contextual models tuned for retrieval geometry.",
        ], bullets=[
            "Contextual embeddings: same word, many vectors — sense as geometry.",
            "SBERT (2019): sentence embeddings → semantic search industry.",
            "Modern embeddings are activations, not tables — emergent from the model.",
        ], insight="The token is a fiction that works: subword units with contextual "
                  "embeddings give the geometry enough resolution to encode meaning "
                  "— and enough ambiguity to make every similarity score a "
                  "probability, not a fact.",
        figures=[{"num": "3", "img": P("bpe.jpg"), "ratio": 0.85,
                  "caption": "BPE tokenization — the subword units whose embeddings populate "
                             "the space (Raschka diagram).",
                  "source": "Sebastian Raschka, 2025."}]),
        sec("4. Embeddings in Practice: RAG, Search, and Retrieval", paras=[
            "The embedding industry's center of gravity is retrieval. The canonical "
            "architecture: documents are chunked, embedded, and indexed in a vector "
            "database; queries are embedded with the same model; and nearest-neighbor "
            "search (ANN: HNSW, IVF, or disk-ANN indexes) returns candidates for "
            "re-ranking. The retrieval-augmented generation (RAG) stack — the "
            "dominant enterprise architecture of 2023-2026 — is built entirely on "
            "embedding geometry, and its quality is bounded by the quality of the "
            "embedding space: chunking strategy, embedding model, and similarity "
            "metric.",
            "The documented refinements: Matryoshka embeddings (2022) train "
            "representations whose prefixes are usable at multiple dimensions — "
            "letting systems trade cost for quality; ColBERT-style late interaction "
            "keeps per-token geometry for finer matching; and hybrid search "
            "(lexical BM25 + vector) remains the pragmatic default because "
            "embedding similarity misses exact identifiers that lexical search "
            "catches. The frontier: learned re-rankers (cross-encoders) that "
            "inspect the candidate geometry directly.",
        ], bullets=[
            "RAG stack: chunk → embed → index → retrieve → rerank → generate.",
            "ANN indexes: HNSW/IVF/disk-ANN; quality bounded by embedding geometry.",
            "Matryoshka (2022): dimension-truncatable embeddings for cost control.",
        ], insight="Retrieval is where embedding theory meets physics: the quality of "
                  "every RAG answer is decided by the geometry of a handful of "
                  "vectors — and by the chunking that produced them.",
        figures=[{"num": "4", "img": P("rag.png"), "ratio": 0.9,
                  "caption": "RAG architecture: indexing, retrieval, and generation over "
                             "vector geometry (Palo Alto Networks diagram).",
                  "source": "Palo Alto Networks Cyberpedia."}]),
        sec("5. The Linear Representation Hypothesis in LLMs", paras=[
            "The most consequential recent claim about embedding geometry is that "
            "large language models represent concepts — and logical operations — as "
            "linear directions in activation space. 'The Linear Representation "
            "Hypothesis' (Park, Choe, Veitch, 2023) formalized the claim and its "
            "testable consequences: if concepts are directions, then interventions "
            "are vector additions — subtracting a direction removes a concept "
            "(the mechanism behind representation-engineering methods like "
            "activation addition for honesty or refusal).",
            "The empirical evidence accumulated since: features in SAE dictionaries "
            "are directions (Anthropic, 2023-2024); truth appears to be "
            "represented directionally ('linear probing' of truthfulness, 2023); "
            "and representation engineering (Zou et al., 2023) demonstrated "
            "behavioral control — honesty, harmlessness, even 'love' — by adding "
            "or subtracting concept directions in models like LLaMA. The "
            "hypothesis is not settled, but it is the working assumption of the "
            "interpretability and alignment industries.",
        ], bullets=[
            "Concepts as directions: interventions as vector arithmetic.",
            "Truth probing: linear classifiers detect truthfulness in activation "
            "space.",
            "Representation engineering (2023): behavioral control via direction "
            "manipulation.",
        ], insight="If the linear representation hypothesis holds, alignment becomes "
                  "geometry: steering a model is editing vectors. The stakes are "
                  "why the field is testing it at frontier scale.",
        figures=[{"num": "5", "img": P("nn_layers.png"), "ratio": 0.9,
                  "caption": "Deep network layers — the residual stream where concept "
                             "directions live (schematic).",
                  "source": "Creately diagram library."}]),
        sec("6. Bias, Geometry, and the Ethics of Distance", paras=[
            "Embedding geometry encodes not only meaning but bias. The classic "
            "demonstrations: Bolukbasi et al. (2016) showed gender analogies "
            "(doctor − man + woman ≈ nurse) and measurable occupational bias in "
            "word2vec; later work found race and religion biases in contextual "
            "embeddings; and the 'bias direction' literature showed biases are "
            "linear and therefore removable in principle (hard debiasing, "
            "post-processing, and representation-engineering variants).",
            "The deeper ethical finding: similarity in embedding space has real "
            "consequences — hiring tools, search ranking, and content moderation "
            "all inherit the geometry, and the geometry inherits the corpus. "
            "The frontier response has been measurement (bias benchmarks), "
            "mitigation (debiasing, data curation), and transparency "
            "(embedding-model documentation). The honest state: geometry is "
            "easier to measure than to fix.",
        ], bullets=[
            "Gender/race/religion bias is linear and measurable in embedding spaces.",
            "Downstream systems inherit the geometry: hiring, search, moderation.",
            "Mitigation exists (debiasing, curation) but is partial.",
        ], insight="Embedding geometry is the quiet carrier of social values: every "
                  "downstream decision inherits the corpus's statistics. Measuring "
                  "the geometry is the first ethical duty of embedding "
                  "engineering.",
        figures=[{"num": "6", "img": P("fei_fei_li.jpg"), "ratio": 0.75,
                  "caption": "Fei-Fei Li — pioneer of human-centered AI and dataset "
                             "accountability (portrait, Yale University).",
                  "source": "Yale University, 2025."}]),
        sec("7. The Future: Geometry as Memory and Reasoning", paras=[
            "The frontier applications of embedding geometry are memory and "
            "reasoning. Memory: long-context systems and agents increasingly "
            "store experience as embeddings — retrieval over a lifetime of "
            "interactions, with the geometry doing the association work that "
            "symbolic memory did poorly. Reasoning: the 'attention over "
            "memory' architectures and the reported internal 'memory layers' "
            "of frontier models embed past computations and retrieve them by "
            "similarity — a learned, geometric form of recall.",
            "The open scientific questions: is the linear structure of "
            "meaning stable as models scale (early evidence says yes, with "
            "dimension count growing with model size)? Can geometry support "
            "compositional reasoning beyond analogies (the active "
            "'compositionality in embeddings' literature)? And can "
            "embedding-based memory scale to the exabytes of experience "
            "that agents will accumulate? The field's bet: yes, and the "
            "geometry will look familiar.",
        ], bullets=[
            "Memory as geometry: agents retrieve experience by similarity.",
            "Memory layers / attention over memory: the reported frontier "
            "architecture.",
            "Open: compositionality, stability at scale, exabyte memory.",
        ], insight="The endgame of the embedding program is a geometric "
                  "theory of cognition: memory as retrieval, reasoning as "
                  "traversal, and meaning as direction. The next decade "
                  "will test how far the analogy holds.",
        figures=[{"num": "7", "img": P("muzero.jpg"), "ratio": 0.85,
                  "caption": "Representation learning in agents — MuZero's learned state "
                             "space is an embedding geometry built for planning "
                             "(DeepMind figure).",
                  "source": "Google DeepMind, 2020."}]),
    ],
    references=[
        "Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space' "
        "(word2vec), arXiv:1301.3781, 2013. https://arxiv.org/abs/1301.3781",
        "Pennington et al., 'GloVe: Global Vectors for Word Representation', EMNLP 2014. "
        "https://nlp.stanford.edu/projects/glove/",
        "Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers for Language "
        "Understanding', arXiv:1810.04805, 2018. https://arxiv.org/abs/1810.04805",
        "Bolukbasi et al., 'Man is to Computer Programmer as Woman is to Homemaker? Debiasing "
        "Word Embeddings', NeurIPS 2016. https://arxiv.org/abs/1607.06520",
        "Ethayarajh, 'How Contextual are Contextualized Word Representations?', 2019. "
        "https://arxiv.org/abs/1909.00512",
        "Park, Choe, Veitch, 'The Linear Representation Hypothesis and the Geometry of Large "
        "Language Models', arXiv:2311.03658, 2023. https://arxiv.org/abs/2311.03658",
        "Zou et al., 'Representation Engineering: A Top-Down Approach to AI Transparency', "
        "arXiv:2310.01405, 2023. https://arxiv.org/abs/2310.01405",
        "Kusupati et al., 'Matryoshka Representation Learning', NeurIPS 2022. "
        "https://arxiv.org/abs/2205.13147",
        "Reimers & Gurevych, 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks', "
        "EMNLP 2019. https://arxiv.org/abs/1908.10084",
        "Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', "
        "arXiv:2005.11401, 2020. https://arxiv.org/abs/2005.11401",
    ],
    glossary=[
        ("Embedding", "A vector representation of a symbol, token, or context."),
        ("Cosine similarity", "Dot product of normalized vectors — the standard semantic "
         "distance."),
        ("Anisotropy", "The tendency of embeddings to cluster in a narrow cone."),
        ("Contextual embedding", "A representation computed conditionally on surrounding "
         "context."),
        ("Linear representation hypothesis", "Concepts as linear directions in activation "
         "space."),
        ("ANN index", "Approximate nearest neighbor index (HNSW, IVF) for vector search."),
    ],
    timeline=[
        ("2013", "word2vec — analogies as vector arithmetic."),
        ("2014", "GloVe; 2016 fastText and the first bias directions."),
        ("2018", "ELMo/BERT — contextual embeddings."),
        ("2019", "SBERT; anisotropy measured."),
        ("2022", "Matryoshka embeddings."),
        ("2023", "Linear representation hypothesis; representation engineering."),
        ("2026", "Embedding geometry powers RAG, agents, and memory systems at scale."),
    ],
    closing="Meaning, measured, is geometry. Every claim about what a model knows is "
            "ultimately a claim about the structure of its embedding space — learn to "
            "read the geometry and the models become legible.",
    short_title="Embedding Spaces: Semantic Geometry",
    keywords="embeddings, word2vec, word vectors, geometry, RAG, linear representation",
    next_volume="Volume 10 — Tokenizer Engineering",
))

# ============================================================================
# VOLUME 10 — TOKENIZER ENGINEERING
# ============================================================================
VOLUMES.append(V(
    10, "Vol_10_Tokenizer_Engineering.pdf",
    "Tokenizer Engineering",
    "BPE, SentencePiece, Vocabulary Design, and the Hidden Layer Every Model Depends On",
    "Massachusetts Institute of Technology", L("mit.png"),
    [L("openai.png"), L("meta.png"), L("google.png")],
    "AI/ML — Tokenization and Vocabulary Systems",
    "The tokenizer is the first and least-visible layer of every language model: it decides "
    "what a 'token' is, and therefore what the model can and cannot think. This volume covers "
    "byte-pair encoding and its variants, vocabulary engineering, the documented failure modes "
    "(number tokenization, the solidGoldMagikarp artifact, adversarial tokens), and the "
    "frontier shift toward byte- and patch-level modeling.",
    [
        sec("1. Why the Tokenizer Matters More Than It Seems", paras=[
            "Every transformer reads text as a sequence of tokens — subword units from a "
            "fixed vocabulary — and every token is a row of the embedding matrix. The "
            "tokenizer therefore determines the model's input alphabet, its vocabulary "
            "size, its effective sequence length, and its exposure to rare strings. "
            "Andrej Karpathy's widely-circulated lectures made the point bluntly: "
            "'tokenization is a root cause of many LLM quirks' — from simple arithmetic "
            "failures (numbers are split into unpredictable pieces) to spelling "
            "weaknesses and prompt-injection surfaces.",
            "The economics are equally blunt: a 100k-token vocabulary with a 768-"
            "dimensional embedding is 77M parameters of pure lookup table before the "
            "first layer computes; vocabulary choice also sets the bytes-per-token "
            "ratio (English: ~4 chars/token) that determines context-window length in "
            "human terms. Tokenizer engineering is the discipline of spending these "
            "budgets well.",
        ], bullets=[
            "Tokens are the model's alphabet: embedding table, sequence length, and "
            "quirks all start here.",
            "Karpathy's documented claim: tokenization is a root cause of LLM quirks.",
            "Vocabulary size trades parameters, context coverage, and bytes-per-token.",
        ], insight="The tokenizer is the model's theory of language — its decision about "
                  "what the atomic units of meaning are. Every other layer inherits "
                  "that decision.",
        figures=[{"num": "1", "img": P("bpe.jpg"), "ratio": 0.85,
                  "caption": "BPE merge overview — how frequent subword pairs become "
                             "vocabulary entries (Raschka diagram).",
                  "source": "Sebastian Raschka, 'BPE from Scratch', 2025."}]),
        sec("2. BPE and Its Variants: The Merge Algorithm", paras=[
            "Byte-pair encoding (BPE, Sennrich et al. 2016) builds a vocabulary "
            "greedily: start with a character (or byte) alphabet, then repeatedly "
            "merge the most frequent adjacent pair, adding it to the vocabulary "
            "until the target size is reached. The result is a vocabulary of "
            "frequent subwords and a deterministic encoding of any text. The "
            "variants differ in the base units and the objective: WordPiece "
            "(BERT, 2018) merges by likelihood gain; Unigram (SentencePiece, "
            "2018) starts from a large vocabulary and prunes by likelihood "
            "loss; and byte-level BPE (GPT-2, 2019) operates on raw bytes — "
            "the same algorithm over UTF-8 bytes rather than characters — "
            "giving universal coverage at the cost of some characters "
            "becoming multi-token.",
            "The production details that separate good tokenizers from bad "
            "ones: the training corpus mix (a tokenizer trained on code must "
            "see code), the final merge count (most frontier models now use "
            "100k-200k tokens), the treatment of whitespace and digits "
            "(digit-prefix tokens measurably improve arithmetic), and the "
            "reserved-token discipline (special tokens for chat, tools, "
            "and padding must not collide with natural text).",
        ], bullets=[
            "BPE: greedy pair-merging on bytes or characters.",
            "WordPiece/Unigram: likelihood-based variants (BERT/SentencePiece).",
            "Production details: corpus mix, digit handling, reserved tokens.",
        ], insight="BPE is a compression algorithm doing linguistics: the merge "
                  "statistics are the model's implicit theory of which letter "
                  "sequences are meaningful — including the errors in that "
                  "theory.",
        figures=[{"num": "2", "img": P("bpe2.png"), "ratio": 0.9,
                  "caption": "BPE tokenization in practice — subword splits on real text "
                             "(BuildFastWithAI diagram).",
                  "source": "BuildFastWithAI, 2026."}]),
        sec("3. The Vocabulary Zoo: cl100k, o200k, and the Open Families", paras=[
            "The frontier vocabularies are now public artifacts. OpenAI's tiktoken "
            "library documents cl100k_base (100k tokens, GPT-4 generation) and "
            "o200k_base (200k tokens, o-series), both byte-level BPE with "
            "digit-prefix tokens; LLaMA (Meta) uses SentencePiece BPE at 32k "
            "tokens; LLaMA 3 raised it to 128k; Qwen families use 150k+; and "
            "Gemini's vocabulary is undisclosed but inferred to be large. The "
            "trend is unambiguous: vocabularies are growing because more tokens "
            "mean fewer bytes per token — more context per window — at the cost "
            "of embedding-table parameters and softmax computation.",
            "The less-publicized engineering: tokenizer versions are load-bearing "
            "compatibility surfaces — a model's tokenizer must match its "
            "training distribution, and every tokenizer change requires "
            "re-embedding and re-tuning. Frontier labs treat tokenizer "
            "releases as breaking changes with migration plans.",
        ], bullets=[
            "cl100k (GPT-4) → o200k (o-series): vocabulary growth is a frontier "
            "trend.",
            "LLaMA 3: 128k SentencePiece; Qwen: 150k+; Gemini: undisclosed, "
            "inferred large.",
            "Tokenizer changes are breaking changes: compatibility is "
            "infrastructure.",
        ], insight="Vocabulary size is a strategic dial: more tokens buy context "
                  "density, but every token is a parameter row and a softmax "
                  "entry — and a new attack surface.",
        figures=[{"num": "3", "img": P("chatgpt.jpg"), "ratio": 0.8,
                  "caption": "ChatGPT — production front end of the cl100k/o200k tokenizer "
                             "generations (screenshot).",
                  "source": "The Verge, 2024."}]),
        sec("4. Documented Failure Modes: Numbers, Spelling, and Artifacts", paras=[
            "The documented failure modes make a taxonomy. Number tokenization: "
            "BPE splits numerals inconsistently (e.g., '123456' into arbitrary "
            "pieces), so arithmetic and year-comparisons fail in ways that "
            "single-digit or digit-prefix tokenizers fix — a measured, "
            "reproducible effect. Spelling: models tokenize to subwords, so "
            "character-level spelling and anagrams are systematically weak; "
            "reverse-words and 'tokenization probes' quantify the degradation. "
            "And the artifact class: solidGoldMagikarp — the famous "
            "single-token oddity from the GPT-2/3 tokenizer that appeared as a "
            "'glitch token' in unrelated outputs — demonstrated that rare "
            "vocabulary entries create unpredictable behavior, and the "
            "'glitch token' literature (2023) catalogued hundreds of them.",
            "The adversarial consequences are now a security discipline: "
            "adversarial token sequences (tokens that decode to invisible or "
            "confusable text) enable prompt injection and content-filter "
            "evasion; token-level attacks ('token smuggling') are studied in "
            "the jailbreak literature; and the defense is tokenizer hygiene — "
            "input normalization, tokenization-aware filtering, and "
            "vocabulary audits.",
        ], bullets=[
            "Numbers: BPE splits digits arbitrarily → arithmetic failures (measured).",
            "solidGoldMagikarp (2023): the canonical glitch token — rare vocabulary "
            "entries misbehave.",
            "Adversarial tokens: injection, evasion, and confusables — a security "
            "surface.",
        ], insight="Every tokenizer quirk is a small window into the model's "
                  "world-model — and a potential attack. Reading the quirks is "
                  "the cheapest interpretability available.",
        figures=[{"num": "4", "img": P("word2vec_pca.png"), "ratio": 0.9,
                  "caption": "Token embeddings in projected space — vocabulary geometry "
                             "visualized (Towards Data Science).",
                  "source": "Towards Data Science, 2020."}]),
        sec("5. Tokenizer as Security Surface", paras=[
            "The security literature converged on a sobering conclusion: the "
            "tokenizer is an attack surface that model-level defenses "
            "systematically miss. Prompt injections can be encoded in tokens "
            "that decode to invisible characters or homoglyphs; "
            "token-level jailbreaks (e.g., the 2024 'Cipher' jailbreaks) "
            "re-encode requests into token patterns the safety filters do "
            "not recognize; and the 'token smuggling' line of research "
            "shows that content policies applied at the text level can be "
            "bypassed by token-level manipulation.",
            "The defense stack that emerged: normalization (Unicode NFKC, "
            "invisible-character stripping), tokenization-aware "
            "detection (anomaly detection over token sequences), and "
            "vocabulary audits (removing or constraining dangerous "
            "entries). The frontier labs' published red-team reports "
            "(OpenAI, Anthropic, Google) all include tokenizer-level "
            "sections — a marker of how central the layer has become.",
        ], bullets=[
            "Invisible/homoglyph tokens bypass text-level filters.",
            "Cipher-style jailbreaks re-encode requests at the token level.",
            "Defenses: normalization, token anomaly detection, vocabulary audits.",
        ], insight="The tokenizer is the model's immune system boundary: attacks that "
                  "pass it bypass everything above. Securing it is a "
                  "precondition for securing the model.",
        figures=[{"num": "5", "img": P("rag2.jpg"), "ratio": 0.9,
                  "caption": "Retrieval pipelines — where untrusted text enters the "
                             "model and tokenizer attacks land (diagram).",
                  "source": "Trigma, 2026."}]),
        sec("6. Beyond Tokens: Bytes, Patches, and Continuous Inputs", paras=[
            "The frontier is questioning the token layer itself. Byte-level "
            "models (ByT5, 2021; Mamba-byte, 2024) process raw bytes at the "
            "cost of longer sequences; patch-level vision-text models "
            "(GPT-4o, Gemini, Qwen-VL) tokenize images into patches, "
            "audio into spectrogram tokens, and video into frame tokens — "
            "the 'token' is becoming a universal quantization of any "
            "modality; and continuous-input models (the flow-matching "
            "and diffusion-LLM hybrids) are experimenting with "
            "eliminating discrete tokens for generation altogether.",
            "The practical driver: multilingual and low-resource "
            "performance. Byte-level models handle any script by "
            "construction; tokenizer-heavy models degrade on languages "
            "underrepresented in the merge corpus — the documented "
            "reason Llama 3 moved to 128k tokens and why byte-fallback "
            "mechanisms are now standard in multilingual systems.",
        ], bullets=[
            "Byte-level modeling (ByT5, Mamba-byte): universal scripts, longer "
            "sequences.",
            "Universal tokens: patches for images, frames for video, "
            "spectrogram tokens for audio.",
            "Multilingual equity is a tokenizer-design issue — corpus mix "
            "decides who the model serves.",
        ], insight="The token is a quantization choice, and every quantization "
                  "choice has equity consequences: the tokenizer's training "
                  "corpus decides which languages, scripts, and dialects "
                  "the model can think in.",
        figures=[{"num": "6", "img": P("nn_cnn.jpg"), "ratio": 0.85,
                  "caption": "Layer-wise network visualization — the stack that begins at "
                             "the token embedding (schematic).",
                  "source": "Scifig.ai."}]),
        sec("7. Tokenizer Engineering as a Discipline", paras=[
            "The professional practice of tokenizer engineering now has a "
            "documented canon: corpus analysis (measuring character and "
            "byte distributions across languages), merge design (digit "
            "prefixes, whitespace handling, control tokens), evaluation "
            "(bytes-per-token, compression ratios, downstream benchmarks "
            "per language), and versioning (tokenizer migrations with "
            "backward-compatibility tests). Open tooling (Hugging Face "
            "tokenizers library, tiktoken, SentencePiece) has "
            "industrialized the layer, and the 'tokenizer bake-off' "
            "benchmarks (e.g., the 2024 multilingual tokenization "
            "studies) now guide frontier vocabulary decisions.",
            "The honest summary of the field: tokenization is the layer "
            "where linguistics, compression, security, and equity "
            "intersect — and the layer most practitioners still treat "
            "as a default. The labs that treat it as engineering "
            "measure the difference in every downstream benchmark.",
        ], bullets=[
            "Professional canon: corpus analysis, merge design, evaluation, "
            "versioning.",
            "Open tooling: HF tokenizers, tiktoken, SentencePiece — the layer "
            "is industrialized.",
            "The labs that engineer the layer measure the difference "
            "everywhere else.",
        ], insight="Tokenizer engineering is the discipline of choosing what the "
                  "model's atoms are. In an era of 200k-token vocabularies and "
                  "universal modalities, that choice is strategy.",
        figures=[{"num": "7", "img": P("huggingface.png"), "ratio": 0.8,
                  "caption": "Hugging Face — the open-source hub whose tokenizers "
                             "library standardized the layer (logo).",
                  "source": "Hugging Face brand asset."}]),
    ],
    references=[
        "Sennrich et al., 'Neural Machine Translation of Rare Words with Subword Units' (BPE), "
        "ACL 2016. https://arxiv.org/abs/1508.07909",
        "Radford et al., 'Language Models are Unsupervised Multitask Learners' (byte-level "
        "BPE), OpenAI, 2019. https://openai.com/research/better-language-models",
        "Kudo & Richardson, 'SentencePiece: A simple and language independent subword "
        "tokenizer', 2018. https://arxiv.org/abs/1808.06226",
        "Karpathy, A., 'Let's build the GPT Tokenizer' lecture notes, 2024. "
        "https://github.com/karpathy/minbpe",
        "OpenAI, 'tiktoken' — tokenizer documentation. https://github.com/openai/tiktoken",
        "Land & Bartolo, 'solidGoldMagikarp (plus, pseudogoldmagikarp): A glitch token "
        "analysis', 2023. https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/",
        "Xue et al., 'ByT5: Towards a token-free future with pre-trained byte-to-byte "
        "models', arXiv:2105.13626, 2021. https://arxiv.org/abs/2105.13626",
        "Hugging Face, 'tokenizers' library documentation. "
        "https://huggingface.co/docs/tokenizers/",
        "Wang et al., 'Mamba-byte: Token-free Selective State Space Model', 2024. "
        "https://arxiv.org/abs/2401.13660",
        "Anthropic, 'Challenges in Red Teaming AI Systems' (tokenizer-level red teaming), "
        "2023-2025. https://www.anthropic.com/research",
    ],
    glossary=[
        ("BPE", "Byte-pair encoding — greedy subword merging."),
        ("Vocabulary", "The fixed set of token types a model can emit."),
        ("Bytes-per-token", "The compression ratio of a tokenizer; decides context "
         "density."),
        ("Glitch token", "A rare vocabulary entry with anomalous model behavior."),
        ("Digit-prefix token", "Tokens encoding digit runs; measurably improves "
         "arithmetic."),
        ("NFKC", "Unicode normalization form used to neutralize confusable "
         "characters."),
    ],
    timeline=[
        ("2016", "BPE for NMT (Sennrich et al.)."),
        ("2018", "SentencePiece/Unigram; BERT's WordPiece."),
        ("2019", "GPT-2 byte-level BPE — universal coverage."),
        ("2023", "Glitch-token literature; tokenizer-as-attack-surface studies."),
        ("2024", "o200k vocabulary; Mamba-byte; tokenizer bake-offs."),
        ("2026", "Universal tokenization (text/image/audio/video) as the norm."),
    ],
    closing="The tokenizer is where language becomes arithmetic — and where the "
            "model's blind spots are born. Master the layer, and the model's "
            "quirks stop being mysteries and start being measurements.",
    short_title="Tokenizer Engineering",
    keywords="tokenizer, BPE, SentencePiece, vocabulary, glitch tokens, byte-level",
    next_volume="Volume 11 — Synthetic Data Generation",
))

VOLUMES = [v for v in VOLUMES if v["filename"]]
