#!/usr/bin/env python3
"""
Asset pipeline: converts raw web-downloaded images (image-search/) into
clean, normalized assets for the 30-volume AI research monograph series.

- Logos  -> assets/logos/*.png   (RGBA, white removed, autocropped)
- Photos -> assets/photos/*.jpg  (RGB, max width 1600, quality 85)
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "image-search")
LOGO_OUT = os.path.join(ROOT, "assets", "logos")
PHOTO_OUT = os.path.join(ROOT, "assets", "photos")
os.makedirs(LOGO_OUT, exist_ok=True)
os.makedirs(PHOTO_OUT, exist_ok=True)

# ---------------- logo mapping: target -> source file ----------------
LOGOS = {
    "harvard.png":   "yale-university-shield-svg-wikipedia-com-2.png",   # Wikimedia: Harvard University shield.svg
    "yale.png":      "yale-university-shield-svg-wikipedia-com-1.png",   # Wikimedia: Yale University Shield 1.svg
    "princeton.png": "princeton-university-official-logo-shiel-2.png",   # Wikimedia: Princeton_seal.svg
    "columbia.png":  "columbia-university-official-logo-crown-1.png",    # Columbia University official brand
    "cornell.png":   "cornell-university-official-logo-red-sea-1.png",   # Cornell University official
    "brown.png":     "coat-of-arms-of-brown-university-shield--1.png",   # Wikimedia: Brown Coat of Arms.svg
    "dartmouth.png": "dartmouth-college-official-logo-green-1.png",      # Dartmouth Big Green emblem
    "upenn.png":     "penn-university-of-pennsylvania-shield-l-2.png",   # stickpng: UPenn logo horizontal
    "mit.png":       "massachusetts-institute-of-technology-se-1.png",   # brandeps: MIT Seal
    "stanford.png":  "stanford-university-official-seal-logo-1.png",     # cdnlogo: Stanford University Seal
    "oxford.png":    "oxford-university-logo-png-transparent-v-2.png",   # seeklogo: University of Oxford
    "cambridge.png": "university-of-cambridge-coat-of-arms-svg-2.png",   # Wikimedia: Coat of Arms of the University of Cambridge
    "openai.png":    "openai-logo-black-transparent-png-2.jpg",          # freebiehive (white bg removed)
    "anthropic.png": "anthropic-logo-transparent-png-official-1.png",    # brandlogohub
    "deepmind.png":  "google-deepmind-logo-transparent-png-1.png",       # seeklogo
    "google.png":    "google-logo-transparent-png-2015-2.png",           # freebiesupply
    "microsoft.png": "microsoft-logo-transparent-png-2012-1.png",        # freebiesupply
    "nvidia.png":    "nvidia-logo-green-transparent-png-1.png",          # pngplay
    "meta.png":      "meta-logo-blue-infinity-transparent-png-2.png",    # vecteezy
    "tesla.png":     "tesla-logo-red-transparent-png-2.png",             # freepnglogos
    "ibm.png":       "ibm-logo-eight-bars-transparent-png-2.png",        # IBM design language
    "huggingface.png": "hugging-face-logo-transparent-png-2.png",        # pnghdpro
}

# ---------------- photo mapping: target -> source file ----------------
PHOTOS = {
    "sam_altman.jpg":      "sam-altman-wikimedia-commons-photo-2023-2.jpg",
    "openai_hq.jpg":       "openai-headquarters-san-francisco-office-1.png",
    "dario_amodei.jpg":    "dario-amodei-portrait-photo-anthropic-1.jpg",
    "anthropic_hq.jpg":    "anthropic-headquarters-500-howard-street-2.jpg",
    "ilya_sutskever.jpg":  "ilya-sutskever-safe-superintelligence-ph-1.jpg",
    "demis_hassabis.jpg":  "demis-hassabis-portrait-photo-1.jpg",
    "geoffrey_hinton.jpg": "geoffrey-hinton-portrait-photo-1.jpg",
    "yann_lecun.jpg":      "yann-lecun-portrait-photo-2.jpg",
    "yoshua_bengio.jpg":   "yoshua-bengio-portrait-photo-2.jpg",
    "andrej_karpathy.jpg": "andrej-karpathy-conference-speaking-phot-2.jpg",
    "fei_fei_li.jpg":      "fei-fei-li-portrait-photo-stanford-1.jpg",
    "jensen_huang.jpg":    "jensen-huang-portrait-photo-nvidia-1.jpg",
    "nick_bostrom.jpg":    "nick-bostrom-portrait-photo-2.jpg",
    "alan_turing.jpg":     "alan-turing-portrait-wikimedia-commons-2.jpg",
    "elon_musk.jpg":       "elon-musk-portrait-wikimedia-commons-1.jpg",
    "john_jumper.jpg":     "john-jumper-alphafold-nobel-portrait-2.jpg",
    "mira_murati.jpg":     "mira-murati-openai-portrait-photo-1.jpg",
    "bletchley_park.jpg":  "bletchley-park-mansion-photo-2.jpg",
    "colossus.jpg":        "colossus-computer-bletchley-park-photo-2.webp",
    "deepmind_london.jpg": "google-deepmind-london-office-building-1.jpg",
    "h100.jpg":            "nvidia-h100-gpu-chip-photo-2.jpg",
    "data_center.jpg":     "data-center-gpu-server-racks-photo-1.jpg",
    "cerebras.png":        "cerebras-wafer-scale-engine-chip-1.png",
    "alphago.jpg":         "alphago-lee-sedol-match-2016-photo-1.jpg",
    "alphafold.jpg":       "alphafold-protein-structure-prediction-i-1.jpg",
    "alphazero.jpg":       "alphazero-chess-game-board-deepmind-1.jpg",
    "stockfish.jpg":       "stockfish-chess-engine-computer-screen-1.jpg",
    "deep_blue.jpg":       "deep-blue-kasparov-chess-match-1997-phot-1.jpg",
    "chatgpt.jpg":         "chatgpt-openai-interface-screenshot-1.jpg",
    "claude.jpg":          "claude-ai-anthropic-chat-interface-1.jpg",
    "claude_code.png":     "claude-ai-anthropic-chat-interface-2.png",
    "dalle.jpg":           "dall-e-openai-generated-images-examples-1.jpg",
    "stable_diffusion.jpg":"stable-diffusion-generated-artwork-examp-1.webp",
    "gemini.jpg":          "google-gemini-app-interface-screenshot-2.webp",
    "copilot.png":         "github-copilot-ai-code-completion-editor-2.png",
    "copilot_gif.jpg":     "github-copilot-ai-code-completion-editor-1.gif",
    "waymo.jpg":           "waymo-self-driving-car-on-street-photo-2.jpg",
    "tesla_fsd.jpg":       "tesla-full-self-driving-autopilot-displa-1.jpg",
    "optimus.jpg":         "tesla-optimus-humanoid-robot-photo-1.jpg",
    "figure.jpg":          "figure-ai-humanoid-robot-photo-1.jpg",
    "eu_ai_act.jpg":       "eu-ai-act-european-parliament-voting-pho-2.jpg",
    "eu_parliament.jpg":   "eu-ai-act-european-parliament-voting-pho-1.jpg",
    "neurons.jpg":         "brain-neurons-connectome-microscopy-imag-1.webp",
    "connectome.png":      "brain-neurons-connectome-microscopy-imag-2.png",
    "fmri.jpg":            "fmri-brain-activation-map-functional-mri-1.jpg",
    "brain_scan.jpg":      "fmri-brain-scan-imaging-photo-1.jpg",
    "iter.jpg":            "iter-tokamak-interior-construction-photo-1.jpg",
    "fourcastnet.jpg":     "ai-weather-forecasting-model-map-visuali-1.jpg",
    "graphcast.jpg":       "ai-weather-forecasting-model-map-visuali-2.jpg",
    "transformer.png":     "transformer-architecture-diagram-attenti-2.png",
    "transformer_exxact.jpg": "transformer-architecture-diagram-attenti-1.jpg",
    "word2vec_pca.png":    "word2vec-word-embeddings-vector-space-vi-1.png",
    "word2vec_tsne.png":   "word2vec-word-embeddings-vector-space-vi-2.png",
    "bpe.jpg":             "bpe-byte-pair-encoding-tokenizer-example-1.webp",
    "bpe2.png":            "bpe-byte-pair-encoding-tokenizer-example-2.png",
    "gan_faces.png":       "gan-generated-human-faces-this-person-do-2.png",
    "gan_grid.jpg":        "gan-generated-human-faces-this-person-do-1.jpg",
    "rlhf.png":            "rlhf-reinforcement-learning-from-human-f-1.png",
    "rlhf2.png":           "rlhf-reinforcement-learning-from-human-f-2.png",
    "rag.png":             "retrieval-augmented-generation-rag-archi-2.jpg",
    "rag2.jpg":            "retrieval-augmented-generation-rag-archi-1.webp",
    "moe_mixtral.png":     "mixture-of-experts-neural-network-archit-2.png",
    "moe_nvidia.png":      "mixture-of-experts-neural-network-archit-1.png",
    "nn_layers.png":       "deep-neural-network-layers-diagram-visua-1.png",
    "nn_cnn.jpg":          "deep-neural-network-layers-diagram-visua-2.webp",
    "muzero.jpg":          "muzero-deepmind-board-game-algorithm-1.jpg",
    "alphaproof.jpg":      "alphaproof-alphageometry-deepmind-mathem-1.jpg",
    "superintelligence.jpg": "superintelligence-book-nick-bostrom-cove-1.jpg",
}


def autocrop(img):
    """Crop transparent borders."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def remove_white(img, threshold=238):
    """Turn near-white pixels transparent (for logos on white)."""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                px[x, y] = (r, g, b, 0)
    return img


