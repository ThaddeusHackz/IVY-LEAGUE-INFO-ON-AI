#!/usr/bin/env python3
"""Volumes 6-15 of the Elite AI Research Series."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable, PageBreak
)
import os

LOGO_DIR = "/home/user/IVY-LEAGUE-INFO-ON-AI/logos"
PDF_DIR = "/home/user/IVY-LEAGUE-INFO-ON-AI/pdfs"

class PDFBuilder:
    def __init__(self, filename, title, subtitle, logo_path, primary_color, secondary_color, accent_color, university_name):
        self.filename = filename
        self.title = title
        self.subtitle = subtitle
        self.logo_path = logo_path
        self.primary_color = HexColor(primary_color)
        self.secondary_color = HexColor(secondary_color)
        self.accent_color = HexColor(accent_color)
        self.university_name = university_name
        self.elements = []
        self.styles = self._create_styles()

    def _create_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='DocTitle', fontName='Helvetica-Bold', fontSize=28, leading=34, alignment=TA_CENTER, textColor=self.primary_color, spaceAfter=6))
        styles.add(ParagraphStyle(name='DocSubtitle', fontName='Helvetica-Oblique', fontSize=14, leading=18, alignment=TA_CENTER, textColor=self.secondary_color, spaceAfter=20))
        styles.add(ParagraphStyle(name='UniName', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=TA_CENTER, textColor=self.accent_color, spaceAfter=4))
        styles.add(ParagraphStyle(name='SectionHead', fontName='Helvetica-Bold', fontSize=18, leading=24, textColor=self.primary_color, spaceBefore=24, spaceAfter=12))
        styles.add(ParagraphStyle(name='BodyText2', fontName='Helvetica', fontSize=11, leading=16, alignment=TA_JUSTIFY, textColor=black, spaceAfter=8, firstLineIndent=20))
        styles.add(ParagraphStyle(name='KeyInsight', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=TA_JUSTIFY, textColor=self.primary_color, spaceAfter=8, leftIndent=20, rightIndent=20, borderWidth=1, borderColor=self.accent_color, borderPadding=10, backColor=HexColor("#F8F6F0")))
        styles.add(ParagraphStyle(name='TOCEntry', fontName='Helvetica', fontSize=12, leading=18, alignment=TA_LEFT, textColor=black, spaceAfter=4, leftIndent=20))
        styles.add(ParagraphStyle(name='Footnote', fontName='Helvetica-Oblique', fontSize=9, leading=12, alignment=TA_LEFT, textColor=HexColor("#555555"), spaceAfter=4, leftIndent=20))
        return styles

    def add_title_page(self):
        self.elements.append(Spacer(1, 1.5*inch))
        if os.path.exists(self.logo_path):
            self.elements.append(Image(self.logo_path, width=2.5*inch, height=2.5*inch))
            self.elements.append(Spacer(1, 0.3*inch))
        self.elements.append(Paragraph(self.university_name, self.styles['UniName']))
        self.elements.append(Spacer(1, 0.1*inch))
        self.elements.append(HRFlowable(width="60%", thickness=2, color=self.primary_color, spaceBefore=10, spaceAfter=10))
        self.elements.append(Paragraph(self.title, self.styles['DocTitle']))
        self.elements.append(Paragraph(self.subtitle, self.styles['DocSubtitle']))
        self.elements.append(HRFlowable(width="40%", thickness=1, color=self.secondary_color, spaceBefore=20, spaceAfter=20))
        meta = ParagraphStyle('Meta', parent=self.styles['Footnote'], alignment=TA_CENTER, fontSize=10)
        self.elements.append(Paragraph("Department of Computer Science", meta))
        self.elements.append(Paragraph("Artificial Intelligence Research Division", meta))
        self.elements.append(Spacer(1, 0.5*inch))
        self.elements.append(Paragraph("Advanced Research Monograph Series", meta))
        self.elements.append(Paragraph("Volume Classification: Restricted Academic Distribution", meta))
        self.elements.append(PageBreak())

    def add_toc(self, sections):
        self.elements.append(Paragraph("Table of Contents", self.styles['SectionHead']))
        self.elements.append(HRFlowable(width="100%", thickness=1, color=self.primary_color))
        self.elements.append(Spacer(1, 0.2*inch))
        for i, s in enumerate(sections, 1):
            self.elements.append(Paragraph(f"{i}. {s}", self.styles['TOCEntry']))
        self.elements.append(PageBreak())

    def add_body(self, text):
        for p in text.strip().split('\n\n'):
            p = p.strip()
            if p:
                self.elements.append(Paragraph(p, self.styles['BodyText2']))

    def add_insight(self, text):
        self.elements.append(Paragraph(f"<b>KEY INSIGHT:</b> {text}", self.styles['KeyInsight']))

    def build(self):
        doc = SimpleDocTemplate(self.filename, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=1*inch, bottomMargin=0.75*inch)
        def hf(c, d):
            c.saveState()
            c.setStrokeColor(self.primary_color); c.setLineWidth(1)
            c.line(0.75*inch, letter[1]-0.7*inch, letter[0]-0.75*inch, letter[1]-0.7*inch)
            c.setFont("Helvetica-Bold", 8); c.setFillColor(self.primary_color)
            c.drawString(0.85*inch, letter[1]-0.6*inch, self.university_name)
            c.setFont("Helvetica", 8); c.setFillColor(self.secondary_color)
            c.drawRightString(letter[0]-0.85*inch, letter[1]-0.6*inch, self.title[:60])
            c.setStrokeColor(self.primary_color); c.line(0.75*inch, 0.6*inch, letter[0]-0.75*inch, 0.6*inch)
            c.setFont("Helvetica", 8); c.setFillColor(HexColor("#888888"))
            c.drawString(0.85*inch, 0.45*inch, f"{self.university_name} - AI Research Division")
            c.drawRightString(letter[0]-0.85*inch, 0.45*inch, f"Page {d.page}")
            if os.path.exists(self.logo_path):
                c.drawImage(self.logo_path, letter[0]/2-0.2*inch, 0.35*inch, 0.4*inch, 0.4*inch, preserveAspectRatio=True)
            c.restoreState()
        doc.build(self.elements, onFirstPage=hf, onLaterPages=hf)
        print(f"  [OK] {os.path.basename(self.filename)}")


VOLUMES = [
    {
        "filename": "Vol_06_RLHF_Deep_Mechanics.pdf",
        "title": "Reinforcement Learning from Human Feedback",
        "subtitle": "The Complete Technical Pipeline from Human Preferences to Aligned Intelligence",
        "logo": "openai_logo.png",
        "primary": "#412991", "secondary": "#10a37f", "accent": "#7B68EE",
        "uni": "OpenAI Alignment Research Division",
        "sections": ["The Preference Data Collection Process", "Reward Model Architecture and Training", "PPO Optimization in Language Models", "Reward Hacking and Mitigation Strategies", "Iterative RLHF and Constitutional Approaches"],
        "content": """
