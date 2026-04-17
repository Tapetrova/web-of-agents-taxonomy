# A Functional Taxonomy of the Web of Agents

<!-- Replace the Zenodo badge below once the webhook mints a DOI -->
[![DOI](https://zenodo.org/badge/DOI/PLACEHOLDER.svg)](https://doi.org/PLACEHOLDER)

Companion repository for the article

> **A Functional Taxonomy of the Web of Agents: Operational Definitions
> and an Empirical Validation Protocol.** Tatiana Petrova.

It contains the full LaTeX source and a compiled PDF of the article,
together with every artefact needed to reproduce the **E4a
LLM-self-consistency pilot** reported in Section V: the operational
codebook, the standardized rater prompt, the five-system local
specification corpus, three independent rater outputs, and a script
that recomputes pairwise agreement and Cohen's kappa.

## Repository layout

```
.
├── paper/
│   ├── ieee_is_v2.tex            Article source
│   ├── ieee_is_v2.pdf            Compiled article (14 pages)
│   ├── references.bib            Bibliography
│   ├── figures/                  Figures referenced by the article
│   │   ├── fig1_history.pdf
│   │   ├── fig2_taxonomy.pdf
│   │   └── fig3_sequence_car.pdf
│   ├── IEEEcsmag.cls             IEEE Computer Society magazine class
│   ├── IEEEtran.bst              IEEE Transactions BibTeX style
│   └── upmath.sty                Upright math package
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
│   └── compute_agreement.py      Reproduces every number in Section V
│
├── CITATION.cff                  Citation metadata (GitHub + Zenodo)
├── .zenodo.json                  Zenodo metadata override
├── LICENSE                       CC-BY-4.0 for article/data
├── LICENSE-CODE                  MIT for scripts
└── .gitignore                    LaTeX build-artefact exclusions
```

## Reproducing the E4a pilot

The pilot measures self-consistency of an LLM classifier applied to a
fixed corpus, under a codebook that supplies operational criteria for
each axis value. The exact raw outputs are archived, so three separate
reproduction levels are possible.

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
Supply the codebook (`experiments/taxonomy_codebook.md`) and prompt
(`experiments/standardized_prompt.md`) to three independent model
instances. Each instance reads only from `experiments/specs/` and
writes a rater CSV in the same schema. No web access is needed.

**3. Refresh the corpus from the primary sources.** Replace the files
in `experiments/specs/` with newer snapshots. Upstream URLs at the
time of the 2026-04 snapshot:

- FIPA SC00061G — `http://www.fipa.org/specs/fipa00061/SC00061G.html`
  (fetched via `archive.org` 2024 mirror)
- FIPA SC00023K — `http://www.fipa.org/specs/fipa00023/SC00023K.html`
  (fetched via `archive.org` 2024 mirror)
- OWL-S 1.2 — `https://www.w3.org/Submission/OWL-S/`
- LangChain — `github.com/langchain-ai/langchain` master: `README.md`
  and `AGENTS.md`
- MCP 2025-03-26 — `github.com/modelcontextprotocol/modelcontextprotocol`
  `docs/specification/2025-03-26/{index,basic/index,basic/transports,server/tools}.mdx`
- A2A — `github.com/a2aproject/A2A` main: `README.md` and
  `docs/specification.md`

Different snapshots will produce different assignments; that is
intentional and is the subject of Section V's discussion of corpus
sensitivity.

## Building the paper

```bash
cd paper
pdflatex ieee_is_v2
bibtex   ieee_is_v2
pdflatex ieee_is_v2
pdflatex ieee_is_v2
```

Requires a TeX Live installation with `IEEEcsmag`-compatible fonts
(Adobe Helvetica, Courier, Times). The class and the supporting
`IEEEtran.bst` and `upmath.sty` are vendored next to the source so
no additional packages beyond the base distribution are strictly
required.

## Pilot summary

Three independent LLM rater instances were given an identical codebook
and a locally archived corpus of five agent systems (FIPA ACL, OWL-S,
LangChain, MCP, A2A). Each rater produced a value in `{0.0, 0.5, 1.0,
UNSPECIFIED}` on each of four axes with a verbatim evidence excerpt
(≤15 words) from the corpus.

| Axis                      | Mean pct agree | Mean Cohen's kappa | Disagreements |
|---------------------------|---------------:|-------------------:|--------------:|
| Semantic Foundation (a1)  |          1.000 |              1.000 |             0 |
| Communication (a2)        |          0.867 |              0.815 |             1 |
| Locus of Intelligence (a3)|          0.867 |              0.804 |             1 |
| Discovery Mechanism (a4)  |          1.000 |              1.000 |             0 |

Both item-level disagreements occurred where one rater honestly chose
`UNSPECIFIED` against a terse corpus (OWL-S on a2; LangChain on a3)
and the others assigned a numeric value. The LangChain result
illustrates corpus sensitivity: all three raters flagged Axes 1, 2,
and 4 as `UNSPECIFIED` because the vendored corpus contains only the
repository-level `README.md` and `AGENTS.md` rather than the long-form
documentation site.

This is **not** a substitute for a human inter-rater-reliability
study. Three parallel LLM instances can share systematic biases that
kappa does not detect. See Section V for the full E1/E2/E4 protocol.

## Citing this artefact

Use the Zenodo DOI (link above once minted) for the archived snapshot
of this repository, or the `CITATION.cff` file below for citation
metadata.

```
Petrova, T. (2026). A Functional Taxonomy of the Web of Agents:
Operational Definitions and an Empirical Validation Protocol
(v1.0.0) [Paper and data]. Zenodo. https://doi.org/PLACEHOLDER
```

## Licence

- Article text, figures, and the experimental data (codebook,
  specifications corpus, rater outputs, derived tables) are released
  under **CC-BY-4.0** — see `LICENSE`.
- The reproducibility script in `scripts/` is released under **MIT** —
  see `LICENSE-CODE`.

The specification corpus in `experiments/specs/` reproduces short
excerpts from third-party documents (FIPA, W3C, OWL-S, MCP, A2A,
LangChain) that remain the property of their respective copyright
holders; they are included here for the sole purpose of
reproducibility and are used in accordance with each document's
licence or fair-use provisions.
