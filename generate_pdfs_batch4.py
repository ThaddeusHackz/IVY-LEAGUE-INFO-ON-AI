#!/usr/bin/env python3
"""Volumes 26-30 of the Elite AI Research Series."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
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
        "filename": "Vol_26_AI_Legal_Ethics_Governance.pdf",
        "title": "AI Ethics and Governance Frameworks",
        "subtitle": "The Intersection of Law, Philosophy, and Engineering in the Age of Artificial Intelligence",
        "logo": "yale_logo.png",
        "primary": "#00356B", "secondary": "#00274C", "accent": "#FFFFFF",
        "uni": "Yale Law School and Computer Science Joint Program",
        "sections": ["The Regulatory Landscape: EU AI Act and Beyond", "Fairness, Accountability, and Transparency in AI Systems", "Intellectual Property and the Training Data Problem", "AI Liability and the Attribution of Harm", "International Governance and the Geopolitics of AI"],
        "content": """
The governance of artificial intelligence systems requires frameworks that draw on expertise from computer science, law, philosophy, economics, and political science. The rapid deployment of AI systems in high-stakes applications such as healthcare, criminal justice, employment, and financial services has created an urgent need for regulatory frameworks that can keep pace with technological development while protecting fundamental rights and promoting innovation.

The European Union's AI Act, which entered into force in 2024, represents the most comprehensive regulatory framework for artificial intelligence in the world. The Act classifies AI systems by risk level, imposing strict requirements on high-risk systems (such as those used in critical infrastructure, education, employment, and law enforcement) while imposing lighter requirements on lower-risk systems. The Act's requirements include conformity assessments, transparency obligations, human oversight requirements, and data governance standards.

The risk-based approach of the EU AI Act reflects a pragmatic recognition that not all AI applications pose the same level of risk. High-risk applications, where AI systems make or influence decisions that significantly affect people's lives, require the most stringent regulation. Limited-risk applications, such as chatbots and deepfake generators, require transparency obligations that ensure users know they are interacting with an AI system. Minimal-risk applications, such as spam filters and video game AI, are subject to minimal or no regulation.

The fairness and accountability requirements for AI systems address the well-documented tendency of machine learning models to perpetuate or amplify existing social biases. The COMPAS (Correctional Offender Management Profiling for Alternative Sanctions) case, where a recidivism prediction system was found to have significantly different false positive rates for Black and white defendants, illustrates the real-world consequences of algorithmic bias. Ensuring fairness in AI systems requires both technical solutions (such as bias-aware training algorithms) and institutional solutions (such as impact assessments and audit requirements).

The intellectual property implications of AI training data are among the most contentious legal questions in AI governance. The training of large language models on copyrighted text and images raises questions about whether this use constitutes fair use, whether rightsholders should be compensated, and whether the outputs of AI systems can themselves be copyrighted. The legal landscape is rapidly evolving, with different jurisdictions reaching different conclusions on these questions.

The attribution problem in AI-generated content asks whether the output of an AI system can be attributed to the system, its developers, or its users. This question has significant implications for liability, as the party to whom the output is attributed is typically responsible for any harm it causes. The current legal framework in most jurisdictions does not clearly address this question, creating uncertainty for both developers and users of AI systems.

AI liability frameworks must address the challenge of attributing harm to specific decisions or components in complex AI systems. Traditional product liability frameworks, which hold manufacturers responsible for defects in their products, may not be directly applicable to AI systems, where the "defect" may be an emergent property of the training data or the interaction between multiple components. The development of AI-specific liability frameworks is an active area of legal research and policy development.

The international governance of AI is complicated by the absence of a global regulatory framework and the significant differences between national approaches. The United States has taken a largely sectoral approach, with different agencies regulating AI in their respective domains. China has focused on regulating specific AI applications, such as recommendation algorithms and generative AI. The European Union has taken the most comprehensive approach with the AI Act.

The geopolitical competition in AI development, particularly between the United States and China, creates tensions between the goals of promoting innovation and ensuring safety. Export controls on advanced chips and AI technology, restrictions on cross-border data flows, and competing standards for AI governance all reflect the geopolitical dimensions of AI regulation.

