# A Functional Taxonomy of the Web of Agents

<!-- Replace the Zenodo badge below once the webhook mints a DOI -->
[![DOI](https://zenodo.org/badge/DOI/PLACEHOLDER.svg)](https://doi.org/PLACEHOLDER)

Companion repository for the article

> **A Functional Taxonomy of the Web of Agents: Operational Definitions
> and an Empirical Validation Protocol.** Tatiana Petrova.

The repository contains the LaTeX source and a compiled PDF of the
article, together with every artefact needed to reproduce the E4a
LLM-self-consistency pilot reported in Section 5: the operational
codebook, the standardized rater prompt, the five-system local
specification corpus, three independent rater outputs, and a script
that recomputes pairwise agreement and Cohen's kappa.

## Repository layout

```
.
├── paper/
│   ├── woa_taxonomy.tex          Article source
│   ├── woa_taxonomy.pdf          Compiled article
│   ├── references.bib            Bibliography
│   └── figures/                  Figures referenced by the article
│       ├── fig1_history.pdf
│       ├── fig2_taxonomy.pdf
│       └── fig3_sequence_car.pdf
│
├── experiments/
│   ├── taxonomy_codebook.md      Codebook v1.0 used by raters
│   ├── standardized_prompt.md    Exact prompt given to each rater
│   ├── specs/                    Local specification snapshots
│   │   ├── fipa.txt              FIPA SC00061G + SC00023K (archive.org 2024)
│   │   ├── owls.txt              OWL-S 1.2 W3C Submission (2004)
│   │   ├── langchain.txt         LangChain master README.md + AGENTS.md
│   │   ├── mcp.txt               MCP spec 2025-03-26 (4 source files)
│   │   └── a2a.txt               A2A README + specification.md (main)
│   ├── rater_outputs/
│   │   ├── rater1.csv            Rater 1 raw assignments
│   │   ├── rater2.csv            Rater 2 raw assignments
│   │   └── rater3.csv            Rater 3 raw assignments
│   ├── e4sim_assignments.csv     Long-format merge of the three raters
│   ├── e4sim_matrix.csv          Wide summary with per-item majority vote
│   └── e4sim_results.json        Agreement and Cohen's kappa per axis
│
├── scripts/
│   └── compute_agreement.py      Reproduces every number in Section 5
│
├── CITATION.cff                  Citation metadata
├── .zenodo.json                  Zenodo metadata override
├── LICENSE                       CC-BY-4.0 for article/data
├── LICENSE-CODE                  MIT for scripts
└── .gitignore                    LaTeX build-artefact exclusions
```

## Reproducing the E4a pilot

The pilot measures self-consistency of an LLM classifier applied to a
fixed corpus under a codebook that supplies operational criteria for
each axis value. The raw outputs are archived, so three reproduction
levels are possible.

**1. Recompute statistics from the archived rater outputs (seconds, no
network, no LLM).** Agreement and Cohen's kappa:

```bash
python3 scripts/compute_agreement.py
```

Expected output (identical to the numbers in the article):

```
Axis a1: pct_agree(mean)=1.000  kappa(mean)=1.000
Axis a2: pct_agree(mean)=0.867  kappa(mean)=0.815
Axis a3: pct_agree(mean)=0.867  kappa(mean)=0.804
Axis a4: pct_agree(mean)=1.000  kappa(mean)=1.000
```

**2. Re-run the raters against the archived corpus with any LLM.**
Supply the codebook (`experiments/taxonomy_codebook.md`) and the
prompt (`experiments/standardized_prompt.md`) to three independent
model instances. Each instance reads only from `experiments/specs/`
and writes a rater CSV in the same schema. No web access is needed.

**3. Refresh the corpus from the primary sources.** Replace the files
in `experiments/specs/` with newer snapshots. Upstream URLs at the
time of the 2026-04 snapshot:

- FIPA SC00061G: `http://www.fipa.org/specs/fipa00061/SC00061G.html`
  (fetched via `archive.org` 2024 mirror)
- FIPA SC00023K: `http://www.fipa.org/specs/fipa00023/SC00023K.html`
  (fetched via `archive.org` 2024 mirror)
- OWL-S 1.2: `https://www.w3.org/Submission/OWL-S/`
- LangChain: `github.com/langchain-ai/langchain` master, `README.md`
  and `AGENTS.md`
- MCP 2025-03-26: `github.com/modelcontextprotocol/modelcontextprotocol`
  `docs/specification/2025-03-26/{index,basic/index,basic/transports,server/tools}.mdx`
- A2A: `github.com/a2aproject/A2A` main, `README.md` and
  `docs/specification.md`

Different snapshots will produce different assignments; that is
intentional and is the subject of the Section 5 discussion of corpus
sensitivity.

## Building the paper

```bash
cd paper
pdflatex woa_taxonomy
bibtex   woa_taxonomy
pdflatex woa_taxonomy
pdflatex woa_taxonomy
```

Requires a standard TeX Live installation and the `authblk` package.
The document class is the plain `article` class in two-column layout;
no publisher-specific class files are needed.

## Pilot summary

Three independent LLM rater instances were given an identical codebook
and a locally archived corpus of five agent systems (FIPA ACL, OWL-S,
LangChain, MCP, A2A). Each rater produced a value in `{0.0, 0.5, 1.0,
UNSPECIFIED}` on each of four axes with a verbatim evidence excerpt
(≤15 words) from the corpus.

| Axis                      | Mean pct-agreement | Mean Cohen's kappa | Disagreements |
|---------------------------|-------------------:|-------------------:|--------------:|
| Semantic Foundation (a1)  |              1.000 |              1.000 |             0 |
| Communication (a2)        |              0.867 |              0.815 |             1 |
| Locus of Intelligence (a3)|              0.867 |              0.804 |             1 |
| Discovery Mechanism (a4)  |              1.000 |              1.000 |             0 |

Both item-level disagreements occurred where one rater chose
`UNSPECIFIED` against a terse corpus (OWL-S on a2; LangChain on a3)
and the other two assigned a numeric value. The LangChain result
shows corpus sensitivity: all three raters flagged Axes 1, 2, and 4
as `UNSPECIFIED` because the vendored corpus contains only the
repository-level `README.md` and `AGENTS.md` rather than the long-form
documentation site.

This pilot is **not** a substitute for a human inter-rater-reliability
study. Three parallel LLM instances can share systematic biases that
kappa does not detect. See Section 5 for the full E1/E2/E4 protocol.

## Citing this artefact

Use the Zenodo DOI (link above, once minted) for the archived snapshot
of this repository, or the `CITATION.cff` file for structured
citation metadata.

```
Petrova, T. (2026). A Functional Taxonomy of the Web of Agents:
Operational Definitions and an Empirical Validation Protocol
(v1.0.1) [Paper and data]. Zenodo. https://doi.org/PLACEHOLDER
```

## Licence

- Article text, figures, and the experimental data (codebook,
  specifications corpus, rater outputs, derived tables) are released
  under CC-BY-4.0. See `LICENSE`.
- The reproducibility script in `scripts/` is released under MIT.
  See `LICENSE-CODE`.

The specification corpus in `experiments/specs/` reproduces short
excerpts from third-party documents (FIPA, W3C, OWL-S, MCP, A2A,
LangChain) that remain the property of their respective copyright
holders; they are included here solely for reproducibility and are
used in accordance with each document's licence or fair-use
provisions.
