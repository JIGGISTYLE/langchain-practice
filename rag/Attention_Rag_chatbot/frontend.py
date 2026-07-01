"""
Attention Is All You Need — an interactive study companion.

Built from the original NIPS 2017 paper (Vaswani et al.). Figures and
tables shown throughout are cropped directly from the uploaded PDF.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

def frontend():
    ASSETS_DIR = "assets"
    # ----------------------------------------------------------------------------
    # Design tokens & global styles
    # ----------------------------------------------------------------------------
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        :root{
            --ink:#161A23;
            --muted:#5B6472;
            --paper:#EEF0F3;
            --surface:#FFFFFF;
            --border:#DBE0E6;
            --accent:#E0552B;
            --accent-soft:#FBE7DF;
            --accent-violet:#8A7CC4;
            --accent-violet-soft:#EFEBF8;
            --accent-sage:#6E9572;
            --accent-sage-soft:#E9F1EA;
            --radius:14px;
        }

        html, body, .stApp { background: var(--paper); }
        .stApp, .stMarkdown, p, li, span, label, div { font-family: 'Inter', -apple-system, sans-serif; }
        h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; color: var(--ink); letter-spacing:-0.01em; }
        code, .mono { font-family: 'IBM Plex Mono', monospace !important; }

        .block-container{ padding-top:1.6rem; padding-bottom:4rem; max-width:1180px; }
        a { color: var(--accent); }

        section[data-testid="stSidebar"]{ background:#161A23; }
        section[data-testid="stSidebar"] *{ color:#E7E9EE !important; }
        section[data-testid="stSidebar"] hr{ border-color:#2C3242; }
        section[data-testid="stSidebar"] .stRadio label p{ font-size:0.92rem; }
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{ color:#AEB4C2 !important; }

        /* Eyebrow / section header */
        .eyebrow{ display:flex; align-items:center; gap:10px; font-family:'IBM Plex Mono',monospace;
                font-size:0.76rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--accent);
                margin-bottom:0.5rem; }
        .eyebrow .num{ background:var(--ink); color:#fff; padding:2px 9px; border-radius:6px; font-weight:600; }
        .eyebrow .rule{ flex:1; height:1px; background:var(--border); }
        .section-title{ font-size:2.05rem; font-weight:700; margin:0 0 0.25rem 0; color:var(--ink); }
        .section-sub{ color:var(--muted); font-size:1.02rem; margin-bottom:1.3rem; max-width:760px; line-height:1.55; }

        /* Cards */
        .card{ background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
            padding:1.5rem 1.7rem; margin-bottom:1.1rem; box-shadow:0 1px 2px rgba(20,20,30,0.03); }
        .card h4{ margin-top:0; margin-bottom:0.7rem; font-size:1.15rem; }
        .card p{ color:#2B313D; line-height:1.65; margin:0 0 0.7rem 0; font-size:0.98rem; }
        .card p:last-child{ margin-bottom:0; }
        .card ul{ margin:0.3rem 0 0.7rem 0; padding-left:1.2rem; }
        .card li{ color:#2B313D; line-height:1.6; margin-bottom:0.35rem; font-size:0.98rem; }
        .card .kicker{ font-family:'IBM Plex Mono',monospace; font-size:0.72rem; text-transform:uppercase;
                        letter-spacing:0.08em; color:var(--muted); margin-bottom:0.4rem; }

        /* Callouts */
        .callout{ border-radius:12px; padding:1rem 1.3rem; margin:0.4rem 0 1.1rem 0; border-left:4px solid var(--accent);
                background:var(--accent-soft); }
        .callout.insight{ border-left-color:var(--accent-violet); background:var(--accent-violet-soft); }
        .callout.note{ border-left-color:var(--accent-sage); background:var(--accent-sage-soft); }
        .callout .label{ font-family:'IBM Plex Mono',monospace; font-size:0.7rem; text-transform:uppercase;
                        letter-spacing:0.09em; color:var(--ink); opacity:0.55; margin-bottom:0.35rem; }
        .callout p{ margin:0; color:#222836; line-height:1.6; font-size:0.97rem; }

        /* Tags */
        .tag{ display:inline-block; padding:0.24rem 0.75rem; border-radius:999px; background:var(--ink);
            color:#fff !important; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; letter-spacing:0.03em;
            margin:0.15rem 0.35rem 0.15rem 0; }
        .tag.alt{ background:var(--accent); }

        /* Metric tiles */
        .metric-row{ display:flex; gap:0.85rem; flex-wrap:wrap; margin:1.3rem 0 0.4rem 0; }
        .metric-tile{ flex:1; min-width:128px; background:var(--ink); border-radius:14px; padding:0.95rem 1.05rem; }
        .metric-tile .val{ font-family:'Space Grotesk',sans-serif; font-size:1.7rem; font-weight:700; color:#fff; }
        .metric-tile .lbl{ font-size:0.74rem; color:#AEB4C2; margin-top:0.1rem; }

        /* Hero */
        .hero{ background:linear-gradient(135deg,#161A23 0%, #1E2738 55%, #2B2140 100%);
            border-radius:22px; padding:2.6rem 2.8rem 2.2rem 2.8rem; color:#fff; margin-bottom:1.3rem; }
        .hero .eyebrow{ color:#E59A7F; }
        .hero .eyebrow .num{ background:rgba(255,255,255,0.14); }
        .hero .eyebrow .rule{ background:rgba(255,255,255,0.16); }
        .hero h1{ font-size:3rem; line-height:1.04; margin:0.2rem 0 0.7rem 0; color:#fff !important; }
        .hero p.lede{ color:#C9CEDA; font-size:1.06rem; max-width:600px; line-height:1.6; margin-bottom:0.4rem; }

        /* Figures */
        .fig-eyebrow{ font-family:'IBM Plex Mono',monospace; font-size:0.74rem; text-transform:uppercase;
                    letter-spacing:0.08em; color:var(--accent); margin:0.2rem 0 0.5rem 2px; }
        [data-testid="stImage"]{ background:var(--surface); border:1px solid var(--border);
                                border-radius:var(--radius); padding:14px; }
        [data-testid="stImage"] img{ border-radius:6px; }
        [data-testid="stCaptionContainer"]{ font-family:'IBM Plex Mono',monospace !important; color:var(--muted) !important;
                                            font-size:0.82rem !important; padding:0.4rem 0.2rem 0 0.2rem; }

        /* KaTeX formula blocks */
        .katex-display{ background:var(--surface) !important; border:1px solid var(--border); border-radius:12px;
                        padding:1rem 1.2rem; margin:0.2rem 0 1.2rem 0 !important; overflow-x:auto; }
        .formula-label{ font-family:'IBM Plex Mono',monospace; font-size:0.74rem; text-transform:uppercase;
                        letter-spacing:0.08em; color:var(--muted); margin:0.1rem 0 0.2rem 2px; }

        /* Dataframe */
        [data-testid="stDataFrame"]{ border:1px solid var(--border); border-radius:12px; overflow:hidden; }

        /* Footer */
        .app-footer{ margin-top:2.6rem; padding-top:1.1rem; border-top:1px solid var(--border);
                    color:var(--muted); font-size:0.84rem; }

        hr{ border-color:var(--border); margin:1.4rem 0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


    # ----------------------------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------------------------
    def section_header(num: str, eyebrow_text: str, title: str, subtitle: str = ""):
        sub_html = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
        st.markdown(
            f"""
            <div class="eyebrow"><span class="num">{num}</span><span>{eyebrow_text}</span><span class="rule"></span></div>
            <div class="section-title">{title}</div>
            {sub_html}
            """,
            unsafe_allow_html=True,
        )


    def card(title: str, paragraphs=None, items=None, kicker: str = ""):
        paragraphs = paragraphs or []
        kicker_html = f'<div class="kicker">{kicker}</div>' if kicker else ""
        title_html = f"<h4>{title}</h4>" if title else ""
        body = "".join(f"<p>{p}</p>" for p in paragraphs)
        if items:
            body += "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
        st.markdown(f'<div class="card">{kicker_html}{title_html}{body}</div>', unsafe_allow_html=True)


    def callout(kind: str, label: str, text: str):
        st.markdown(
            f'<div class="callout {kind}"><div class="label">{label}</div><p>{text}</p></div>',
            unsafe_allow_html=True,
        )


    def tags_row(tags, alt_index=None):
        spans = "".join(
            f'<span class="tag{" alt" if i == alt_index else ""}">{t}</span>' for i, t in enumerate(tags)
        )
        st.markdown(f"<div>{spans}</div>", unsafe_allow_html=True)


    def metrics_row(items):
        tiles = "".join(
            f'<div class="metric-tile"><div class="val">{v}</div><div class="lbl">{l}</div></div>'
            for v, l in items
        )
        st.markdown(f'<div class="metric-row">{tiles}</div>', unsafe_allow_html=True)


    def formula(label: str, latex: str):
        st.markdown(f'<div class="formula-label">{label}</div>', unsafe_allow_html=True)
        st.latex(latex)


    def figure(filename: str, label: str, caption: str, width_pct: int = 100):
        path = Path(ASSETS_DIR) / filename
        st.markdown(f'<div class="fig-eyebrow">{label}</div>', unsafe_allow_html=True)
        if path.exists():
            if width_pct < 100:
                c1, c2, c3 = st.columns([(100 - width_pct) / 2, width_pct, (100 - width_pct) / 2])
                with c2:
                    st.image(str(path), use_container_width=True)
            else:
                st.image(str(path), use_container_width=True)
            st.caption(caption)
        else:
            st.warning(f"Missing image asset: {filename}")


    ATTENTION_SVG = """
    <svg viewBox="0 0 760 168" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:620px;height:auto;display:block;margin-top:0.4rem;">
    <path d="M 584 138 Q 347 28 110 138" fill="none" stroke="#E0552B" stroke-width="3" opacity="0.92"/>
    <path d="M 584 138 Q 639 112 694 138" fill="none" stroke="#8A7CC4" stroke-width="2" opacity="0.45"/>
    <path d="M 584 138 Q 501 100 418 138" fill="none" stroke="#7C8398" stroke-width="1.6" opacity="0.32"/>
    <text x="20" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#C9CEDA">The</text>
    <text x="71.8" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#F0805E" font-weight="600">animal</text>
    <text x="161.4" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#C9CEDA">didn't</text>
    <text x="251.0" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#C9CEDA">cross</text>
    <text x="328.0" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#C9CEDA">the</text>
    <text x="379.8" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#7C8398">street</text>
    <text x="469.4" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#C9CEDA">because</text>
    <text x="571.6" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#FFFFFF" font-weight="700">it</text>
    <text x="610.8" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#C9CEDA">was</text>
    <text x="662.6" y="150" font-family="IBM Plex Mono, monospace" font-size="21" fill="#7C8398">tired</text>
    </svg>
    """

    ATTENTION_SVG_LIGHT = ATTENTION_SVG.replace("#C9CEDA", "#454C5A").replace(
        "#FFFFFF", "#161A23"
    ).replace("#7C8398", "#9CA3B0")


    # ----------------------------------------------------------------------------
    # Data
    # ----------------------------------------------------------------------------
    PAGES = [
        "Home",
        "1. Abstract",
        "2. Introduction",
        "3. Background",
        "4. Model Architecture",
        "5. Attention Mechanism",
        "6. Why Self-Attention",
        "7. Training",
        "8. Results",
        "9. Conclusion",
        "Credits & References",
    ]

    authors = [
        ("Ashish Vaswani", "Google Brain", "Co-designed and implemented the first Transformer models"),
        ("Noam Shazeer", "Google Brain", "Proposed scaled dot-product attention, multi-head attention, parameter-free position representation"),
        ("Niki Parmar", "Google Research", "Designed, implemented, tuned and evaluated countless model variants"),
        ("Jakob Uszkoreit", "Google Research", "Proposed replacing RNNs with self-attention; started the evaluation effort"),
        ("Llion Jones", "Google Research", "Novel model variants, initial codebase, efficient inference & visualizations"),
        ("Aidan N. Gomez", "University of Toronto", "Co-built tensor2tensor, improving results and research speed"),
        ("Łukasz Kaiser", "Google Brain", "Co-built tensor2tensor, improving results and research speed"),
        ("Illia Polosukhin", "—", "Co-designed and implemented the first Transformer models"),
    ]

    layer_complexity = pd.DataFrame(
        [
            ["Self-Attention", "O(n\u00b2\u00b7d)", "O(1)", "O(1)"],
            ["Recurrent", "O(n\u00b7d\u00b2)", "O(n)", "O(n)"],
            ["Convolutional", "O(k\u00b7n\u00b7d\u00b2)", "O(1)", "O(log\u2096(n))"],
            ["Self-Attention (restricted)", "O(r\u00b7n\u00b7d)", "O(1)", "O(n/r)"],
        ],
        columns=["Layer Type", "Complexity per Layer", "Sequential Operations", "Maximum Path Length"],
    )

    results_table = pd.DataFrame(
        [
            ["ByteNet", 23.75, None, None, None],
            ["GNMT + RL", 24.60, 39.92, "2.3\u00d710\u00b9\u2079", "1.4\u00d710\u00b2\u2070"],
            ["ConvS2S", 25.16, 40.46, "9.6\u00d710\u00b9\u2078", "1.5\u00d710\u00b2\u2070"],
            ["Transformer (base)", 27.30, 38.10, "3.3\u00d710\u00b9\u2078", "\u2014"],
            ["Transformer (big)", 28.40, 41.00, "2.3\u00d710\u00b9\u2079", "\u2014"],
        ],
        columns=["Model", "BLEU EN-DE", "BLEU EN-FR", "Training Cost EN-DE (FLOPs)", "Training Cost EN-FR (FLOPs)"],
    )


    # ----------------------------------------------------------------------------
    # Sidebar
    # ----------------------------------------------------------------------------
    st.sidebar.markdown(
        "<div style='font-family:Space Grotesk,sans-serif;font-size:1.3rem;font-weight:700;color:#fff;'>"
        "Attention Is All You Need</div>"
        "<div style='font-family:IBM Plex Mono,monospace;font-size:0.74rem;color:#9CA3B0;margin-top:0.2rem;'>"
        "STUDY COMPANION</div>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

    page = st.sidebar.radio("Go to section", PAGES, label_visibility="collapsed")

    progress_value = (PAGES.index(page)) / (len(PAGES) - 1)
    st.sidebar.progress(progress_value)
    st.sidebar.caption(f"Section {PAGES.index(page) + 1} of {len(PAGES)}")

    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<div style='font-family:IBM Plex Mono,monospace;font-size:0.72rem;letter-spacing:0.08em;"
        "text-transform:uppercase;color:#9CA3B0;margin-bottom:0.5rem;'>Quick facts</div>"
        "<div style='font-size:0.86rem;line-height:1.9;'>"
        "<b>Architecture</b> Transformer<br/>"
        "<b>Venue</b> NIPS 2017<br/>"
        "<b>Heads</b> 8 &nbsp;·&nbsp; <b>Layers</b> 6 + 6<br/>"
        "<b>d_model</b> 512 &nbsp;·&nbsp; <b>d_ff</b> 2048<br/>"
        "<b>BLEU EN-DE</b> 28.4<br/>"
        "<b>BLEU EN-FR</b> 41.0"
        "</div>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
    st.sidebar.caption("Figures and tables are cropped directly from the source PDF.")


    # ----------------------------------------------------------------------------
    # HOME
    # ----------------------------------------------------------------------------
    if page == "Home":
        st.markdown(
            f"""
            <div class="hero">
                <div class="eyebrow"><span class="num">NIPS</span><span>2017 \u00b7 Google Brain \u00b7 Google Research \u00b7 University of Toronto</span><span class="rule"></span></div>
                <h1>Attention Is All You Need</h1>
                <p class="lede">The paper that removed recurrence and convolution from sequence transduction
                entirely, replacing them with self-attention — and became the architecture behind nearly
                every large language model that followed.</p>
                {ATTENTION_SVG}
            </div>
            """,
            unsafe_allow_html=True,
        )

        tags_row(["Transformer", "Self-Attention", "Encoder-Decoder", "Machine Translation"], alt_index=0)

        metrics_row(
            [
                ("28.4", "BLEU \u00b7 EN\u2192DE"),
                ("41.0", "BLEU \u00b7 EN\u2192FR"),
                ("8", "Attention heads"),
                ("6 + 6", "Encoder / decoder layers"),
                ("3.5 days", "Big model training time"),
            ]
        )

        st.markdown("<br/>", unsafe_allow_html=True)
        left, right = st.columns([1.2, 1])
        with left:
            card(
                "What this companion covers",
                paragraphs=[
                    "This app turns the paper into a section-by-section guide: the original figures and "
                    "tables, pulled straight from the PDF, paired with plain-language explanations of the "
                    "architecture, the attention mechanism, and the training setup.",
                ],
            )
            card(
                "Authors",
                paragraphs=[
                    ", ".join(a[0] for a in authors)
                    + ". Listing order is random — the paper notes all authors contributed equally."
                ],
                kicker="Google Brain \u00b7 Google Research \u00b7 University of Toronto",
            )
            callout(
                "insight",
                "Main idea",
                "Replace recurrence and convolution with attention alone. Every position can look directly "
                "at every other position in a constant number of steps, which makes training far more "
                "parallelizable and shortens the path signals travel between distant words.",
            )
        with right:
            figure("transformer_architecture.png", "FIG. 1 \u2014 ORIGINAL FIGURE FROM THE PDF", "The Transformer model architecture: encoder on the left, decoder on the right.")

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title" style="font-size:1.5rem;">Map of the paper</div>'
            '<div class="section-sub">Use the sidebar to move through it section by section.</div>',
            unsafe_allow_html=True,
        )
        toc = [
            ("01", "Abstract", "The result in three sentences."),
            ("02", "Introduction", "Why sequential computation was the bottleneck."),
            ("03", "Background", "Prior work on reducing sequential computation."),
            ("04", "Model Architecture", "Encoder/decoder stacks, embeddings, positional encoding."),
            ("05", "Attention Mechanism", "Scaled dot-product and multi-head attention, in detail."),
            ("06", "Why Self-Attention", "The complexity/parallelism/path-length argument."),
            ("07", "Training", "Data, hardware, optimizer, regularization."),
            ("08", "Results", "BLEU scores, training cost, and architecture ablations."),
            ("09", "Conclusion", "What the authors took away, and what came next."),
        ]
        cols = st.columns(3)
        for i, (num, title, desc) in enumerate(toc):
            with cols[i % 3]:
                st.markdown(
                    f'<div class="card" style="min-height:118px;">'
                    f'<div class="kicker">{num}</div>'
                    f'<h4 style="font-size:1.02rem;">{title}</h4>'
                    f'<p style="font-size:0.9rem;">{desc}</p></div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            '<div class="app-footer">Built as a study companion from the uploaded paper PDF. '
            "Not affiliated with the authors or Google — for academic use, cite the original paper.</div>",
            unsafe_allow_html=True,
        )


    # ----------------------------------------------------------------------------
    # 1. ABSTRACT
    # ----------------------------------------------------------------------------
    elif page == "1. Abstract":
        section_header("01", "The 30-second version", "Abstract")

        card(
            "",
            paragraphs=[
                "The strongest sequence transduction models at the time were complex recurrent or "
                "convolutional networks built around an encoder and a decoder, with the best of them "
                "also connecting encoder and decoder through an attention mechanism.",
                "This paper proposes the <b>Transformer</b>, a simpler architecture based solely on "
                "attention mechanisms — recurrence and convolutions are dispensed with entirely.",
                "On two machine translation tasks, the resulting models are not only higher quality, "
                "they're also more parallelizable and need significantly less time to train.",
            ],
        )

        metrics_row(
            [
                ("28.4", "BLEU on WMT14 EN\u2192DE \u00b7 +2 over prior best (incl. ensembles)"),
                ("41.0", "BLEU on WMT14 EN\u2192FR \u00b7 new single-model state of the art"),
                ("3.5 days", "Training time for the big model, on 8 GPUs"),
            ]
        )

        callout(
            "insight",
            "In plain words",
            "We can translate sequences using attention only — and because it skips the slow, "
            "step-by-step recurrence of RNNs, it's also considerably faster to train.",
        )


    # ----------------------------------------------------------------------------
    # 2. INTRODUCTION
    # ----------------------------------------------------------------------------
    elif page == "2. Introduction":
        section_header("02", "Setting up the problem", "Introduction")

        card(
            "The sequential bottleneck",
            paragraphs=[
                "Recurrent neural networks — LSTMs and gated recurrent networks especially — were the "
                "established state of the art for sequence modeling and transduction problems like "
                "language modeling and machine translation.",
                "Recurrent models factor computation along the symbol positions of the input and output: "
                "a hidden state h<sub>t</sub> is generated as a function of the previous hidden state "
                "h<sub>t\u22121</sub> and the input at position t. That sequential dependency precludes "
                "parallelization within a training example, which becomes a real constraint at longer "
                "sequence lengths, since memory limits how much batching can compensate.",
                "Factorization tricks and conditional computation had improved efficiency and, in some "
                "cases, performance — but the fundamental constraint of sequential computation remained.",
            ],
        )

        card(
            "Attention, so far",
            paragraphs=[
                "Attention mechanisms had already become integral to strong sequence models, letting them "
                "capture dependencies without regard to distance in the input or output. In nearly every "
                "case, though, attention was used <i>alongside</i> a recurrent network, not in place of one.",
            ],
        )

        callout(
            "insight",
            "What this paper proposes",
            "The Transformer eschews recurrence entirely and relies wholly on an attention mechanism to "
            "draw global dependencies between input and output. That allows for significantly more "
            "parallelization, and the model reaches a new state of the art after as little as twelve "
            "hours of training on eight P100 GPUs.",
        )

        callout(
            "note",
            "Simple version",
            "Instead of reading words one-by-one like an RNN, the Transformer lets every word look at "
            "every other word directly — so it doesn't have to wait its turn.",
        )


    # ----------------------------------------------------------------------------
    # 3. BACKGROUND
    # ----------------------------------------------------------------------------
    elif page == "3. Background":
        section_header("03", "Prior work", "Background")

        card(
            "Reducing sequential computation",
            paragraphs=[
                "The same goal — cutting down sequential computation — also motivated the Extended Neural "
                "GPU, ByteNet, and ConvS2S, which all use convolutional networks as their basic building "
                "block, computing hidden representations for every input and output position in parallel.",
                "In those models, the number of operations needed to relate two arbitrary positions grows "
                "with the distance between them: linearly for ConvS2S, logarithmically for ByteNet — which "
                "makes distant dependencies harder to learn. The Transformer reduces this to a "
                "<b>constant</b> number of operations, at the cost of reduced effective resolution from "
                "averaging attention-weighted positions — an effect counteracted with multi-head attention.",
            ],
        )

        card(
            "Self-attention",
            paragraphs=[
                "Self-attention, sometimes called intra-attention, relates different positions of a single "
                "sequence to compute a representation of that sequence. It had already been used "
                "successfully for reading comprehension, abstractive summarization, textual entailment, "
                "and learning task-independent sentence representations.",
                "End-to-end memory networks, built on a recurrent attention mechanism rather than "
                "sequence-aligned recurrence, had shown strong results on simple-language question "
                "answering and language modeling.",
            ],
        )

        callout(
            "insight",
            "What's new here",
            "To the authors' knowledge, the Transformer is the first transduction model to rely entirely "
            "on self-attention to compute representations of its input and output, without any "
            "sequence-aligned RNNs or convolution.",
        )

        st.markdown('<div class="fig-eyebrow">WORKED EXAMPLE</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card">{ATTENTION_SVG_LIGHT}'
            '<p style="margin-top:0.8rem;">In <i>"The animal didn\'t cross the street because it was '
            'tired,"</i> self-attention lets the model connect <b>it</b> directly to <b>animal</b> — '
            "no matter how many words sit in between.</p></div>",
            unsafe_allow_html=True,
        )


    # ----------------------------------------------------------------------------
    # 4. MODEL ARCHITECTURE
    # ----------------------------------------------------------------------------
    elif page == "4. Model Architecture":
        section_header("04", "How it's built", "Model Architecture")
        card(
            "",
            paragraphs=[
                "The Transformer keeps the overall encoder-decoder structure common to competitive "
                "sequence transduction models: an encoder maps an input sequence to a sequence of "
                "continuous representations, and a decoder then generates an output sequence one element "
                "at a time, consuming previously generated symbols as additional input at each step "
                "(auto-regressive). What changes is what the encoder and decoder are built from."
            ],
        )
        figure("transformer_architecture.png", "FIG. 1 \u2014 ORIGINAL FIGURE FROM THE PDF", "The full encoder (left) and decoder (right) stacks.", width_pct=64)

        c1, c2 = st.columns(2)
        with c1:
            card(
                "4.1 \u00b7 Encoder",
                paragraphs=[
                    "A stack of <b>N = 6</b> identical layers. Each layer has two sub-layers: a multi-head "
                    "self-attention mechanism, then a position-wise fully connected feed-forward network.",
                    "Each sub-layer is wrapped in a residual connection followed by layer normalization, "
                    "so every sub-layer's output is LayerNorm(x + Sublayer(x)). To make that addition "
                    "work, every sub-layer and embedding layer produces outputs of dimension "
                    "<b>d_model = 512</b>.",
                ],
            )
        with c2:
            card(
                "4.2 \u00b7 Decoder",
                paragraphs=[
                    "Also a stack of <b>N = 6</b> identical layers. Alongside the encoder's two sub-layers, "
                    "the decoder inserts a third: multi-head attention over the encoder stack's output.",
                    "The self-attention sub-layer here is <b>masked</b> so positions can't attend to "
                    "subsequent positions. Combined with output embeddings being offset by one position, "
                    "this guarantees predictions for position i depend only on outputs already known at "
                    "positions less than i — keeping generation auto-regressive.",
                ],
            )

        formula("Every sub-layer's output", r"\text{LayerNorm}(x + \text{Sublayer}(x))")

        card(
            "4.3 \u00b7 Embeddings and softmax",
            paragraphs=[
                "Input and output tokens are converted to vectors of dimension d_model via learned "
                "embeddings. A learned linear transformation plus softmax converts decoder output into "
                "next-token probabilities, and the same weight matrix is shared between both embedding "
                "layers and the pre-softmax linear layer. In the embedding layers, those weights are "
                "multiplied by \u221ad_model.",
            ],
        )

        card(
            "4.4 \u00b7 Positional encoding",
            paragraphs=[
                "Since the model has no recurrence and no convolution, it needs another way to use the "
                "order of the sequence — so positional encodings are added to the input embeddings at the "
                "bottom of both stacks, sharing the same dimension d_model so the two can be summed.",
                "The paper uses sine and cosine functions of different frequencies, chosen on the "
                "hypothesis that they'd let the model learn to attend by relative position, since "
                "PE<sub>pos+k</sub> can be expressed as a linear function of PE<sub>pos</sub> for any fixed "
                "offset k. Learned positional embeddings produced nearly identical results in testing — "
                "sinusoidal encoding was kept because it may let the model extrapolate to sequence lengths "
                "longer than any seen during training.",
            ],
        )
        formula("Positional encoding", r"PE_{(pos,\,2i)} = \sin\left(\dfrac{pos}{10000^{2i/d_{model}}}\right) \qquad PE_{(pos,\,2i+1)} = \cos\left(\dfrac{pos}{10000^{2i/d_{model}}}\right)")


    # ----------------------------------------------------------------------------
    # 5. ATTENTION MECHANISM
    # ----------------------------------------------------------------------------
    elif page == "5. Attention Mechanism":
        section_header("05", "The core mechanism", "Attention Mechanism")
        card(
            "",
            paragraphs=[
                "An attention function maps a query and a set of key-value pairs to an output — all of "
                "them vectors. The output is a weighted sum of the values, where each value's weight comes "
                "from a compatibility function between the query and the corresponding key.",
            ],
        )

        c1, c2 = st.columns(2)
        with c1:
            figure("scaled_dot_product_attention.png", "FIG. 2 (LEFT)", "Scaled Dot-Product Attention.", width_pct=72)
        with c2:
            figure("multi_head_attention.png", "FIG. 2 (RIGHT)", "Multi-Head Attention: several attention layers running in parallel.", width_pct=72)

        card(
            "5.1 \u00b7 Scaled dot-product attention",
            paragraphs=[
                "Queries and keys have dimension d_k, values have dimension d_v. The dot product of the "
                "query with every key is computed, divided by \u221ad_k, then passed through softmax to "
                "obtain the weights on the values.",
                "Dot-product attention is identical to the more common additive attention except for that "
                "scaling factor. The two are similar in theoretical complexity, but dot-product attention "
                "is much faster and more space-efficient in practice, since it runs on highly optimized "
                "matrix multiplication.",
                "Without scaling, large d_k pushes the dot products to large magnitudes, which pushes "
                "softmax into regions with extremely small gradients — the \u221ad_k scaling exists "
                "specifically to counteract that.",
            ],
        )
        formula("Scaled dot-product attention", r"\text{Attention}(Q, K, V) = \text{softmax}\!\left(\dfrac{QK^{T}}{\sqrt{d_k}}\right)V")

        card(
            "5.2 \u00b7 Multi-head attention",
            paragraphs=[
                "Rather than performing one attention function on full d_model-dimensional keys, values "
                "and queries, the model linearly projects them h times with different learned projections "
                "down to d_k, d_k and d_v dimensions, runs attention on each projection in parallel, "
                "concatenates the results, and projects once more.",
                "This lets the model jointly attend to information from different representation subspaces "
                "at different positions — something a single attention head's averaging would inhibit. "
                "The paper uses <b>h = 8</b> heads with d_k = d_v = d_model/h = <b>64</b>, so the total "
                "computational cost stays close to single-head attention at full dimensionality.",
            ],
        )
        formula("Multi-head attention", r"\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\,W^{O} \qquad \text{head}_i = \text{Attention}(QW_i^{Q}, KW_i^{K}, VW_i^{V})")

        card(
            "5.3 \u00b7 Three uses of attention in the Transformer",
            items=[
                "<b>Encoder-decoder attention</b> — queries come from the previous decoder layer; keys and "
                "values come from the encoder's output, letting every decoder position attend over the "
                "entire input sequence.",
                "<b>Encoder self-attention</b> — queries, keys and values all come from the same place, "
                "the previous encoder layer's output, so each position can attend to every position in "
                "that layer.",
                "<b>Decoder self-attention</b> — each position attends to all decoder positions up to and "
                "including itself; illegal leftward connections are masked out (set to \u2212\u221e before "
                "the softmax) to preserve the auto-regressive property.",
            ],
        )

        card(
            "5.4 \u00b7 Position-wise feed-forward networks",
            paragraphs=[
                "Each encoder and decoder layer also contains a fully connected feed-forward network, "
                "applied identically and separately to every position: two linear transformations with a "
                "ReLU in between. The transformation is the same across positions but uses different "
                "parameters layer to layer — equivalent to two convolutions with kernel size 1. Input and "
                "output dimensionality is d_model = 512; the inner layer has dimensionality d_ff = 2048.",
            ],
        )
        formula("Feed-forward network", r"\text{FFN}(x) = \max(0,\, xW_1 + b_1)\,W_2 + b_2")


    # ----------------------------------------------------------------------------
    # 6. WHY SELF-ATTENTION
    # ----------------------------------------------------------------------------
    elif page == "6. Why Self-Attention":
        section_header("06", "The argument", "Why Self-Attention")
        card(
            "",
            paragraphs=[
                "Self-attention is compared against recurrent and convolutional layers on three criteria: "
                "total computational complexity per layer, how much computation can be parallelized "
                "(measured by the minimum number of required sequential operations), and the path length "
                "between long-range dependencies — shorter paths make it easier for a network to learn "
                "long-range dependencies in the first place.",
            ],
        )

        figure("table1_complexity.png", "TABLE 1 \u2014 ORIGINAL TABLE FROM THE PDF", "Complexity, sequential operations, and maximum path length by layer type.", width_pct=80)

        with st.expander("View as a plain table"):
            st.dataframe(layer_complexity, use_container_width=True, hide_index=True)

        card(
            "Reading the comparison",
            paragraphs=[
                "A self-attention layer connects all positions with a constant number of sequential "
                "operations, while a recurrent layer needs O(n). In terms of raw complexity, self-attention "
                "is actually faster than recurrence whenever the sequence length n is smaller than the "
                "representation dimension d — the common case for the word-piece and byte-pair "
                "representations used by state-of-the-art translation models.",
                "For very long sequences, self-attention could be restricted to a neighborhood of size r "
                "around each output position, which would raise the maximum path length to O(n/r) — the "
                "paper flags this as a direction for future work rather than something it implements.",
                "A single convolutional layer with kernel width k < n doesn't connect every pair of "
                "positions on its own; doing so needs a stack of O(n/k) layers (contiguous kernels) or "
                "O(log<sub>k</sub>(n)) layers (dilated convolutions). Convolutional layers are also "
                "generally costlier than recurrent ones by a factor of k. Separable convolutions cut that "
                "cost considerably — but even then, their complexity matches a self-attention layer "
                "combined with a point-wise feed-forward layer, which is exactly the combination the "
                "Transformer uses.",
            ],
        )

        callout(
            "note",
            "A side benefit",
            "Self-attention may also make models more interpretable: individual attention heads appear to "
            "learn distinct tasks, and many seem to track the syntactic and semantic structure of "
            "sentences — something the paper explores further in its appendix.",
        )


    # ----------------------------------------------------------------------------
    # 7. TRAINING
    # ----------------------------------------------------------------------------
    elif page == "7. Training":
        section_header("07", "How it was trained", "Training")

        metrics_row(
            [
                ("4.5M", "EN-DE sentence pairs (WMT 2014)"),
                ("36M", "EN-FR sentence pairs (WMT 2014)"),
                ("8\u00d7P100", "GPUs, one machine"),
                ("100K / 12h", "Base model steps / time"),
                ("300K / 3.5d", "Big model steps / time"),
            ]
        )

        c1, c2 = st.columns(2)
        with c1:
            card(
                "7.1 \u00b7 Data and batching",
                paragraphs=[
                    "English-German training used the standard WMT 2014 dataset, about 4.5 million "
                    "sentence pairs, encoded with byte-pair encoding over a shared ~37,000-token "
                    "vocabulary. English-French used the much larger WMT 2014 dataset — 36M sentences — "
                    "split into a 32,000-token word-piece vocabulary.",
                    "Sentence pairs were batched by approximate sequence length, with each training batch "
                    "holding roughly 25,000 source tokens and 25,000 target tokens.",
                ],
            )
        with c2:
            card(
                "7.2 \u00b7 Hardware and schedule",
                paragraphs=[
                    "Training ran on a single machine with 8 NVIDIA P100 GPUs. Base-model steps took about "
                    "0.4 seconds each, for a total of 100,000 steps — roughly 12 hours. Big-model steps "
                    "took about 1.0 second each, for 300,000 steps — roughly 3.5 days.",
                ],
            )

        card(
            "7.3 \u00b7 Optimizer",
            paragraphs=[
                "Adam, with \u03b21 = 0.9, \u03b22 = 0.98, \u03b5 = 10\u207b\u2079. The learning rate "
                "increases linearly for the first warmup_steps, then decreases proportionally to the "
                "inverse square root of the step number. <b>warmup_steps = 4000</b>.",
            ],
        )
        formula("Learning-rate schedule", r"lrate = d_{model}^{-0.5} \cdot \min\!\left(\text{step\_num}^{-0.5},\; \text{step\_num} \cdot \text{warmup\_steps}^{-1.5}\right)")

        card(
            "7.4 \u00b7 Regularization",
            paragraphs=[
                "Two kinds of regularization: residual dropout, applied to each sub-layer's output before "
                "it's added back and normalized, plus dropout applied to the sum of embeddings and "
                "positional encodings in both stacks — the base model uses P_drop = 0.1.",
                "Label smoothing of \u03b5_ls = 0.1 is also used. It hurts perplexity, since the model "
                "learns to be less certain, but it improves accuracy and BLEU score.",
            ],
        )


    # ----------------------------------------------------------------------------
    # 8. RESULTS
    # ----------------------------------------------------------------------------
    elif page == "8. Results":
        section_header("08", "How it performed", "Results")

        figure("table2_results.png", "TABLE 2 \u2014 ORIGINAL TABLE FROM THE PDF", "BLEU score and training cost against prior state-of-the-art models.", width_pct=85)

        with st.expander("View as a plain table"):
            st.dataframe(results_table, use_container_width=True, hide_index=True)

        card(
            "8.1 \u00b7 Machine translation",
            paragraphs=[
                "On WMT 2014 English-to-German, the big Transformer reaches <b>28.4 BLEU</b>, beating the "
                "best previously reported models — including ensembles — by more than 2.0 BLEU, after 3.5 "
                "days of training on 8 P100 GPUs. Even the base model surpasses every previously published "
                "model and ensemble, at a fraction of their training cost.",
                "On WMT 2014 English-to-French, the big model reaches <b>41.0 BLEU</b>, beating every "
                "previously published single model at under a quarter of the training cost of the prior "
                "state of the art. For this task the big model used a dropout rate of 0.1 rather than 0.3.",
                "Final base-model results average the last 5 checkpoints (written at 10-minute intervals); "
                "big-model results average the last 20. Decoding uses beam search with beam size 4 and "
                "length penalty \u03b1 = 0.6, with maximum output length set to input length + 50 and "
                "early termination where possible.",
            ],
        )

        card(
            "8.2 \u00b7 Model variations",
            paragraphs=[
                "Holding total computation roughly constant, the authors varied head count and "
                "key/value dimensions, model size, dropout, and the choice between sinusoidal and learned "
                "positional encodings — measured on the English-to-German development set.",
            ],
            items=[
                "Single-head attention scores 0.9 BLEU below the best setting; quality also drops off "
                "again with too many heads.",
                "Shrinking the attention key size d_k hurts quality, suggesting the compatibility function "
                "matters — dot product may not be the most sophisticated option.",
                "Bigger models perform better, as expected, and dropout meaningfully helps avoid "
                "overfitting.",
                "Learned positional embeddings and sinusoidal positional encoding give nearly identical "
                "results in this setting.",
            ],
        )
        figure("table3_variations.png", "TABLE 3 \u2014 ORIGINAL TABLE FROM THE PDF", "Architecture variations and their effect on dev-set perplexity and BLEU.", width_pct=92)


    # ----------------------------------------------------------------------------
    # 9. CONCLUSION
    # ----------------------------------------------------------------------------
    elif page == "9. Conclusion":
        section_header("09", "Where it lands", "Conclusion")

        card(
            "",
            paragraphs=[
                "The Transformer is presented as the first sequence transduction model built entirely on "
                "attention, replacing the recurrent layers most encoder-decoder architectures relied on "
                "with multi-headed self-attention.",
                "For translation specifically, it trains significantly faster than architectures based on "
                "recurrent or convolutional layers, and reaches a new state of the art on both WMT 2014 "
                "English-to-German and English-to-French — on the former, the best model outperforms even "
                "every previously reported ensemble.",
            ],
        )

        card(
            "Future directions named in the paper",
            items=[
                "Apply attention-based models to tasks beyond text.",
                "Extend the Transformer to other input/output modalities — images, audio, video.",
                "Investigate local, restricted attention to handle very large inputs and outputs "
                "efficiently.",
                "Make generation less sequential.",
            ],
        )

        callout(
            "insight",
            "Final takeaway",
            "By making attention the core operation instead of a supplement to recurrence, the Transformer "
            "opened the door to training sequence models at a scale and speed that wasn't practical "
            "before — which is a large part of why it became the foundation for the language models that "
            "followed.",
        )

        st.caption(
            "Training and evaluation code referenced in the paper was released as tensor2tensor on "
            "GitHub. The authors thank Nal Kalchbrenner and Stephan Gouws for comments, corrections, "
            "and inspiration."
        )


    # ----------------------------------------------------------------------------
    # CREDITS & REFERENCES
    # ----------------------------------------------------------------------------
    elif page == "Credits & References":
        section_header("\u2014", "Source material", "Credits & References")

        card(
            "Paper",
            paragraphs=[
                "<b>Title</b> Attention Is All You Need<br/>"
                "<b>Venue</b> 31st Conference on Neural Information Processing Systems (NIPS 2017), "
                "Long Beach, CA, USA<br/>"
                "<b>Institutions</b> Google Brain, Google Research, University of Toronto",
            ],
        )

        st.markdown('<div class="fig-eyebrow">AUTHOR CONTRIBUTIONS</div>', unsafe_allow_html=True)
        st.markdown(
            "<div class='card'><p style='margin-bottom:1rem;color:var(--muted);font-size:0.9rem;'>"
            "All authors contributed equally; listing order is random, per the paper's own footnote.</p>"
            + "".join(
                f"<p><b>{name}</b> &nbsp;\u00b7&nbsp; <span class='mono' style='color:var(--muted);"
                f"font-size:0.85rem;'>{affil}</span><br/>"
                f"<span style='font-size:0.92rem;'>{contribution}</span></p>"
                for name, affil, contribution in authors
            )
            + "</div>",
            unsafe_allow_html=True,
        )

        card(
            "Image and table credits",
            paragraphs=["Every figure and table shown in this app is cropped directly from the uploaded PDF:"],
            items=[
                "Figure 1 \u2014 Transformer model architecture (page 3)",
                "Figure 2 \u2014 Scaled dot-product attention and multi-head attention (page 4)",
                "Table 1 \u2014 Complexity and path-length comparison (page 6)",
                "Table 2 \u2014 BLEU score and training-cost results (page 8)",
                "Table 3 \u2014 Architecture variations (page 9)",
            ],
        )

        st.markdown('<div class="fig-eyebrow">SELECTED REFERENCES</div>', unsafe_allow_html=True)
        with st.expander("Show major reference list"):
            refs = [
                "Ba, Kiros & Hinton \u2014 Layer Normalization",
                "Bahdanau, Cho & Bengio \u2014 Neural Machine Translation by Jointly Learning to Align and Translate",
                "Britz, Goldie, Luong & Le \u2014 Massive Exploration of Neural Machine Translation Architectures",
                "Cho et al. \u2014 RNN Encoder-Decoder for Statistical Machine Translation",
                "Gehring et al. \u2014 Convolutional Sequence to Sequence Learning",
                "Hochreiter & Schmidhuber \u2014 Long Short-Term Memory",
                "Kingma & Ba \u2014 Adam: A Method for Stochastic Optimization",
                "Sennrich, Haddow & Birch \u2014 Neural Machine Translation of Rare Words with Subword Units",
                "Sukhbaatar et al. \u2014 End-To-End Memory Networks",
                "Wu et al. \u2014 Google's Neural Machine Translation System",
            ]
            for r in refs:
                st.markdown(f"- {r}")

        st.markdown(
            '<div class="app-footer">This is a study companion generated from the uploaded PDF, not an '
            "official artifact. For academic use, cite the original paper: Vaswani et al., "
            '"Attention Is All You Need," NeurIPS 2017.</div>',
            unsafe_allow_html=True,
        )