The technical challenges of AI governance include the difficulty of auditing black-box models, the lack of standardized evaluation metrics for fairness and safety, and the challenge of ensuring compliance in systems that continuously learn and adapt. The development of technical standards for AI governance, including model cards, datasheets for datasets, and algorithmic impact assessments, is an important area of ongoing work.

The ethical frameworks for AI governance draw on multiple philosophical traditions, including consequentialism (which evaluates actions based on their outcomes), deontology (which evaluates actions based on their adherence to rules), and virtue ethics (which evaluates actions based on the character of the agent). Each framework provides different guidance for the design and deployment of AI systems, and the practical governance of AI typically draws on elements of all three traditions.
"""
    },
    {
        "filename": "Vol_27_AI_Scientific_Discovery.pdf",
        "title": "AI for Scientific Discovery",
        "subtitle": "How Neural Networks Are Revolutionizing Drug Discovery, Materials Science, and Fundamental Research",
        "logo": "princeton_logo.png",
        "primary": "#E77500", "secondary": "#100D09", "accent": "#000000",
        "uni": "Princeton University Institute for Advanced Study",
        "sections": ["AlphaFold and the Protein Structure Revolution", "AI-Driven Drug Discovery and Molecular Design", "Materials Science and the Inverse Design Problem", "AI in Mathematics: Conjecture and Proof", "The Future of AI-Augmented Scientific Research"],
        "content": """
The application of artificial intelligence to scientific discovery represents one of the most promising and consequential uses of AI technology. From solving the protein folding problem to discovering new materials and generating mathematical conjectures, AI systems are transforming the practice of science in ways that were unimaginable just a decade ago. Understanding the technical foundations of AI-driven science is essential for researchers across all disciplines.

AlphaFold, developed by DeepMind, solved one of the grand challenges of biology: predicting the three-dimensional structure of proteins from their amino acid sequences. The protein structure prediction problem had resisted solution for over 50 years, despite the efforts of thousands of researchers worldwide. AlphaFold's solution, which achieves accuracy comparable to experimental methods, has opened new avenues for drug design, enzyme engineering, and the understanding of disease mechanisms.

The technical architecture of AlphaFold combines several innovative components. The input representation encodes the amino acid sequence and evolutionary information from multiple sequence alignments. The Evoformer module, the core of the architecture, processes this representation through a series of attention layers that capture both sequential and spatial relationships between amino acids. The structure module converts the processed representation into three-dimensional coordinates.

The training of AlphaFold used a combination of supervised learning on experimentally determined protein structures and self-supervised learning on protein sequences. The supervised learning component provided ground truth for the structure prediction task, while the self-supervised component taught the model to understand the evolutionary relationships between proteins. The combination of these training signals produced a model with remarkable generalization to proteins not seen during training.

AI-driven drug discovery uses neural networks to predict the properties of potential drug molecules, identify promising drug targets, and design novel molecules with desired properties. The traditional drug discovery pipeline, which takes an average of 12 years and costs over 2 billion dollars, can potentially be accelerated by an order of magnitude through the use of AI techniques.

The molecular representation problem is a fundamental challenge in AI-driven drug discovery. Molecules can be represented as graphs (with atoms as nodes and bonds as edges), as three-dimensional point clouds, or as strings (using notations such as SMILES). Each representation captures different aspects of molecular structure, and the choice of representation significantly affects the model's ability to predict molecular properties.

The Graph Neural Network architecture, which operates on molecular graphs, has become the standard approach for molecular property prediction. GNNs process molecular graphs through message-passing layers that aggregate information from neighboring atoms, producing a representation that captures both local chemical environments and global molecular structure. The predictions of GNN-based models can be used to screen large libraries of potential drug molecules, identifying candidates for further investigation.

Materials science presents a different set of challenges for AI-driven discovery. The inverse design problem, which asks for a material with specific desired properties, requires models that can not only predict properties from structure but also generate structures with desired properties. Generative models, including variational autoencoders and diffusion models, have been applied to the inverse design problem with promising results.