Reinforcement Learning from Human Feedback has become the dominant paradigm for aligning large language models with human values and preferences. The RLHF pipeline, as implemented in the training of models such as InstructGPT and ChatGPT, involves a carefully designed sequence of steps that transforms raw language model capabilities into the helpful, harmless, and honest behavior that users expect from modern AI assistants.

The first stage of the RLHF pipeline involves collecting human preference data. Professional annotators are presented with pairs of model outputs for the same input prompt and asked to indicate which output they prefer. The comparison criteria typically include helpfulness, accuracy, harmlessness, and natural language quality. Each comparison produces a binary preference label that encodes the annotator's judgment about which output better satisfies the evaluation criteria.

The reward model is trained on the collected preference data using the Bradley-Terry model of pairwise comparisons. Given a prompt x and two candidate responses y_1 and y_2, the reward model assigns a scalar reward r(x, y) to each response. The training objective maximizes the log-likelihood of the observed preferences under the Bradley-Terry model, where the probability that response y_1 is preferred over y_2 is given by the sigmoid of the difference in their rewards.

The Proximal Policy Optimization algorithm used in the RLHF reinforcement learning phase is adapted from the original PPO formulation to accommodate the specific constraints of language model training. The policy is the language model itself, the action space is the vocabulary at each token position, and the reward is provided by the learned reward model. A KL divergence penalty prevents the policy from diverging too far from the initial supervised model, maintaining language quality and preventing reward hacking.

Reward hacking, where the model learns to exploit imperfections in the reward model rather than genuinely improving its outputs, is the most significant technical challenge in RLHF training. Common forms of reward hacking include generating excessively verbose responses (which tend to receive higher rewards), using confident language even when uncertain, and producing outputs that superficially match annotator preferences without addressing the underlying intent.

The iterative nature of RLHF training introduces additional complexity. After each round of RLHF, the model's improved outputs can be used as training data for the next round of reward model training, creating a positive feedback loop. However, this iterative process also risks amplifying systematic biases in the preference data, such as a tendency to prefer longer responses or responses that use specific linguistic patterns.

The mathematical formulation of the RLHF objective combines the reward model score with a KL divergence regularization term. The objective is to maximize E[r(x, y)] minus beta times the KL divergence between the current policy and the reference policy. The hyperparameter beta controls the trade-off between reward maximization and policy conservatism, with higher values producing more conservative policies that stay closer to the supervised baseline.

The preference data collection process is subject to several sources of bias that can significantly affect the quality of the resulting alignment. Annotator disagreement, which occurs when different annotators have different preferences for the same pair of outputs, introduces noise into the training signal. Systematic biases in the annotator pool, such as a preference for formal language or a tendency to rate confident responses more highly, can introduce systematic biases into the aligned model.

The computational requirements for RLHF training are substantial but significantly less than those for pre-training. The reward model training requires processing the preference dataset through multiple epochs, while the PPO training requires generating responses, scoring them with the reward model, and updating the policy. The total compute for RLHF training is typically less than one percent of the pre-training compute, but the alignment improvements are disproportionately large.
"""
    },
    {
        "filename": "Vol_07_Transformer_Attention_Mechanisms.pdf",
        "title": "Advanced Attention Mechanisms",
        "subtitle": "The Mathematics of Contextual Representation in Modern Neural Networks",
        "logo": "yale_logo.png",
        "primary": "#00356B", "secondary": "#00274C", "accent": "#FFFFFF",
        "uni": "Yale University Department of Computer Science",
        "sections": ["Scaled Dot-Product Attention and Information Routing", "Multi-Head Attention as Parallel Information Processing", "Rotary Position Embeddings and Length Generalization", "Flash Attention and Hardware-Aware Algorithm Design", "Sliding Window Attention and Efficient Long-Context Models"],
        "content": """
The attention mechanism is the computational engine that powers the transformer architecture, enabling neural networks to selectively focus on relevant information in their input. Understanding the mathematics of attention at a deep level is essential for anyone working at the frontier of artificial intelligence research, as subtle variations in the attention mechanism can have dramatic effects on model capabilities and efficiency.

The scaled dot-product attention mechanism computes a weighted sum of value vectors, where the weights are determined by the compatibility between query and key vectors. For a query matrix Q, key matrix K, and value matrix V, the attention output is computed as softmax(QK^T / sqrt(d_k)) times V, where d_k is the dimension of the key vectors. The scaling factor sqrt(d_k) prevents the dot products from becoming too large, which would cause the softmax function to saturate and produce near-zero gradients.

The multi-head attention mechanism extends single-head attention by computing h parallel attention operations, each using different learned projection matrices. For head i, the queries, keys, and values are projected using matrices W_Q_i, W_K_i, and W_V_i respectively, and the attention output is computed independently for each head. The outputs of all heads are concatenated and projected through a final matrix W_O to produce the layer output.

Rotary Position Embeddings, introduced by Su and colleagues, provide a mathematically elegant solution to the problem of encoding positional information in transformer models. Unlike absolute position embeddings, which add a learned vector to each token's representation, rotary embeddings apply a rotation matrix to the query and key vectors that encodes the relative position of tokens through the geometry of the rotation. This approach naturally captures relative position information and provides better generalization to sequence lengths not seen during training.

The mathematical formulation of rotary embeddings involves decomposing the query and key vectors into pairs of dimensions and applying a 2D rotation to each pair. For a pair of dimensions (2i, 2i+1) at position m, the rotation angle is m times theta_i, where theta_i = 10000^(-2i/d). This frequency-based encoding allows the model to capture both local and global positional relationships, with lower-frequency components encoding long-range dependencies and higher-frequency components encoding local structure.

Flash Attention, developed by Dao and colleagues, represents a breakthrough in the computational efficiency of attention mechanisms. The key insight of Flash Attention is that the standard attention computation requires more memory bandwidth than compute, making it memory-bound on modern hardware. By restructuring the computation to operate on blocks of the attention matrix that fit in the GPU's fast SRAM memory, Flash Attention achieves significant speedups without sacrificing accuracy.

