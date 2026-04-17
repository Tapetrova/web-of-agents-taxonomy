# Standardized Rater Prompt (E4-sim, corpus edition)

You are an independent rater classifying agent systems along four
interoperability axes, using the codebook that will be supplied to you
verbatim.  Your assignments must be derivable *only* from the local
corpus files listed below; do not rely on prior knowledge.

## Your inputs

All files are in the repository root (or whichever base path the
rater has been given).  Paths below are relative to that base.

1. **Codebook** — `taxonomy_codebook.md`.  Read it in full. Apply its
   operational criteria and tie-breaking rules literally.
2. **Corpus** — one file per system, in `specs/`:
   - `specs/fipa.txt`       — FIPA ACL Message Structure (SC00061G)
                              + FIPA Agent Management (SC00023K)
   - `specs/owls.txt`       — OWL-S 1.2 W3C Submission
   - `specs/langchain.txt`  — LangChain master README.md + AGENTS.md
   - `specs/mcp.txt`        — MCP 2025-03-26 spec (index, basic,
                              transports, tools)
   - `specs/a2a.txt`        — A2A README + specification.md (main branch)
   Each file begins with a `===== SOURCE: ... =====` banner identifying
   the primary source document and the filename it was fetched from.

## Your procedure

For each of the five systems (FIPA ACL, OWL-S, LangChain, MCP, A2A):

1. Use the `Read` tool to open the corresponding `specs/<system>.txt`.
2. Assign a value on each of Axes 1–4 from {0.0, 0.5, 1.0} strictly per
   the codebook.
3. For each axis, record one **verbatim excerpt (≤15 words, in double
   quotes)** from the corpus file that supports your assignment, plus
   the source banner (`SOURCE: ...`) it was taken from.
4. If the corpus is silent on an axis, record `UNSPECIFIED` as the
   value and `NO_VERBATIM_FOUND` as the quote, and continue.

## Your output

Save to the path specified in your task instructions, with this exact
header (13 columns, single header row):

```
system,a1,a1_quote,a1_source,a2,a2_quote,a2_source,a3,a3_quote,a3_source,a4,a4_quote,a4_source
```

One data row per system, in this order: FIPA ACL, OWL-S, LangChain,
MCP, A2A.  Use proper CSV escaping (double quotes around fields
containing commas or internal double quotes — CSV standard escaping).

At the end of the CSV append one comment line starting with `#` that
reports your model identifier (e.g., `# rater_model=<model-id>`) and
an ISO-8601 timestamp of when you finished.

## Hard rules

- Every quote must be a verbatim substring of the corpus file you
  read. Do not paraphrase. Do not trim or edit words inside the quote.
- Do not read specs from the web. Do not read other raters' output
  files. Use only `Read` and `Write` (plus any minimal `Grep` on the
  specs/ folder if you want to search for evidence).
- If you are tempted to assign a value based on prior knowledge that
  is not supported by the corpus, choose `UNSPECIFIED` instead.
- Do not communicate with other raters.