AI in mathematics has produced several remarkable results, including the discovery of new conjectures in knot theory and the identification of patterns in combinatorial sequences. The AI mathematician, which can formulate conjectures, test them against data, and suggest proof strategies, represents a new paradigm for mathematical research that combines the creativity of human mathematicians with the computational power of AI systems.

The Lean formal proof assistant, combined with AI models trained on formal proofs, has demonstrated the ability to prove mathematical theorems automatically. The key insight is that formal proofs can be verified mechanically, providing a reliable training signal for AI models. The AI model generates candidate proof steps, and the proof assistant verifies each step, providing immediate feedback on correctness.

The integration of AI into the scientific method raises fundamental questions about the nature of scientific understanding. If an AI system can predict experimental outcomes with high accuracy but cannot explain why those outcomes occur, does this constitute scientific knowledge? The answer to this question has important implications for how we design and use AI systems in scientific research.

The reproducibility challenges in AI-driven science are significant. AI models trained on specific datasets may not generalize to new datasets, experimental conditions, or scientific domains. Ensuring that AI-driven scientific discoveries are robust and reproducible requires careful attention to experimental design, data quality, and model evaluation.

The ethical considerations in AI-driven science include the potential for AI systems to amplify existing biases in scientific research, the question of authorship and credit for AI-assisted discoveries, and the risk of over-reliance on AI predictions without adequate validation. The responsible use of AI in science requires a thoughtful approach that balances the potential benefits of AI-driven discovery with the need for rigorous scientific standards.
"""
    },
    {
        "filename": "Vol_28_AI_Energy_Climate_Modeling.pdf",
        "title": "AI for Energy and Climate",
        "subtitle": "Neural Networks for Weather Prediction, Energy Optimization, and Climate Science",
        "logo": "cornell_logo.png",
        "primary": "#B31B1B", "secondary": "#222222", "accent": "#FFFFFF",
        "uni": "Cornell University Atkinson Center for Sustainability",
        "sections": ["GraphCast and the Revolution in Weather Prediction", "AI for Renewable Energy Forecasting and Grid Optimization", "Climate Modeling and Downscaling with Neural Networks", "Carbon Capture and Emissions Monitoring", "The Energy Cost of AI and the AI of Energy Efficiency"],
        "content": """
The intersection of artificial intelligence and climate science represents one of the most impactful applications of AI technology, with the potential to improve weather prediction, optimize energy systems, and accelerate the transition to renewable energy. Understanding the technical foundations of AI-driven climate science is essential for researchers and policymakers working on the defining challenge of our era.

GraphCast, developed by DeepMind, demonstrated that a graph neural network can produce weather forecasts that are more accurate than the operational numerical weather prediction systems used by major weather agencies, while requiring a fraction of the computational resources. GraphCast generates 10-day global weather forecasts in under a minute on a single GPU, compared to the hours of supercomputer time required by traditional numerical weather prediction.

The technical architecture of GraphCast represents the atmosphere as a graph, with nodes corresponding to points on a latitude-longitude grid and edges connecting nearby points. The graph neural network processes this representation through message-passing layers that capture the physical interactions between neighboring grid points. The model is trained on 39 years of historical weather data from the European Centre for Medium-Range Weather Forecasts (ECMWF).

The key innovation of GraphCast is its use of a multi-mesh representation that captures atmospheric processes at different spatial scales. The original latitude-longitude grid is progressively coarsened to produce a hierarchy of graphs at different resolutions, allowing the model to efficiently capture both local weather phenomena and global atmospheric patterns. The multi-mesh architecture enables the model to propagate information across the globe in a small number of message-passing steps.

AI for renewable energy forecasting addresses one of the key challenges of integrating renewable energy sources into the electrical grid: the variability of solar and wind power generation. Neural network models trained on historical weather data and energy generation data can predict renewable energy output hours to days in advance, enabling grid operators to plan for fluctuations in supply and maintain grid stability.

The optimization of electrical grid operations using AI involves solving complex combinatorial optimization problems that determine how power is generated, transmitted, and distributed to meet demand. Traditional optimization methods struggle with the scale and complexity of modern electrical grids, which must balance supply and demand across thousands of generators, millions of consumers, and extensive transmission networks.