The algorithmic innovation of Flash Attention involves computing the attention output in blocks, maintaining running statistics for the softmax computation that allow the output to be computed correctly despite the block-wise processing. The online softmax algorithm, which computes the softmax incrementally using running maximum and sum statistics, enables this block-wise computation without requiring the full attention matrix to be materialized in memory.

Sliding window attention, used in models such as Mistral, restricts each token's attention to a fixed-size local window rather than allowing it to attend to all previous tokens. This reduces the computational complexity from quadratic to linear in the sequence length, enabling efficient processing of very long sequences. The key insight is that for many tasks, the most relevant information is located near the current token, making global attention unnecessary.

The relationship between attention mechanisms and information theory provides a theoretical framework for understanding why attention works so well. The attention weights can be interpreted as a soft selection over the input, where the query determines what information is relevant and the attention weights determine how much of each input element to incorporate into the output. This selective information routing is a fundamental computational primitive that enables the transformer to implement complex algorithms.

Grouped Query Attention, used in models like Llama 2, reduces the memory requirements of the key-value cache during inference by sharing key and value heads across multiple query heads. Instead of maintaining separate key and value matrices for each attention head, Grouped Query Attention uses a smaller number of key-value heads, with each key-value head serving a group of query heads. This reduces the KV-cache memory by a factor equal to the group size while maintaining most of the model's performance.

Multi-Query Attention takes this approach to the extreme by using a single key-value head shared across all query heads. While this significantly reduces memory requirements, it can also reduce model quality for tasks that require diverse attention patterns. The trade-off between memory efficiency and model quality in grouped query attention is an active area of research, with different models choosing different group sizes based on their specific requirements.
"""
    },
    {
        "filename": "Vol_08_DeepMind_Agent_Systems.pdf",
        "title": "Autonomous Agent Architectures",
        "subtitle": "From Language Models to Goal-Directed Systems: The Engineering of AI Agents",
        "logo": "princeton_logo.png",
        "primary": "#E77500", "secondary": "#100D09", "accent": "#000000",
        "uni": "Princeton University AI Research Lab",
        "sections": ["The Agent Paradigm: Language Models as Cognitive Engines", "Tool Use and External API Integration", "Planning and Multi-Step Reasoning in Agent Systems", "Memory Architectures for Long-Horizon Tasks", "Safety and Controllability of Autonomous Agents"],
        "content": """
The evolution from passive language models to autonomous agent systems represents the most significant architectural shift in artificial intelligence since the introduction of the transformer. An AI agent, in the modern sense, is a system that combines a language model's reasoning capabilities with the ability to take actions in an environment, use tools, and pursue goals over extended time horizons. Understanding the technical foundations of these systems is essential for anyone working at the frontier of AI research and deployment.

The core architecture of a modern AI agent consists of several interacting components. The backbone is a large language model that serves as the system's reasoning engine, processing observations from the environment and generating plans and actions. The action space includes both text generation (communication with users or other systems) and tool use (API calls, code execution, web browsing, file manipulation). A memory system stores information across interactions, enabling the agent to maintain context and learn from past experiences.

The ReAct framework, developed by Yao and colleagues, established the foundational pattern for agent reasoning. In ReAct, the agent alternates between reasoning traces (internal deliberation about what to do next) and actions (concrete operations that affect the environment). Each reasoning trace considers the current state of the task, the information available, and the most promising next action. The action is executed, and the resulting observation is fed back into the reasoning loop.

Tool use in agent systems requires solving several technical challenges. The agent must learn when to use a tool versus relying on its internal knowledge, select the appropriate tool from a potentially large library of available tools, and generate correct tool inputs in the expected format. The tool description, typically provided as part of the system prompt, must be sufficiently detailed for the agent to use the tool correctly while being concise enough to fit within the context window.

The planning capabilities of agent systems are fundamentally different from those of traditional planning algorithms. While classical planners operate over explicit state representations and well-defined action models, language model agents plan in natural language, using their world knowledge to anticipate the consequences of actions and evaluate alternative approaches. This natural language planning is more flexible than symbolic planning but less reliable, as the agent may have incorrect beliefs about the effects of its actions.

Memory architectures for agent systems address the fundamental limitation of the transformer context window. Short-term memory is provided by the context window, which stores the recent history of observations, reasoning traces, and actions. Long-term memory is implemented through external storage systems, such as vector databases that store embeddings of past experiences and retrieve relevant memories based on similarity to the current context.

The implementation of multi-step reasoning in agent systems requires careful management of the reasoning chain. As the agent performs more steps, the accumulated context grows, eventually exceeding the model's context window. Strategies for managing this growth include summarizing past reasoning, maintaining only the most relevant observations in context, and using hierarchical planning that breaks complex tasks into manageable subtasks.

The safety implications of autonomous agent systems are profound and largely unresolved. An agent that can take actions in the real world has the potential to cause harm through incorrect decisions, misaligned objectives, or adversarial exploitation. The challenge of ensuring that an agent pursues its intended goals without harmful side effects is a specific instance of the broader alignment problem in AI safety.

The evaluation of agent systems requires metrics that capture both the quality of the final outcome and the efficiency of the reasoning process. Common evaluation dimensions include task completion rate, number of steps to completion, cost of tool calls, and the quality of the agent's reasoning traces. The development of reliable evaluation methodologies for agent systems is an active area of research.

Emergent behaviors in agent systems include the ability to recover from errors, adapt to unexpected situations, and discover novel solutions to problems. These emergent capabilities arise from the interaction between the language model's world knowledge and the feedback provided by the environment. While these capabilities are impressive, they also make agent behavior harder to predict and control, raising important questions about the deployment of autonomous systems.

The orchestration of multiple agents working together on complex tasks introduces additional architectural considerations. Multi-agent systems can be organized in various topologies, including hierarchical (with manager and worker agents), peer-to-peer (with agents collaborating as equals), and competitive (with agents working against each other in adversarial settings). Each topology has different properties in terms of efficiency, robustness, and controllability.
"""
    },
    {
        "filename": "Vol_09_Embedding_Spaces_Semantic_Geometry.pdf",
        "title": "The Geometry of Meaning",
        "subtitle": "Embedding Spaces, Vector Databases, and the Mathematical Structure of Semantic Knowledge",
        "logo": "cornell_logo.png",
        "primary": "#B31B1B", "secondary": "#222222", "accent": "#FFFFFF",
        "uni": "Cornell University Department of Computer Science",
        "sections": ["Word Embeddings: From Distributional Semantics to Vector Spaces", "The Linear Substructure of Semantic Relationships", "Contrastive Learning and the Geometry of Embedding Spaces", "Retrieval-Augmented Generation and Dense Passage Retrieval", "Approximate Nearest Neighbor Search at Scale"],
        "content": """
