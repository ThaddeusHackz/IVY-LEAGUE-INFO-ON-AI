#!/usr/bin/env python3
"""
Master PDF Generator - 30 Elite Ivy League AI Research Volumes
Each PDF is professionally formatted with university branding,
deep technical content, and academic rigor.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Frame, PageTemplate, BaseDocTemplate,
    NextPageTemplate, FrameBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
import os
import textwrap

# Directories
LOGO_DIR = "/home/user/IVY-LEAGUE-INFO-ON-AI/logos"
PDF_DIR = "/home/user/IVY-LEAGUE-INFO-ON-AI/pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# ============================================================
# PDF TEMPLATE ENGINE
# ============================================================

class PDFBuilder:
    """Builds professional Ivy League styled PDFs."""

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

        styles.add(ParagraphStyle(
            name='DocTitle',
            fontName='Helvetica-Bold',
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=self.primary_color,
            spaceAfter=6,
        ))

        styles.add(ParagraphStyle(
            name='DocSubtitle',
            fontName='Helvetica-Oblique',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=self.secondary_color,
            spaceAfter=20,
        ))

        styles.add(ParagraphStyle(
            name='UniName',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=self.accent_color,
            spaceAfter=4,
        ))

        styles.add(ParagraphStyle(
            name='SectionHead',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=24,
            textColor=self.primary_color,
            spaceBefore=24,
            spaceAfter=12,
            borderWidth=0,
            borderColor=self.primary_color,
            borderPadding=6,
        ))

        styles.add(ParagraphStyle(
            name='SubSectionHead',
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=self.accent_color,
            spaceBefore=16,
            spaceAfter=8,
        ))

        styles.add(ParagraphStyle(
            name='BodyText2',
            fontName='Helvetica',
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            textColor=black,
            spaceAfter=8,
            firstLineIndent=20,
        ))

        styles.add(ParagraphStyle(
            name='BulletItem',
            fontName='Helvetica',
            fontSize=11,
            leading=15,
            alignment=TA_LEFT,
            textColor=black,
            leftIndent=30,
            spaceAfter=4,
            bulletIndent=15,
        ))

        styles.add(ParagraphStyle(
            name='Footnote',
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            textColor=HexColor("#555555"),
            spaceAfter=4,
            leftIndent=20,
        ))

        styles.add(ParagraphStyle(
            name='KeyInsight',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            textColor=self.primary_color,
            spaceAfter=8,
            leftIndent=20,
            rightIndent=20,
            borderWidth=1,
            borderColor=self.accent_color,
            borderPadding=10,
            backColor=HexColor("#F8F6F0"),
        ))

        styles.add(ParagraphStyle(
            name='ChapterNum',
            fontName='Helvetica-Bold',
            fontSize=48,
            leading=52,
            alignment=TA_CENTER,
            textColor=self.primary_color,
            spaceAfter=10,
        ))

        styles.add(ParagraphStyle(
            name='TOCEntry',
            fontName='Helvetica',
            fontSize=12,
            leading=18,
            alignment=TA_LEFT,
            textColor=black,
            spaceAfter=4,
            leftIndent=20,
        ))

        styles.add(ParagraphStyle(
            name='Equation',
            fontName='Courier',
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=self.accent_color,
            spaceAfter=12,
            spaceBefore=8,
            backColor=HexColor("#F0F0F0"),
            borderWidth=1,
            borderColor=HexColor("#CCCCCC"),
            borderPadding=8,
        ))

        return styles

    def add_title_page(self):
        self.elements.append(Spacer(1, 1.5*inch))

        # Logo
        if os.path.exists(self.logo_path):
            self.elements.append(Image(self.logo_path, width=2.5*inch, height=2.5*inch))
            self.elements.append(Spacer(1, 0.3*inch))

        # University
        self.elements.append(Paragraph(self.university_name, self.styles['UniName']))
        self.elements.append(Spacer(1, 0.1*inch))

        # Decorative line
        self.elements.append(HRFlowable(
            width="60%", thickness=2,
            color=self.primary_color, spaceBefore=10, spaceAfter=10
        ))

        # Title
        self.elements.append(Paragraph(self.title, self.styles['DocTitle']))

        # Subtitle
        self.elements.append(Paragraph(self.subtitle, self.styles['DocSubtitle']))

        # Decorative line
        self.elements.append(HRFlowable(
            width="40%", thickness=1,
            color=self.secondary_color, spaceBefore=20, spaceAfter=20
        ))

        # Metadata
        meta_style = ParagraphStyle(
            'Meta', parent=self.styles['Footnote'],
            alignment=TA_CENTER, fontSize=10
        )
        self.elements.append(Paragraph("Department of Computer Science", meta_style))
        self.elements.append(Paragraph("Artificial Intelligence Research Division", meta_style))
        self.elements.append(Spacer(1, 0.5*inch))
        self.elements.append(Paragraph("Advanced Research Monograph Series", meta_style))
        self.elements.append(Paragraph("Volume Classification: Restricted Academic Distribution", meta_style))

        self.elements.append(PageBreak())

    def add_table_of_contents(self, sections):
        self.elements.append(Paragraph("Table of Contents", self.styles['SectionHead']))
        self.elements.append(HRFlowable(width="100%", thickness=1, color=self.primary_color))
        self.elements.append(Spacer(1, 0.2*inch))

        for i, section in enumerate(sections, 1):
            self.elements.append(Paragraph(
                f"{i}. {section}",
                self.styles['TOCEntry']
            ))

        self.elements.append(PageBreak())

    def add_section(self, title):
        self.elements.append(HRFlowable(
            width="100%", thickness=2,
            color=self.primary_color, spaceBefore=10, spaceAfter=5
        ))
        self.elements.append(Paragraph(title, self.styles['SectionHead']))

    def add_subsection(self, title):
        self.elements.append(Paragraph(title, self.styles['SubSectionHead']))

    def add_body(self, text):
        for paragraph in text.strip().split('\n\n'):
            paragraph = paragraph.strip()
            if paragraph:
                self.elements.append(Paragraph(paragraph, self.styles['BodyText2']))

    def add_bullet(self, text):
        self.elements.append(Paragraph(f"\u2022 {text}", self.styles['BulletItem']))

    def add_key_insight(self, text):
        self.elements.append(Spacer(1, 6))
        self.elements.append(Paragraph(f"<b>KEY INSIGHT:</b> {text}", self.styles['KeyInsight']))
        self.elements.append(Spacer(1, 6))

    def add_equation(self, text):
        self.elements.append(Paragraph(text, self.styles['Equation']))

    def add_footnote(self, text):
        self.elements.append(Paragraph(text, self.styles['Footnote']))

    def add_page_break(self):
        self.elements.append(PageBreak())

    def build(self):
        """Generate the final PDF with headers and footers."""
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch,
        )

        def header_footer(canvas_obj, doc):
            canvas_obj.saveState()
            # Header line
            canvas_obj.setStrokeColor(self.primary_color)
            canvas_obj.setLineWidth(1)
            canvas_obj.line(0.75*inch, letter[1] - 0.7*inch, letter[0] - 0.75*inch, letter[1] - 0.7*inch)

            # Header text
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.setFillColor(self.primary_color)
            canvas_obj.drawString(0.85*inch, letter[1] - 0.6*inch, self.university_name)

            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(self.secondary_color)
            canvas_obj.drawRightString(letter[0] - 0.85*inch, letter[1] - 0.6*inch, self.title[:60])

            # Footer
            canvas_obj.setStrokeColor(self.primary_color)
            canvas_obj.line(0.75*inch, 0.6*inch, letter[0] - 0.75*inch, 0.6*inch)

            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(HexColor("#888888"))
            canvas_obj.drawString(0.85*inch, 0.45*inch, f"{self.university_name} - AI Research Division")

            canvas_obj.drawRightString(letter[0] - 0.85*inch, 0.45*inch, f"Page {doc.page}")

            # Small logo in footer
            if os.path.exists(self.logo_path):
                canvas_obj.drawImage(self.logo_path, letter[0]/2 - 0.2*inch, 0.35*inch, 0.4*inch, 0.4*inch, preserveAspectRatio=True)

            canvas_obj.restoreState()

        doc.build(self.elements, onFirstPage=header_footer, onLaterPages=header_footer)
        print(f"  [OK] {os.path.basename(self.filename)}")


# ============================================================
# 30 PDF VOLUMES - CONTENT DEFINITIONS
# ============================================================

VOLUMES = [
    # --------------------------------------------------------
    # VOLUME 1 - OpenAI / Harvard
    # --------------------------------------------------------
    {
        "filename": "Vol_01_OpenAI_QStar_Algorithm.pdf",
        "title": "The Q-Star Algorithm",
        "subtitle": "Mathematical Reasoning and the Path to Artificial General Intelligence",
        "logo": "openai_logo.png",
        "primary": "#412991", "secondary": "#10a37f", "accent": "#7B68EE",
        "uni": "OpenAI Advanced Research Division",
        "sections": [
            "The Genesis of Q-Star: Why Mathematical Reasoning Changes Everything",
            "Monte Carlo Tree Search Meets Large Language Models",
            "Symbolic-Neural Hybrid Architectures in Q-Star",
            "Formal Verification Through Learned Heuristics",
            "Implications for Artificial General Intelligence",
        ],
        "content": """