Climate modeling with neural networks offers the potential to dramatically accelerate climate simulations, which currently require months of supercomputer time for a single high-resolution simulation. Neural network emulators can learn to approximate the output of complex climate models at a fraction of the computational cost, enabling the exploration of a much wider range of climate scenarios.

The downscaling problem in climate science involves translating the coarse-resolution output of global climate models into high-resolution predictions for specific regions. Traditional downscaling methods are computationally expensive and often produce results that are inconsistent with local observations. Neural network downscaling methods learn the relationship between coarse and fine-resolution climate data from historical observations, producing high-resolution predictions that are both computationally efficient and observationally consistent.

Carbon capture and emissions monitoring using AI involves the analysis of satellite imagery and sensor data to detect and quantify greenhouse gas emissions from individual facilities and regions. Neural networks trained on satellite data can identify emission sources, estimate emission rates, and track changes in emissions over time, providing the data necessary for effective climate policy.

The energy cost of AI is itself a significant concern. The training of large language models requires enormous amounts of electricity, and the growing demand for AI computing is contributing to the overall growth in electricity consumption. Understanding and reducing the energy cost of AI is an important area of research that involves both technical innovations (such as more efficient algorithms and hardware) and policy interventions (such as carbon pricing and renewable energy requirements).

The AI of energy efficiency uses neural networks to optimize the energy consumption of buildings, transportation systems, and industrial processes. Machine learning models can learn to predict energy demand, identify opportunities for efficiency improvements, and control systems to minimize energy consumption while maintaining performance. These applications of AI can contribute significantly to reducing overall energy consumption and greenhouse gas emissions.

The integration of AI into climate policy requires careful consideration of the uncertainties in AI-driven predictions. While AI models can provide valuable insights into climate trends and energy system behavior, they are subject to the same limitations as all machine learning models, including sensitivity to training data quality, potential for distributional shift, and difficulty in quantifying uncertainty. The responsible use of AI in climate policy requires transparent communication of these limitations.
"""
    },
    {
        "filename": "Vol_29_AI_Neuroscience_Connection.pdf",
        "title": "AI and Neuroscience",
        "subtitle": "The Bidirectional Relationship Between Neural Networks and Brain Science",
        "logo": "harvard_logo.png",
        "primary": "#A51C30", "secondary": "#C9A87C", "accent": "#7B2D26",
        "uni": "Harvard University Center for Brain Science",
        "sections": ["The Deep Learning-Neuroscience Feedback Loop", "Attention Mechanisms and the Neuroscience of Selective Attention", "Predictive Coding and the Transformer Connection", "Brain-Computer Interfaces and Neural Decoding", "Consciousness, Intelligence, and the Hard Problem"],
        "content": """
The relationship between artificial intelligence and neuroscience is one of the most intellectually rich and historically significant in all of science. The development of neural networks was directly inspired by the structure of the brain, and contemporary neuroscience increasingly uses AI models as tools for understanding brain function. This bidirectional relationship continues to drive advances in both fields, with insights from neuroscience inspiring new AI architectures and AI models providing new hypotheses about brain function.

The historical connection between neural networks and neuroscience is well documented. The perceptron, the earliest neural network model, was directly inspired by the neuron doctrine in neuroscience. The backpropagation algorithm, which enables the training of deep neural networks, was inspired by theories of synaptic plasticity in the brain. The attention mechanism in transformers was motivated by the selective attention observed in human cognition.

The convolutional neural network architecture, which revolutionized computer vision, was inspired by the hierarchical organization of the visual cortex. Hubel and Wiesel's Nobel Prize-winning research on the receptive fields of neurons in the primary visual cortex demonstrated that visual processing involves a hierarchy of increasingly complex feature detectors, from simple edge detectors in the early visual areas to complex object representations in the higher areas.

The relationship between attention mechanisms in transformers and selective attention in human cognition is one of the most striking parallels between AI and neuroscience. Both systems use a mechanism that allows the processing of information to be focused on the most relevant inputs while suppressing irrelevant information. The transformer's attention weights can be compared to the attentional modulation observed in neuroimaging studies of human cognition.