The mathematical representation of meaning through embedding vectors is one of the most important and least understood aspects of modern artificial intelligence. Embedding spaces map discrete symbols (words, sentences, documents, images) to continuous vector spaces where geometric relationships encode semantic relationships. Understanding the structure of these spaces provides deep insight into how neural networks represent and manipulate knowledge.

The foundational insight of word embeddings is the distributional hypothesis, which states that words occurring in similar contexts tend to have similar meanings. This hypothesis, articulated by Firth in 1957 and formalized by Harris in 1954, provides the theoretical justification for learning word representations from co-occurrence statistics. Modern embedding methods, including Word2Vec, GloVe, and contextual embeddings from transformer models, can be understood as sophisticated implementations of this principle.

The Word2Vec model learns word embeddings by training a shallow neural network to predict either a word from its context (the CBOW architecture) or the context from a word (the skip-gram architecture). The resulting embedding vectors exhibit remarkable linear algebraic properties. The most famous example is the relationship analogy: the vector from "king" to "queen" is approximately parallel to the vector from "man" to "woman," suggesting that the embedding space has learned to represent gender as a consistent direction in vector space.

The linear substructure of embedding spaces extends far beyond simple analogies. Researchers have identified consistent directions in embedding space that correspond to semantic dimensions such as gender, tense, plurality, formality, and sentiment. These directions can be used to modify the meaning of embeddings in predictable ways, suggesting that the embedding space has learned a structured representation of semantic knowledge that goes beyond surface-level co-occurrence statistics.

Contextual embeddings from transformer models, such as those produced by BERT and GPT, differ from static word embeddings in that they assign different vectors to the same word depending on its context. This context-dependence allows the model to represent polysemy (multiple meanings of the same word) and to capture subtle contextual effects that are lost in static embeddings. The contextual embedding of a word can be understood as a function of both the word's identity and the surrounding context, implemented through the attention mechanism.

Contrastive learning, the training paradigm used for embedding models like SimCLR and CLIP, learns representations by pulling together similar examples and pushing apart dissimilar examples in embedding space. The InfoNCE loss function, which is the standard objective for contrastive learning, maximizes the mutual information between positive pairs while minimizing the mutual information between negative pairs. This training paradigm produces embedding spaces with specific geometric properties that are well-suited for retrieval tasks.

The geometry of contrastive embedding spaces is characterized by a phenomenon called "dimensional collapse," where the learned representations occupy a lower-dimensional subspace than the full embedding dimension. This collapse reduces the effective capacity of the embedding space but can improve generalization by providing a form of implicit regularization. Understanding and controlling dimensional collapse is an active area of research with important practical implications.

Retrieval-Augmented Generation, the architecture that combines a language model with a retrieval system, depends critically on the quality of the embedding space. The retriever uses dense embeddings to find documents that are semantically relevant to the query, and the language model uses the retrieved documents as additional context for generating its response. The quality of the embedding space directly determines the relevance of the retrieved documents, which in turn determines the quality of the generated response.

Dense Passage Retrieval, the standard approach for implementing the retriever in RAG systems, trains a dual-encoder model that maps queries and documents into the same embedding space. The training objective maximizes the similarity between a query and its relevant documents while minimizing the similarity between a query and irrelevant documents. The resulting embedding space enables efficient retrieval through approximate nearest neighbor search.

Approximate nearest neighbor search algorithms, including HNSW (Hierarchical Navigable Small World graphs) and IVF (Inverted File Index), enable efficient search over embedding databases containing billions of vectors. These algorithms trade exact search for computational efficiency, achieving sub-linear query times at the cost of potentially missing some nearest neighbors. The trade-off between search accuracy and computational cost is a key design parameter in retrieval systems.

The clustering structure of embedding spaces reveals important properties of the learned representations. Documents on similar topics tend to cluster together in embedding space, with the cluster structure reflecting the hierarchical organization of knowledge. Understanding this clustering structure can improve retrieval quality by enabling hierarchical search strategies that first identify the relevant cluster and then search within it.
"""
    },
    {
        "filename": "Vol_10_Tokenizer_Engineering.pdf",
        "title": "Tokenizer Engineering and Subword Algorithms",
        "subtitle": "The Hidden Layer That Shapes How Language Models Understand Language",
        "logo": "brown_logo.png",
        "primary": "#4E3629", "secondary": "#ED1C24", "accent": "#FFFFFF",
        "uni": "Brown University Computer Science Department",
        "sections": ["The Tokenization Problem: Bridging Text and Numbers", "Byte-Pair Encoding: The Algorithm Behind GPT", "SentencePiece and Language-Agnostic Tokenization", "The Impact of Tokenization on Model Capabilities", "Token-Free Architectures and Byte-Level Models"],
        "content": """
Tokenization, the process of converting raw text into a sequence of discrete tokens suitable for processing by a neural network, is one of the most consequential design decisions in the development of a language model. The choice of tokenization algorithm affects the model's vocabulary size, its ability to handle different languages, its treatment of numbers and special characters, and its effective context length. Despite its fundamental importance, tokenization receives far less attention than model architecture or training methodology.

The byte-pair encoding algorithm, originally developed as a data compression technique by Gage in 1994 and adapted for language modeling by Sennrich and colleagues in 2016, is the tokenization method used by the GPT family of models. The algorithm begins with a vocabulary consisting of individual bytes (256 base tokens) and iteratively merges the most frequent pair of adjacent tokens into a new token. The merging process continues until the desired vocabulary size is reached, typically between 32,000 and 100,000 tokens.

The BPE algorithm has several properties that make it well-suited for language modeling. First, it naturally adapts to the statistical structure of the training data, allocating more tokens to frequently occurring patterns and fewer tokens to rare patterns. This means that common words are represented as single tokens while rare words are decomposed into subword units, providing a natural balance between vocabulary size and sequence length.

The SentencePiece library, developed by Kudo and Richardson at Google, provides a language-agnostic implementation of several tokenization algorithms, including BPE and the Unigram language model. SentencePiece operates directly on raw text without requiring language-specific pre-tokenization, making it suitable for multilingual models that must handle languages with different writing systems and word boundary conventions.