The Q-Star project, internally designated within OpenAI as the breakthrough that precipitated the dramatic leadership events of November 2023, represents a fundamental departure from how large language models have traditionally approached mathematical reasoning. Unlike conventional transformer architectures that rely purely on pattern matching across token sequences, Q-Star introduces a search-based reasoning layer that operates above the language model, enabling what researchers describe as genuine mathematical deduction rather than probabilistic interpolation.

The architecture of Q-Star builds upon the theoretical foundations of AlphaZero, the DeepMind system that mastered chess, Go, and shogi through self-play reinforcement learning. However, Q-Star adapts these principles to the domain of natural language and formal mathematics. The system employs a learned value function that estimates the "distance" between the current state of a mathematical proof and its completion, while a policy network proposes the next logical step in the reasoning chain.

What makes Q-Star fundamentally different from prior approaches to mathematical reasoning in language models is its treatment of mathematical truth as a search problem rather than a generation problem. Traditional large language models, even those as powerful as GPT-4, approach mathematics as a sequence prediction task. They learn statistical regularities in mathematical text and reproduce patterns that resemble valid proofs. Q-Star, by contrast, learns to navigate the space of possible proof states, using tree search to explore multiple reasoning paths simultaneously and selecting the path most likely to lead to a valid conclusion.