The predictive coding framework in neuroscience, which proposes that the brain continuously generates predictions about incoming sensory input and processes only the errors in those predictions, has intriguing parallels with the next-token prediction objective used to train language models. Both systems learn to predict the most likely continuation of a sequence, and both develop internal representations that capture the statistical structure of their input.

The hierarchical organization of the cortex, with multiple levels of processing between sensory input and cognitive output, mirrors the layer-wise processing in deep neural networks. Both systems extract increasingly abstract representations as information flows through the hierarchy, with early layers capturing low-level features and later layers capturing high-level concepts. This parallel has inspired the use of neural network representations as models of cortical representations.

Brain-computer interfaces, which enable direct communication between the brain and external devices, use neural network decoders to interpret neural signals and translate them into commands. The decoding of neural signals is essentially a machine learning problem: given a pattern of neural activity, predict the intended action or perception. The accuracy of neural decoding has improved dramatically with the application of deep learning techniques.

The neural decoding problem is complicated by the variability of neural signals across individuals and across time. Neural networks that can generalize across different brains and different recording sessions are essential for practical brain-computer interfaces. Transfer learning techniques, which enable models trained on one individual to be adapted to another, are particularly important for reducing the calibration requirements of brain-computer interfaces.

The question of whether artificial neural networks can shed light on consciousness, the most mysterious aspect of the mind-brain relationship, is deeply controversial. Some researchers argue that sufficiently complex AI systems may develop forms of consciousness, while others argue that consciousness requires biological substrates that cannot be replicated in silicon. This debate touches on fundamental questions about the nature of mind and the relationship between physical processes and subjective experience.

The embodied cognition framework, which argues that cognition is fundamentally shaped by the body and its interactions with the environment, suggests limitations for purely computational approaches to intelligence. AI systems that lack physical bodies and direct sensory experience may develop fundamentally different forms of intelligence from biological systems, with different strengths and weaknesses. The development of robotic AI systems that can interact with the physical world is one approach to addressing this limitation.

The computational theory of mind, which proposes that the mind is essentially a computational system, provides the philosophical foundation for the AI-neuroscience connection. If the mind is a computational system, then in principle, any cognitive function can be replicated in an artificial system. The extent to which this theoretical possibility is realized in practice depends on the complexity of the underlying computational mechanisms and our ability to understand and implement them.
"""
    },
    {
        "filename": "Vol_30_AI_Future_AGI_Roadmap.pdf",
        "title": "The Road to Artificial General Intelligence",
        "subtitle": "Technical Pathways, Safety Challenges, and the Future of Intelligence on Earth",
        "logo": "openai_logo.png",
        "primary": "#412991", "secondary": "#10a37f", "accent": "#7B68EE",
        "uni": "OpenAI AGI Safety and Strategy Division",
        "sections": ["Defining AGI: Capabilities, Benchmarks, and Thresholds", "The Scaling Hypothesis: Is Bigger All We Need?", "Agentic AI and the Path to Autonomous Intelligence", "The Intelligence Explosion and Recursive Self-Improvement", "The Post-AGI World: Opportunities, Risks, and Governance"],
        "content": """
The pursuit of Artificial General Intelligence, AI systems that match or exceed human cognitive abilities across all domains, is the defining technological challenge of the 21st century. While the timeline and feasibility of AGI remain subjects of intense debate, the technical progress of recent years has made the question of AGI transition from theoretical speculation to practical engineering consideration. Understanding the technical pathways to AGI, the safety challenges that must be addressed, and the governance frameworks that will be needed is essential for anyone working at the frontier of AI research.

The definition of AGI is itself a subject of significant disagreement within the AI research community. The most common definition describes AGI as an AI system that can perform any intellectual task that a human can perform. However, this definition is ambiguous: does it mean any task that the average human can perform, or any task that any human can perform? Does it include physical tasks or only cognitive tasks? Does it require human-like consciousness or only human-like performance?