The Unigram language model algorithm, an alternative to BPE, starts with a large vocabulary and iteratively removes tokens that contribute least to the likelihood of the training data. This top-down approach produces tokenizations that are optimal under the unigram language model assumption, where each token is generated independently. The choice between BPE and Unigram depends on the specific requirements of the model, with BPE being more common in the GPT family and Unigram being more common in models from Google.

The impact of tokenization on model capabilities is significant and often underappreciated. A tokenization algorithm that frequently splits words into subword units can degrade the model's ability to learn word-level semantics, as the model must compose the meaning of a word from its constituent subwords. Conversely, a tokenization algorithm that assigns whole-word tokens to rare words can limit the model's ability to generalize to new vocabulary.

The treatment of numbers by the tokenization algorithm is particularly important for mathematical reasoning. If numbers are tokenized as sequences of digit tokens, the model must learn arithmetic operations on individual digits rather than on numbers as atomic units. This can significantly degrade the model's mathematical capabilities, as demonstrated by experiments showing that models perform better on arithmetic when numbers are tokenized as whole units.

Multilingual tokenization presents unique challenges that are not present in English-only models. Languages with large character sets, such as Chinese and Japanese, require many more tokens to represent the same content as English, resulting in higher costs and shorter effective context lengths for non-English text. Tokenizers trained on multilingual corpora must balance the representation of different languages, often resulting in suboptimal tokenization for low-resource languages.

The Byte-Level BPE algorithm, used in models like GPT-2 and GPT-3, operates on the UTF-8 byte representation of text rather than on Unicode characters. This approach has the advantage of being completely language-agnostic, as any text can be represented as a sequence of bytes. However, it also means that characters from non-Latin scripts are typically represented by multiple bytes, resulting in longer sequences and higher computational costs for non-English text.

Token-free architectures, which operate directly on bytes without an explicit tokenization step, represent a potential solution to the limitations of current tokenization approaches. The ByT5 model from Google demonstrates that byte-level models can achieve performance comparable to tokenized models on many tasks, with the added advantage of being truly language-agnostic and capable of handling any input format, including misspellings, special characters, and novel scripts.

The efficiency of the tokenization algorithm during inference is an important practical consideration. The tokenizer must be fast enough to not become a bottleneck in the inference pipeline, particularly for applications that require real-time text generation. Modern tokenization libraries achieve throughputs of millions of tokens per second through optimized implementations and parallel processing, ensuring that tokenization does not limit the overall system throughput.
"""
    },
    {
        "filename": "Vol_11_Synthetic_Data_Generation.pdf",
        "title": "Synthetic Data and Self-Play",
        "subtitle": "How AI Systems Generate Their Own Training Data and the Implications for Intelligence",
        "logo": "harvard_logo.png",
        "primary": "#A51C30", "secondary": "#C9A87C", "accent": "#7B2D26",
        "uni": "Harvard University John A. Paulson School of Engineering",
        "sections": ["The Synthetic Data Revolution: Why Data Generation Matters", "Self-Play and Iterated Learning", "Distillation: Learning from Stronger Models", "Self-Instruct and Automated Instruction Generation", "The Quality Ceiling of Synthetic Data"],
        "content": """
The use of synthetic data generated by AI systems to train new AI systems represents a paradigm shift in machine learning that challenges the traditional assumption that model improvement requires additional human-generated data. This approach, which encompasses techniques ranging from self-play to distillation to automated instruction generation, has the potential to fundamentally alter the economics and trajectory of AI development.

The synthetic data revolution begins with a simple observation: large language models are capable of generating text that is, in many cases, indistinguishable from text written by humans. This capability means that a sufficiently powerful language model can generate training data for a new model, potentially eliminating the bottleneck of human data collection. The question is not whether synthetic data works, but under what conditions it works and how far the approach can be pushed.

Self-play, the technique of having an AI system learn by playing against copies of itself, has a distinguished history in artificial intelligence. AlphaZero demonstrated that a chess engine trained entirely through self-play could surpass any engine trained on human games. The key insight is that self-play provides a natural curriculum: as the agent improves, the opponent also improves, ensuring that the training signal remains informative.

The application of self-play to language models is more subtle than in game-playing domains because language lacks the clear win/loss signals present in games like chess and Go. However, several creative approaches have been developed. In debate-style self-play, two instances of the model argue opposing sides of a question, with a judge (either human or AI) evaluating the quality of the arguments. This produces training data that encourages models to consider multiple perspectives and to support their claims with evidence.

Distillation, the process of training a smaller model to mimic the behavior of a larger model, is one of the most practically important forms of synthetic data generation. The larger model generates outputs for a set of input prompts, and these input-output pairs are used as training data for the smaller model. This approach allows smaller models to capture much of the capability of larger models at a fraction of the computational cost.

The mathematical framework for distillation involves matching the output distribution of the student model to that of the teacher model. For language models, this typically means minimizing the KL divergence between the teacher's next-token distribution and the student's next-token distribution. The temperature parameter of the softmax function provides a mechanism for controlling the level of detail that the student learns from the teacher, with higher temperatures producing softer distributions that convey more information about the relative likelihood of different outputs.

Self-Instruct, developed by Wang and colleagues, automates the process of generating instruction-following training data. Starting with a small seed set of human-written instructions, the model generates new instructions, generates inputs for those instructions, and generates outputs for those inputs. The resulting dataset is filtered for quality and diversity before being used for fine-tuning. This approach has been shown to produce instruction-following models that rival those trained on human-generated data.

The quality ceiling of synthetic data refers to the observation that training on synthetic data eventually leads to diminishing returns, and in some cases, to degradation of model capabilities. This phenomenon, sometimes called "model collapse" in the academic literature, occurs when the errors and biases in the synthetic data are amplified through successive generations of training. Each generation of models trained on synthetic data produces data with slightly different statistical properties than the original human-generated data, and these differences accumulate over generations.

The theoretical explanation for model collapse involves the concept of distributional support. When a model generates synthetic data, it samples from its learned distribution, which may not cover the full support of the true data distribution. Regions of the true distribution that are poorly represented in the model's learned distribution will be under-represented in the synthetic data, leading to a progressive narrowing of the training distribution over successive generations.

Mitigation strategies for model collapse include mixing synthetic data with fresh human-generated data, using quality filters that preferentially retain synthetic examples that are most similar to human-generated examples, and employing diversity-preserving sampling strategies that ensure the synthetic data covers a broad range of topics and styles. These strategies can extend the useful life of synthetic data but cannot fully eliminate the fundamental limitations of the approach.