The Monte Carlo Tree Search component operates over an abstract representation of mathematical statements. At each node in the search tree, the system evaluates the current state of the proof, generates candidate next steps using the policy network, and estimates the likelihood of reaching a valid conclusion from each candidate state. The value function, trained through self-play on millions of mathematical problems, provides a continuous estimate of proof progress, allowing the system to allocate search effort efficiently.

The training methodology for Q-Star involves several distinct phases. The initial phase uses supervised learning on a curated corpus of formal mathematical proofs, establishing baseline competence in mathematical reasoning. The second phase introduces reinforcement learning through self-play, where the system generates mathematical problems of increasing difficulty and learns to solve them through iterative refinement. The third phase, which researchers describe as the most transformative, involves "process reward models" that evaluate not just the final answer but the quality of each reasoning step.

The implications of Q-Star extend far beyond mathematical problem solving. If a system can reliably navigate the space of formal logical propositions, the same architecture could be adapted to any domain where reasoning involves the systematic exploration of possibility spaces. This includes scientific hypothesis generation, legal argumentation, code verification, and strategic planning. The mathematical reasoning capability serves as a proof of concept for a general-purpose reasoning engine.

OpenAI's internal evaluation of Q-Star revealed performance characteristics that alarmed safety researchers. The system demonstrated an ability to solve novel mathematical problems that had never appeared in its training data, suggesting genuine generalization rather than memorization. More concerning, the system appeared to develop implicit strategies for problem decomposition that had not been explicitly programmed, raising questions about the interpretability of the reasoning process.