The benchmark approach to defining AGI identifies specific capabilities that are considered hallmarks of general intelligence and measures progress against these capabilities. Common benchmarks include the ability to learn new tasks from a small number of examples, the ability to transfer knowledge across domains, the ability to reason about novel situations, and the ability to engage in open-ended conversation. The ARC (Abstraction and Reasoning Corpus) benchmark, designed by Chollet, specifically tests the ability to solve novel reasoning problems that cannot be solved by memorization or pattern matching.

The scaling hypothesis, which proposes that AGI can be achieved primarily by increasing the scale of current architectures, is the most influential theory of how AGI will be achieved. The hypothesis is supported by the empirical observation that increasing model size, dataset size, and compute consistently produces new capabilities, including capabilities that were not explicitly programmed or anticipated. If this trend continues, sufficiently scaled models may achieve general intelligence.

The arguments against the scaling hypothesis point to several potential limitations. First, the diminishing returns observed in scaling laws suggest that each additional order of magnitude of scale produces smaller improvements in capability. Second, certain capabilities, such as planning, causal reasoning, and physical intuition, may require architectural innovations rather than simply more scale. Third, the training data available on the internet may be insufficient to support the training of models that are significantly larger than current systems.

Agentic AI systems, which combine language model reasoning with the ability to take actions in the environment, represent the most plausible pathway to AGI. These systems can plan multi-step strategies, use tools, learn from feedback, and adapt to new situations. The progression from passive language models to active agents represents a qualitative shift in AI capability that brings systems closer to general intelligence.

The intelligence explosion scenario, first described by I.J. Good in 1965, describes a hypothetical future event where an AI system becomes capable of improving its own intelligence, leading to a rapid and potentially uncontrollable increase in capability. The key question is whether recursive self-improvement is possible and, if so, whether it would lead to a smooth increase in capability or a rapid discontinuity.

The technical feasibility of recursive self-improvement depends on whether AI systems can effectively optimize their own architecture, training data, and training process. Current AI systems can already assist in AI research, including suggesting architectural improvements and generating training data. The question is whether this assistance can become fully autonomous and whether the resulting improvements can compound.

The alignment challenge becomes qualitatively different for AGI systems. While current alignment techniques such as RLHF are effective for systems that are less capable than their human overseers, AGI systems may be more capable than their overseers in some or all domains. The challenge of aligning a system that is more capable than its overseers is fundamentally different from aligning a system that is less capable.

The control problem, which asks how humans can maintain control over AI systems that are more intelligent than themselves, is the central challenge of AGI safety. Proposed solutions include value alignment (ensuring that the AI system shares human values), corrigibility (ensuring that the AI system allows itself to be corrected), and containment (preventing the AI system from taking actions that could cause harm). Each approach has significant theoretical and practical challenges.

The post-AGI world presents both extraordinary opportunities and existential risks. On the opportunity side, AGI could accelerate scientific discovery, solve pressing global challenges, and dramatically increase human productivity and well-being. On the risk side, AGI could be used for malicious purposes, could develop goals that are misaligned with human values, or could trigger a competitive dynamic between nations that leads to unsafe development practices.

The governance of AGI development requires international cooperation on an unprecedented scale. The development of AGI by a single nation or organization could create dangerous power imbalances, while uncoordinated development by multiple actors could lead to a race-to-the-bottom on safety. International governance frameworks must balance the need for safety with the need for innovation, and must be flexible enough to adapt to the rapid pace of AI development.

The economic implications of AGI are profound and largely unpredictable. If AGI systems can perform any cognitive task that a human can perform, the economic implications depend on the relative cost of AI and human labor, the speed at which AGI systems can be deployed, and the ability of the economy to adapt to the displacement of human labor. The potential for dramatic increases in productivity must be balanced against the potential for dramatic increases in inequality.

The philosophical implications of AGI extend beyond economics to fundamental questions about the nature of intelligence, consciousness, and the human condition. If artificial systems can match or exceed human intelligence, what does this tell us about the uniqueness of human cognition? If AGI systems can develop forms of consciousness, what moral status should they be given? These questions, once the province of philosophy, are becoming urgent practical considerations.
""",

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
    print(f"\nGenerated {len(VOLUMES)} volumes (26-30).")