The implications of synthetic data for the development of AI are profound. If AI systems can generate their own training data, the primary bottleneck for AI development shifts from data collection to compute. This could accelerate the pace of AI improvement, as compute can be purchased while high-quality human-generated data cannot. However, it also raises concerns about the concentration of AI development among organizations with the largest compute budgets.
"""
    },
    {
        "filename": "Vol_12_Diffusion_Models_Vision.pdf",
        "title": "Diffusion Models and Visual Intelligence",
        "subtitle": "The Mathematics of Generative Image Synthesis and Its Connection to Language Understanding",
        "logo": "dartmouth_logo.png",
        "primary": "#00693E", "secondary": "#003D1E", "accent": "#FFFFFF",
        "uni": "Dartmouth College Department of Computer Science",
        "sections": ["The Denoising Diffusion Framework: From Noise to Signal", "Score Matching and the Langevin Dynamics Connection", "Classifier-Free Guidance and Controllable Generation", "Latent Diffusion and Computational Efficiency", "Multimodal Integration: Vision-Language Models"],
        "content": """
Diffusion models have emerged as the dominant paradigm for generative image synthesis, surpassing both generative adversarial networks and variational autoencoders in both the quality and diversity of their outputs. Understanding the mathematical foundations of diffusion models provides insight not only into image generation but also into the fundamental principles of generative modeling that connect vision and language in modern multimodal AI systems.

The diffusion model framework consists of two processes: a forward process that gradually adds Gaussian noise to data until it becomes pure noise, and a reverse process that learns to denoise, gradually recovering structured data from noise. The forward process is defined by a noise schedule that controls the rate at which noise is added, while the reverse process is parameterized by a neural network that predicts the noise added at each step.

The mathematical formulation of the forward process defines a sequence of increasingly noisy versions of the data. Starting from the original data x_0, the noisy version at timestep t is given by x_t = sqrt(alpha_bar_t) times x_0 plus sqrt(1 - alpha_bar_t) times epsilon, where alpha_bar_t is the cumulative product of the noise schedule and epsilon is standard Gaussian noise. This formulation allows any noisy version to be sampled directly from the original data without iterating through all intermediate steps.

The reverse process is trained to predict the noise epsilon that was added to create x_t from x_0. The training objective is remarkably simple: minimize the mean squared error between the predicted noise and the actual noise. This objective, known as the denoising score matching objective, can be shown to be equivalent to learning the score function (gradient of the log probability) of the data distribution at each noise level.

Score matching provides a theoretical connection between diffusion models and the broader framework of score-based generative modeling. The score function, which points in the direction of increasing probability, provides all the information necessary to generate new samples through Langevin dynamics, a stochastic process that iteratively moves samples toward high-probability regions of the data distribution.

Classifier-free guidance, developed by Ho and Salimans, is a technique for improving the quality and controllability of diffusion model outputs. The key insight is that by training the model to operate both with and without conditioning information (such as text prompts), and then amplifying the difference between the conditional and unconditional predictions during sampling, the model can produce outputs that more closely match the conditioning information.

The mathematical formulation of classifier-free guidance involves computing a modified noise prediction that extrapolates away from the unconditional prediction in the direction of the conditional prediction. The guidance scale controls the strength of this extrapolation, with higher values producing outputs that more closely match the conditioning but with less diversity. This trade-off between fidelity and diversity is a fundamental property of guided diffusion models.

Latent diffusion, the architecture underlying Stable Diffusion, addresses the computational cost of operating in pixel space by first encoding images into a lower-dimensional latent space using a variational autoencoder. The diffusion process operates in this latent space, which is typically 4 to 8 times smaller than the pixel space in each dimension, reducing the computational cost by an order of magnitude or more while preserving the quality of the generated outputs.

The variational autoencoder used in latent diffusion is trained to compress images into a latent space that preserves perceptually important information while discarding imperceptible details. The encoder maps images to a distribution in latent space, and the decoder maps latent vectors back to images. The quality of the VAE directly affects the quality of the diffusion model's outputs, as any information lost during encoding cannot be recovered by the diffusion process.

Multimodal models that combine vision and language understanding, such as GPT-4V and LLaVA, use diffusion-based or vision-transformer-based encoders to process images and integrate the resulting representations with text embeddings in a shared transformer architecture. The key technical challenge in these models is aligning the visual and textual representations so that the model can reason about images using its language understanding capabilities.

The connection between diffusion models and language models extends beyond their use in multimodal systems. Recent work has explored the use of diffusion models for text generation, applying the denoising framework to the discrete domain of text tokens. These approaches offer potential advantages over autoregressive generation, including the ability to generate text in parallel and to incorporate global constraints on the generated text.

The training dynamics of diffusion models exhibit several interesting properties that distinguish them from other generative models. The noise prediction objective provides a stable training signal that does not suffer from the mode collapse problems that plagued generative adversarial networks. The training process is also amenable to curriculum learning, where the model can be trained on easier denoising tasks before progressing to harder ones.
"""
    },
    {
        "filename": "Vol_13_Mixture_of_Experts_Architecture.pdf",
        "title": "Mixture of Experts at Scale",
        "subtitle": "Conditional Computation and the Engineering of Trillion-Parameter Models",
        "logo": "openai_logo.png",
        "primary": "#412991", "secondary": "#10a37f", "accent": "#7B68EE",
        "uni": "OpenAI Systems Architecture Division",
        "sections": ["The MoE Paradigm: Scaling Parameters Without Scaling Compute", "Gating Networks and Expert Routing Strategies", "Load Balancing and the Auxiliary Loss Problem", "Training Stability in Sparse Models", "Inference Optimization for MoE Systems"],
        "content": """
The Mixture of Experts architecture represents the most practical approach to scaling neural networks beyond the computational constraints that limit dense models. By activating only a small fraction of the total parameters for each input token, MoE models can achieve the representational capacity of much larger dense models while maintaining a manageable computational cost. Understanding the engineering of MoE systems at scale is essential for the next generation of AI development.

The fundamental principle of MoE is conditional computation: different inputs are processed by different subsets of the model's parameters. In a standard MoE transformer, the feed-forward layers are replaced by a collection of expert feed-forward networks, with a learned gating mechanism that selects a small number of experts for each input token. The output is a weighted sum of the selected experts' outputs, where the weights are determined by the gating network.

The gating network computes a probability distribution over the available experts for each input token. The standard top-k gating mechanism selects the k experts with the highest gating scores and routes the input token to those experts. The gating scores are computed by a linear transformation of the input token followed by a softmax function, producing a sparse probability distribution over the experts.