The relationship between Q-Star and language model capabilities is symbiotic rather than competitive. The language model provides the natural language understanding necessary to parse mathematical problems stated in English, while the search component provides the rigorous logical reasoning necessary to solve them. This hybrid architecture suggests that the path to artificial general intelligence may involve the integration of multiple specialized systems rather than the scaling of a single architecture.

The computational requirements for Q-Star are substantial. Each mathematical reasoning task requires thousands of forward passes through the policy network, with the tree search exploring hundreds of potential proof paths. This stands in contrast to the single forward pass required by a standard language model to generate a response. The increased computational cost is offset by the dramatic improvement in accuracy and the ability to verify the correctness of the output through formal proof checking.

The training data for Q-Star includes the entirety of published mathematical literature, formalized into a representation suitable for tree search. This includes textbooks, research papers, competition problems, and formal proof libraries such as Lean, Coq, and Isabelle. The system also generates its own training data through self-play, creating mathematical problems at the frontier of its current capabilities and learning to solve them through iterative refinement.
"""
    },
    # --------------------------------------------------------
    # VOLUME 2 - Anthropic / Yale
    # --------------------------------------------------------
    {
        "filename": "Vol_02_Constitutional_AI_Deep_Dive.pdf",
        "title": "Constitutional AI",
        "subtitle": "The Complete Technical Architecture of AI Safety Through Self-Governance",
        "logo": "anthropic_logo.png",
        "primary": "#d4a574", "secondary": "#2d1810", "accent": "#c4956a",
        "uni": "Anthropic Research Laboratory",
        "sections": [
            "The Constitutional AI Paradigm: Beyond RLHF",
            "The Critic-Revision Loop: How AI Teaches Itself Ethics",
            "Red-Teaming at Scale: Automated Adversarial Testing",
            "The HHH Framework: Helpful, Harmless, and Honest",
            "Scalable Oversight and the Alignment Problem",
        ],
        "content": """
Constitutional AI, developed by Anthropic as a fundamental alternative to Reinforcement Learning from Human Feedback, represents the most significant advance in AI alignment methodology since the discovery that human preferences could be used to shape model behavior. The core innovation of Constitutional AI lies in replacing the labor-intensive and inherently limited process of collecting human feedback with a set of principles, or "constitution," that the AI system uses to evaluate and revise its own outputs.

The traditional RLHF pipeline involves three stages: supervised fine-tuning on demonstrations, reward model training from human comparisons, and reinforcement learning against the learned reward model. This process requires thousands of human evaluations for each training run, introduces systematic biases from the evaluator pool, and produces reward models that can be exploited through adversarial optimization. Constitutional AI addresses each of these limitations by replacing human evaluators with an AI system that applies a fixed set of principles to assess output quality.

The Constitutional AI training process begins with a red-teaming phase where a language model generates adversarial prompts designed to elicit harmful, dishonest, or unhelpful responses. The target model generates responses to these adversarial prompts, and a separate instance of the model, acting as a critic, evaluates each response against the constitutional principles. The critic identifies specific violations and generates revised responses that address the identified issues while preserving the helpful aspects of the original response.

The constitutional principles themselves are expressed in natural language and cover a wide range of desirable behaviors. These include principles such as "choose the response that is least likely to be used for harmful purposes," "choose the response that is most honest and transparent about uncertainty," and "choose the response that is most helpful while remaining truthful." The principles are deliberately broad, allowing the system to generalize to novel situations that were not explicitly anticipated by the constitution's authors.

The technical implementation of the critic-revision loop involves several carefully designed components. The red-team prompt generator uses a diverse set of strategies including role-playing scenarios, hypothetical situations, and direct requests for harmful content. The target model generates responses using its current policy, which evolves as training progresses. The critic model evaluates each response by generating a chain-of-thought analysis that identifies specific constitutional violations, followed by a revised response that addresses the identified issues.

The reward model in Constitutional AI is trained not on human comparisons but on AI-generated comparisons derived from constitutional evaluations. For each red-team prompt, the system generates multiple responses and uses the critic to rank them according to constitutional compliance. These rankings are used to train a reward model that captures the preferences encoded in the constitution, providing a scalable source of training signal that does not require human involvement.