def process_logo(src, dst):
    img = Image.open(src)
    if img.mode in ("P", "LA"):
        img = img.convert("RGBA")
    elif img.mode == "RGB":
        img = remove_white(img)
    img = autocrop(img)
    w, h = img.size
    maxh = 720
    if h > maxh:
        img = img.resize((int(w * maxh / h), maxh), Image.LANCZOS)
    pad = 12
    canvas = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(img, (pad, pad), img)
    canvas.save(dst, "PNG", optimize=True)
    return canvas.size


def process_photo(src, dst, maxw=1600, quality=85):
    img = Image.open(src)
    if img.mode == "P" and img.info.get("transparency") is not None:
        img = img.convert("RGBA")
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    img = img.convert("RGB")
    if img.width > maxw:
        img = img.resize((maxw, int(img.height * maxw / img.width)), Image.LANCZOS)
    if img.height > 1400:
        img = img.resize((int(img.width * 1400 / img.height), 1400), Image.LANCZOS)
    img.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    return img.size


def main():
    missing = []
    done = 0
    for target, src in LOGOS.items():
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            missing.append(src)
            continue
        size = process_logo(p, os.path.join(LOGO_OUT, target))
        print(f"logo  {target:20s} {size}")
        done += 1
    for target, src in PHOTOS.items():
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            missing.append(src)
            continue
        size = process_photo(p, os.path.join(PHOTO_OUT, target))
        print(f"photo {target:24s} {size}")
        done += 1
    print(f"\nProcessed {done} assets.")
    if missing:
        print("MISSING SOURCES:")
        for m in missing:
            print("  ", m)


if __name__ == "__main__":
    main()