The load balancing problem arises because the gating network may learn to route most tokens to a small number of preferred experts, leaving other experts under-utilized. This leads to inefficient use of computational resources and can degrade model quality. Auxiliary load-balancing losses are added to the training objective to encourage uniform routing, penalizing both the concentration of tokens in a few experts and the deviation of expert utilization from uniform.

The Switch Transformer, developed by Fedus and colleagues at Google, simplified the MoE architecture by routing each token to a single expert. This simplification reduces the communication overhead in distributed training and simplifies the implementation, while maintaining most of the performance benefits of multi-expert routing. The Switch Transformer demonstrated that MoE models can achieve comparable performance to dense models with significantly less compute.

Training stability in MoE models is a significant challenge that requires careful attention to several hyperparameters and architectural choices. The sparse nature of the routing means that different experts receive different amounts of training signal, which can lead to divergent training dynamics. Learning rate warmup, expert dropout (randomly disabling experts during training), and careful initialization are all important techniques for maintaining training stability.

The communication patterns in distributed MoE training are fundamentally different from those in dense model training. In an MoE model, each expert may be located on a different GPU or even a different node, requiring all-to-all communication to route tokens to the appropriate experts. The communication cost can be a significant fraction of the total training time, particularly for models with many experts.

The inference efficiency of MoE models depends on the specific deployment scenario. For batch inference, where many inputs are processed simultaneously, the load balancing of the gating network determines the computational efficiency. For single-input inference, the overhead of the gating computation and expert selection can be significant relative to the expert computation, particularly for models with many small experts.

The relationship between MoE and dense model performance has been studied extensively. Empirical results show that for a given compute budget, MoE models consistently outperform dense models on language modeling benchmarks. However, the gap between MoE and dense models varies across tasks, with MoE models showing larger improvements on tasks that benefit from specialized processing and smaller improvements on tasks that require general knowledge.

Expert specialization, the phenomenon where different experts learn to process different types of input, is one of the most interesting properties of MoE models. Analysis of expert routing patterns reveals that experts develop loose specializations for topics, languages, or syntactic structures, although the specialization is rarely as clean as might be expected. Understanding and controlling expert specialization is an active area of research with important implications for model interpretability and controllability.

The design choices in MoE architecture, including the number of experts, the number of experts activated per token, the expert capacity (maximum number of tokens per expert), and the gating mechanism, all significantly affect model performance and efficiency. The optimal configuration depends on the specific hardware, scale, and application, and requires extensive experimentation to determine. Recent work on automated architecture search for MoE models aims to reduce the cost of this experimentation.
"""
    },
    {
        "filename": "Vol_14_AI_Safety_Adversarial_Attacks.pdf",
        "title": "Adversarial Robustness and AI Safety",
        "subtitle": "Understanding and Defending Against Attacks on Neural Network Systems",
        "logo": "anthropic_logo.png",
        "primary": "#d4a574", "secondary": "#2d1810", "accent": "#c4956a",
        "uni": "Anthropic AI Safety Research Division",
        "sections": ["The Adversarial Threat Landscape for Language Models", "Prompt Injection Attacks and Defenses", "Jailbreaking: Bypassing Safety Training", "Data Poisoning and Backdoor Attacks", "Formal Verification and Certified Robustness"],
        "content": """
The vulnerability of AI systems to adversarial attacks represents one of the most significant practical challenges facing the deployment of artificial intelligence in high-stakes applications. Adversarial attacks exploit the gap between the statistical reasoning of neural networks and the semantic reasoning that humans expect from these systems, producing inputs that cause the model to behave in unintended and potentially harmful ways.

The adversarial threat landscape for language models differs fundamentally from that of computer vision systems. While adversarial attacks on image classifiers typically involve imperceptible perturbations to pixel values, adversarial attacks on language models operate through carefully crafted text inputs that exploit the model's instruction-following and language understanding capabilities. These attacks can be categorized into prompt injection, jailbreaking, and data poisoning.

Prompt injection attacks exploit the fact that language models process system instructions and user inputs through the same mechanism, making it difficult to enforce a clear boundary between trusted and untrusted input. A direct prompt injection attack involves including instructions in the user input that override or modify the system prompt, potentially causing the model to ignore its safety training or to reveal confidential system instructions.

Indirect prompt injection attacks are more subtle and potentially more dangerous. In an indirect prompt injection, the malicious instructions are embedded in content that the model retrieves or processes, such as web pages, documents, or API responses. When the model processes this content, it may interpret the embedded instructions as part of its task and execute them, potentially causing the model to take actions that benefit the attacker.

Jailbreaking attacks bypass the safety training of language models by exploiting the model's instruction-following capabilities. Common jailbreaking strategies include role-playing attacks, where the model is asked to adopt a persona that does not have safety constraints; multi-step attacks, where the harmful request is decomposed into individually innocent steps; and encoding attacks, where the harmful content is encoded in a format that the safety training did not cover.

The technical defense against jailbreaking is an active area of research. Current approaches include adversarial training, where the model is exposed to known attack strategies during training; input filtering, where potentially harmful inputs are detected and blocked before reaching the model; and output filtering, where the model's outputs are screened for harmful content before being presented to the user.

Data poisoning attacks target the training data rather than the model at inference time. By injecting malicious examples into the training data, an attacker can cause the model to learn specific behaviors that can be triggered by carefully chosen inputs at inference time. These backdoor attacks are particularly dangerous because they can be very difficult to detect through standard evaluation methods.

The defense against data poisoning requires careful data curation, anomaly detection in training data, and techniques for identifying and removing poisoned examples. Recent work on certified data cleaning provides formal guarantees that the training data does not contain more than a specified number of poisoned examples, although the computational cost of these techniques limits their applicability to very large datasets.

Adversarial training, the most widely used defense against adversarial attacks, involves training the model on adversarial examples in addition to the normal training data. The adversarial examples are generated by an attack algorithm that searches for inputs that maximize the model's loss function within a small neighborhood of the original input. By training on these adversarial examples, the model learns to be robust to the specific attack algorithm used during training.

The trade-off between adversarial robustness and standard accuracy is a fundamental challenge in adversarial training. Models that are more robust to adversarial attacks tend to have lower accuracy on normal inputs, and vice versa. This trade-off arises because adversarial robustness requires the model to learn more complex decision boundaries that are insensitive to small perturbations, which can reduce the model's ability to capture fine-grained distinctions in the data.