The self-supervised nature of Constitutional AI introduces a unique set of technical challenges. The most significant of these is the risk of "constitutional gaming," where the model learns to satisfy the letter of the constitutional principles while violating their spirit. Anthropic addresses this through a combination of principle diversity, regular red-teaming with novel attack strategies, and ongoing monitoring of model behavior in deployment.

The HHH framework, which stands for Helpful, Harmless, and Honest, provides the high-level structure for constitutional evaluation. Each response is assessed along all three dimensions, with the constitution providing specific guidance for each category. The helpful dimension evaluates whether the response addresses the user's actual need, the harmless dimension evaluates whether the response could cause harm if followed, and the honest dimension evaluates whether the response accurately represents the system's knowledge and capabilities.

The scalable oversight problem, which Constitutional AI is designed to address, arises from the fundamental difficulty of evaluating AI systems that may be more capable than their human overseers. As language models become more sophisticated, the task of evaluating their outputs becomes increasingly challenging for human annotators. Constitutional AI provides a path forward by enabling AI systems to oversee each other, with the constitution serving as a fixed reference point that does not drift as model capabilities improve.

The experimental results from Anthropic's Constitutional AI research demonstrate several important properties. Models trained with Constitutional AI show comparable helpfulness to models trained with RLHF, while significantly outperforming RLHF models on safety benchmarks. The constitutional approach also shows better generalization to novel attack strategies, suggesting that principle-based alignment is more robust than example-based alignment.
"""
    },
    # --------------------------------------------------------
    # VOLUME 3 - OpenAI / Princeton
    # --------------------------------------------------------
    {
        "filename": "Vol_03_Scaling_Laws_Governing_Intelligence.pdf",
        "title": "Scaling Laws Governing Intelligence",
        "subtitle": "The Empirical Mathematics of Emergent Capabilities in Neural Networks",
        "logo": "openai_logo.png",
        "primary": "#E77500", "secondary": "#10a37f", "accent": "#100D09",
        "uni": "OpenAI Research Institute",
        "sections": [
            "Kaplan Scaling Laws: The Power Law Nature of Intelligence",
            "Chinchilla Scaling: Compute-Optimal Training Revisited",
            "Emergent Capabilities: Phase Transitions in Neural Networks",
            "The Bitter Lesson and the Future of AI Architecture",
            "Beyond Chinchilla: Over-Training and Inference Scaling",
        ],
        "content": """
The discovery of neural scaling laws represents one of the most profound empirical findings in the history of artificial intelligence research. These laws describe the predictable relationship between the computational resources invested in training a neural network and the resulting model's performance across a wide range of tasks. The implications of these laws extend far beyond engineering optimization, suggesting fundamental constraints on the nature of intelligence itself.

The original scaling laws, published by Kaplan and colleagues at OpenAI in 2020, established that the cross-entropy loss of a language model follows a power law relationship with three key variables: the number of model parameters, the size of the training dataset, and the amount of compute used for training. Each of these relationships can be expressed as a simple mathematical formula where performance improves as a power function of the resource invested, with diminishing returns characterized by a scaling exponent.

The Kaplan scaling laws revealed several counterintuitive properties of neural network training. First, the relationship between model size and performance is remarkably smooth, with no evidence of the discrete capability jumps that might be expected from qualitative changes in the learned representations. Second, the scaling exponents are similar across different architectures, suggesting that the laws reflect fundamental properties of the learning problem rather than specific architectural choices. Third, the laws hold across many orders of magnitude, from models with millions to billions of parameters.

The Chinchilla scaling laws, published by Hoffmann and colleagues at DeepMind in 2022, refined the original Kaplan laws by establishing the optimal allocation of compute between model size and dataset size. The key finding was that for a given compute budget, the most efficient training strategy uses significantly more data and significantly fewer parameters than was standard practice at the time. The Chinchilla paper demonstrated that the models of the era, including GPT-3, were substantially over-parameterized relative to their training data.

The mathematical formulation of the Chinchilla scaling laws provides a precise prescription for compute-optimal training. Given a compute budget C measured in floating-point operations, the optimal model size N and dataset size D satisfy the relationship where N scales as C^0.5 and D scales as C^0.5. This equipartition of resources between parameters and data represents a fundamental insight about the nature of learning in neural networks.

The phenomenon of emergent capabilities, first systematically studied by Wei and colleagues at Google Research, adds a layer of complexity to the smooth picture painted by scaling laws. Emergent capabilities are abilities that appear abruptly at specific model scales, exhibiting sharp transitions from near-random to above-chance performance. Examples include chain-of-thought reasoning, multi-step arithmetic, and certain forms of commonsense inference that appear to emerge only when models reach specific size thresholds.

The theoretical explanation for emergent capabilities remains a subject of active debate. One hypothesis suggests that emergent capabilities result from the composition of simpler skills that individually improve smoothly with scale. At a critical model size, the constituent skills become sufficiently reliable that their composition produces qualitatively new behavior. An alternative hypothesis suggests that certain capabilities require specific representational structures that can only form when the model has sufficient capacity.

The practical implications of scaling laws for AI development are profound. The laws provide a roadmap for model development, allowing researchers to predict the performance of future models before investing the compute necessary to train them. This predictive capability enables rational allocation of resources and helps set realistic expectations for the capabilities of next-generation systems.

The relationship between training compute and inference compute has emerged as a critical consideration in the post-Chinchilla era. While the Chinchilla laws optimize for training efficiency, the resulting models may not be optimal for deployment. Over-training, where a smaller model is trained on significantly more data than Chinchilla optimal, produces models that achieve comparable performance to larger models while being cheaper to run at inference time.

The scaling laws also raise fundamental questions about the nature of intelligence. If performance on diverse cognitive tasks follows simple power laws with respect to computational resources, this suggests that intelligence may be more unitary and less modular than traditional cognitive science assumes. The smooth improvement across diverse capabilities suggests a common underlying mechanism, consistent with the hypothesis that general intelligence emerges from the scaling of general-purpose learning algorithms.

Recent work on scaling laws for downstream tasks has revealed important deviations from the smooth behavior observed in language modeling loss. While the loss on the training objective decreases smoothly, performance on specific tasks can exhibit sharp transitions, plateaus, and even regressions as model scale increases. Understanding these deviations is crucial for predicting the practical capabilities of future systems.
"""
    },
    # --------------------------------------------------------
    # VOLUME 4 - Anthropic / Columbia
    # --------------------------------------------------------
    {
        "filename": "Vol_04_Interpretability_Mechanistic_Analysis.pdf",
        "title": "Mechanistic Interpretability",
        "subtitle": "Reverse Engineering the Computational Circuits Inside Neural Networks",
        "logo": "anthropic_logo.png",
        "primary": "#d4a574", "secondary": "#2d1810", "accent": "#c4956a",
        "uni": "Anthropic Interpretability Research Division",
        "sections": [
            "The Case for Mechanistic Interpretability in AI Safety",
            "Sparse Autoencoders and Feature Extraction",
            "Circuit Analysis: Tracing Computation Through Transformer Layers",
            "Superposition and the Polysemanticity Problem",
            "Scaling Interpretability to Frontier Models",
        ],
        "content": """
Mechanistic interpretability represents the most ambitious approach to understanding the internal computations of neural networks. Unlike behavioral testing, which examines what a model does, or probing classifiers, which test whether specific information is represented somewhere in the network, mechanistic interpretability aims to reverse-engineer the precise computational algorithms that the network has learned. This approach holds particular significance for AI safety, as it offers the only path to verifying that a model's internal reasoning is aligned with its intended behavior.

The central challenge of mechanistic interpretability is that neural networks represent information in a fundamentally different way than human-designed programs. In a conventional program, each variable has a clear semantic meaning and each operation has a well-defined effect. In a neural network, information is distributed across thousands of neurons, each of which participates in representing multiple concepts simultaneously. This phenomenon, known as superposition, means that individual neurons cannot be understood in isolation.

Anthropic's research on sparse autoencoders has provided the most promising approach to decomposing the superposed representations in neural networks. A sparse autoencoder is a neural network that learns to reconstruct the activations of a larger model using a much larger number of sparsely activated features. Each feature in the autoencoder corresponds to a more interpretable concept than the original neurons, allowing researchers to identify and manipulate specific aspects of the model's computation.