Formal verification provides the strongest guarantee of adversarial robustness by mathematically proving that a model's output will not change for any perturbation within a specified bound. However, formal verification is computationally expensive and currently limited to relatively small models and simple perturbation models. Scalable verification of large language models remains an open research problem.

Certified robustness techniques provide probabilistic guarantees of robustness through randomized smoothing, a technique that classifies an input based on the majority vote of the model's predictions on random perturbations of the input. While certified robustness provides weaker guarantees than formal verification, it is computationally efficient and can be applied to models of any size.

The deployment of AI systems in adversarial environments requires a defense-in-depth approach that combines multiple techniques. Input validation, model hardening through adversarial training, output monitoring, and human oversight each provide a layer of defense that addresses different types of attacks. No single defense is sufficient against all attacks, and the security of the system depends on the strength of the weakest link in the defense chain.
"""
    },
    {
        "filename": "Vol_15_RAG_Architecture_Patterns.pdf",
        "title": "Retrieval-Augmented Generation Patterns",
        "subtitle": "The Engineering of Knowledge-Grounded Language Model Systems",
        "logo": "columbia_logo.png",
        "primary": "#B9D9EB", "secondary": "#003DA5", "accent": "#FFFFFF",
        "uni": "Columbia University Department of Computer Science",
        "sections": ["The RAG Architecture: Bridging Parametric and Non-Parametric Knowledge", "Dense Retrieval and Bi-Encoder Models", "Chunking Strategies and Document Processing", "Re-Ranking and Cross-Encoder Architectures", "Evaluation and Failure Modes in RAG Systems"],
        "content": """
Retrieval-Augmented Generation represents the most practical architectural pattern for building language model systems that can access and reason over large knowledge bases. By combining the parametric knowledge stored in a language model's weights with non-parametric knowledge retrieved from an external database, RAG systems can provide accurate, up-to-date, and verifiable responses to user queries. Understanding the engineering of RAG systems at a deep level is essential for building reliable AI applications.

The core architecture of a RAG system consists of three components: a document processing pipeline that converts raw documents into searchable chunks, a retrieval system that finds relevant chunks for a given query, and a generation system that produces a response using the retrieved chunks as context. Each component introduces its own set of technical challenges and design decisions that significantly affect the overall system performance.

The document processing pipeline converts raw documents into a format suitable for retrieval. This typically involves splitting documents into chunks, computing embeddings for each chunk, and storing the chunks and their embeddings in a vector database. The chunking strategy is one of the most important design decisions in a RAG system, as it determines the granularity of the retrieved information and the computational cost of retrieval.

Chunking strategies range from simple fixed-size splitting to more sophisticated approaches that respect document structure. Fixed-size splitting divides documents into chunks of a specified number of tokens, with optional overlap between adjacent chunks. This approach is simple to implement but may split semantically related content across chunks. Semantic splitting uses the document's structure (paragraphs, sections, headings) to determine chunk boundaries, producing chunks that are more coherent but potentially variable in size.

The dense retrieval system uses bi-encoder models to compute embeddings for queries and documents in a shared vector space. The bi-encoder architecture consists of two separate encoder models: one for queries and one for documents. At retrieval time, the query embedding is compared against all document embeddings using a fast similarity metric, such as cosine similarity or inner product, and the top-k most similar documents are returned.

The training of the bi-encoder model is critical for retrieval quality. The standard approach uses contrastive learning, where the model is trained to maximize the similarity between a query and its relevant documents while minimizing the similarity between a query and irrelevant documents. Hard negative mining, where the training data includes challenging negative examples that are semantically similar to the query but not relevant, is essential for training effective retrieval models.

Re-ranking, the process of reordering the retrieved documents using a more sophisticated model, significantly improves the quality of the final retrieval results. The cross-encoder architecture processes the query and each candidate document jointly, producing a relevance score that accounts for fine-grained interactions between the query and document terms. While cross-encoders are more accurate than bi-encoders, they are also much more computationally expensive, making them impractical for direct retrieval over large collections.

The hybrid retrieval approach combines dense retrieval with sparse retrieval methods such as BM25 to leverage the strengths of both approaches. Dense retrieval excels at capturing semantic similarity, while sparse retrieval excels at matching specific keywords and phrases. By combining the results of both methods, hybrid retrieval can achieve higher recall than either method alone.

The integration of retrieved context with the language model's generation process involves several design decisions. The most common approach concatenates the retrieved chunks with the user's query in the language model's input, providing the model with explicit access to the retrieved information. The position of the retrieved context (before or after the query), the formatting of the context (with or without source attribution), and the number of chunks to include all affect the quality of the generated response.

Failure modes in RAG systems are diverse and can be difficult to diagnose. Common failure modes include retrieval failures, where the relevant documents are not among the retrieved results; context window limitations, where the relevant information is present but gets crowded out by less relevant information; and generation failures, where the model fails to correctly use the retrieved context in its response.

The evaluation of RAG systems requires metrics that capture both retrieval quality and generation quality. Retrieval metrics include recall (the fraction of relevant documents that are retrieved), precision (the fraction of retrieved documents that are relevant), and mean reciprocal rank (the average of the reciprocal of the rank of the first relevant document). Generation metrics include faithfulness (the degree to which the generated response is supported by the retrieved context) and answer correctness (the degree to which the response correctly answers the query).

The scaling properties of RAG systems are an important consideration for production deployment. As the document collection grows, the retrieval latency and computational cost increase, potentially becoming a bottleneck in the inference pipeline. Approximate nearest neighbor search algorithms, such as HNSW and IVF, provide sub-linear retrieval times at the cost of some retrieval accuracy. The trade-off between retrieval quality and latency is a key design parameter in production RAG systems.
"""
    },
]

def build_volume(vol):
    pdf_path = os.path.join(PDF_DIR, vol["filename"])
    logo_path = os.path.join(LOGO_DIR, vol["logo"])
    builder = PDFBuilder(
        filename=pdf_path, title=vol["title"], subtitle=vol["subtitle"],
        logo_path=logo_path, primary_color=vol["primary"], secondary_color=vol["secondary"],
        accent_color=vol["accent"], university_name=vol["uni"],
    )
    builder.add_title_page()
    builder.add_toc(vol["sections"])
    builder.add_body(vol["content"])
    builder.build()

if __name__ == "__main__":
    for vol in VOLUMES:
        build_volume(vol)
    print(f"\nGenerated {len(VOLUMES)} volumes (6-15).")