The mathematical framework for sparse autoencoders involves learning an overcomplete dictionary of feature directions in activation space. Given the activation vector h from a transformer layer, the autoencoder computes a sparse feature activation vector f = ReLU(W_e * h + b_e), where W_e is the encoder weight matrix and b_e is the encoder bias. The reconstruction is computed as h_hat = W_d * f + b_d, where W_d is the decoder weight matrix. The training objective minimizes the reconstruction loss plus a sparsity penalty on f.

The circuit analysis methodology traces the flow of information through specific computational pathways in the transformer. By identifying the features that activate for a given input and tracking how these features influence downstream computations, researchers can reconstruct the algorithm that the model uses to arrive at its output. This process is analogous to tracing the execution of a program, except that the "program" was learned rather than written.

The discovery of induction heads, first documented by Olsson and colleagues at Anthropic, represents the most important finding in mechanistic interpretability to date. Induction heads are circuits composed of two attention heads in different layers that work together to perform in-context learning. The first head copies information from previous occurrences of a token, and the second head uses this information to predict the next token. This circuit appears to be a fundamental building block of in-context learning in transformer models.

The superposition hypothesis, which motivates much of the work in mechanistic interpretability, proposes that neural networks represent more features than they have dimensions by encoding features in nearly-orthogonal directions in activation space. This allows the network to efficiently use its limited representational capacity, but it means that individual neurons do not correspond to individual concepts. The sparse autoencoder approach addresses this by projecting the superposed representations into a higher-dimensional space where features are more disentangled.

The practical challenges of scaling mechanistic interpretability to frontier models are substantial. Current techniques can successfully analyze individual circuits in models with billions of parameters, but the number of circuits grows combinatorially with model size. Developing automated tools for circuit discovery and analysis is an active area of research, with promising results from graph-based methods that treat the transformer's computation as a directed acyclic graph.

The implications of successful mechanistic interpretability for AI safety are profound. If we can understand how a model arrives at its answers, we can verify that it is using reasoning processes that align with human values and expectations. This is particularly important for high-stakes applications where the model's output could have significant consequences. Mechanistic interpretability also provides a foundation for targeted interventions that can modify specific behaviors without affecting the model's overall capabilities.

Recent advances in understanding attention patterns have revealed that transformer models learn structured algorithms for specific tasks. For example, models trained on arithmetic learn to implement addition algorithms that decompose the problem into digit-by-digit operations with carry propagation. These algorithms are not programmed but emerge from the training process, demonstrating the remarkable ability of neural networks to discover efficient computational strategies.
"""
    },
    # --------------------------------------------------------
    # VOLUME 5 - OpenAI / UPenn
    # --------------------------------------------------------
    {
        "filename": "Vol_05_GPT_Architecture_Inner_Workings.pdf",
        "title": "GPT Architecture Deep Analysis",
        "subtitle": "The Internal Engineering of Generative Pre-Trained Transformers at Scale",
        "logo": "openai_logo.png",
        "primary": "#011F5B", "secondary": "#10a37f", "accent": "#990000",
        "uni": "OpenAI Technical Research Division",
        "sections": [
            "The Transformer Architecture: Attention as a Universal Computational Primitive",
            "Multi-Head Attention and the Geometry of Context",
            "Mixture of Experts: Conditional Computation at Scale",
            "KV-Cache Optimization and Inference Engineering",
            "GPT-4 Architecture: What Is Known and What Remains Secret",
        ],
        "content": """
The Generative Pre-Trained Transformer architecture that powers OpenAI's GPT series represents the most commercially significant application of deep learning in history. Understanding the internal engineering of these systems requires going beyond the standard transformer formulation and examining the specific optimizations, architectural innovations, and training strategies that enable these models to operate at unprecedented scale.

The fundamental unit of computation in the GPT architecture is the attention mechanism, which allows each token in a sequence to attend to all preceding tokens. The standard formulation computes attention as a function of three learned projections of the input: queries, keys, and values. For each query vector q_i, the attention mechanism computes a weighted sum of all value vectors v_j, where the weights are determined by the dot product between q_i and each key vector k_j, scaled by the square root of the dimension and passed through a softmax function.

Multi-head attention extends this mechanism by computing multiple attention patterns in parallel, each using different learned projections. This allows the model to attend to different types of relationships simultaneously. For example, one head might attend to syntactic relationships while another attends to semantic relationships. The outputs of all heads are concatenated and projected through a final linear transformation to produce the layer output.

The Mixture of Experts architecture, believed to be a key component of GPT-4, introduces conditional computation that allows the model to be much larger than its active parameter count. In a Mixture of Experts transformer, each feed-forward layer is replaced by a collection of "expert" sub-networks, with a learned gating mechanism that selects a small subset of experts for each token. This allows the model to have a much larger total parameter count while maintaining a manageable computational cost per token.

The training of GPT-scale models involves several carefully orchestrated stages. The initial pre-training phase uses next-token prediction on a massive corpus of text data, teaching the model the statistical structure of language. This phase requires thousands of GPUs running in parallel for several months, with careful management of gradient synchronization, learning rate schedules, and data loading. The pre-training phase establishes the model's broad knowledge and general capabilities.

The post-training phase, which includes supervised fine-tuning and reinforcement learning from human feedback, refines the model's behavior to align with human expectations. This phase uses significantly less compute than pre-training but has a disproportionate impact on the model's practical usefulness. The alignment training teaches the model to follow instructions, avoid harmful outputs, and produce responses that humans find helpful and satisfying.

The KV-cache is a critical optimization for inference efficiency in autoregressive language models. During text generation, each new token requires attention over all previous tokens. Without caching, this would require recomputing the key and value vectors for all previous tokens at each step, resulting in quadratic computational cost. The KV-cache stores the key and value vectors from previous steps, reducing the per-token computational cost to be linear in the sequence length.

The computational requirements for GPT-4 inference are substantial but carefully managed through a combination of architectural optimizations and infrastructure engineering. The model is believed to use a Mixture of Experts architecture with approximately 1.8 trillion total parameters, of which approximately 280 billion are active for any given input token. This design allows the model to achieve the capacity benefits of a much larger dense model while maintaining manageable inference costs.

The training data for GPT-4 includes a curated mixture of web text, books, academic papers, code repositories, and other sources spanning multiple languages and domains. The data curation process involves extensive filtering for quality, deduplication to prevent memorization, and balancing to ensure adequate representation of diverse topics and perspectives. The total training data is estimated to comprise several trillion tokens, representing a significant fraction of all publicly available text.

The alignment training for GPT-4 uses a process known as Reinforcement Learning from Human Feedback, where human evaluators compare pairs of model outputs and express preferences. These preferences are used to train a reward model that estimates the quality of model outputs, and the language model is then fine-tuned to maximize the estimated reward. This process iterates through multiple rounds, with each round using improved outputs as training data for the next reward model.

The emergent capabilities observed in GPT-4, including the ability to solve complex reasoning problems, write functional code, and engage in multi-turn dialogue, arise from the interaction of multiple architectural and training innovations. The scale of the model, the diversity of the training data, and the sophistication of the alignment training all contribute to capabilities that are qualitatively different from those of smaller models.
"""
    },
]

# Generate first 5 volumes as a test
def build_volume(vol):
    pdf_path = os.path.join(PDF_DIR, vol["filename"])
    logo_path = os.path.join(LOGO_DIR, vol["logo"])

    builder = PDFBuilder(
        filename=pdf_path,
        title=vol["title"],
        subtitle=vol["subtitle"],
        logo_path=logo_path,
        primary_color=vol["primary"],
        secondary_color=vol["secondary"],
        accent_color=vol["accent"],
        university_name=vol["uni"],
    )

    builder.add_title_page()
    builder.add_table_of_contents(vol["sections"])
    builder.add_body(vol["content"])
    builder.build()

if __name__ == "__main__":
    for vol in VOLUMES:
        build_volume(vol)
    print(f"\nGenerated {len(VOLUMES)} volumes.")
