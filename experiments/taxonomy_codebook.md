# Web-of-Agents Taxonomy Codebook (v1.0)

Supplementary material for "A Functional Taxonomy of the Web of Agents:
Operational Definitions and an Empirical Validation Protocol".

This codebook specifies the observable criteria used by coders to assign
each system under study a value on each of the four taxonomy axes.
It is designed so that two independent raters, given only the system's
public documentation (specification, README, reference implementation),
can assign the same axis value in ≥70% of cases (target
Krippendorff's α ≥ 0.70).

Each axis has three ordered levels, mapped to positions
{0.0, 0.5, 1.0} on the structured ↔ flexible spectrum used in Figure 2.

--------------------------------------------------------------------
## Axis 1 — Semantic Foundation

**Question the coder answers:** *Where is the shared meaning of a
message or capability represented at exchange time?*

| Value | Label | Observable criterion (coder must find ≥2 of 3) |
|-------|-------|------------------------------------------------|
| 0.0 | Formal / Explicit | (a) Spec references RDF, OWL, SHACL, SKOS, or comparable formal ontology language; (b) a schema file (.rdf/.owl/.ttl/.shacl) is part of the reference deployment; (c) the spec's "conformance" section requires consumers to validate against that schema. |
| 0.5 | Procedural | (a) Messages carry a "performative", "intent", "act", or "speech-act" field with a fixed enumerated vocabulary; (b) the spec defines semantics via pre-/post-conditions on those fields rather than via data schemas; (c) interoperability requires agreement on the act vocabulary but not on domain ontologies. |
| 1.0 | Implicit / Emergent | (a) Capabilities are described in unstructured or semi-structured natural language (e.g., tool descriptions, Agent Cards); (b) the spec does not mandate a shared ontology; (c) a language model is expected to interpret the descriptions at call time. |

**Tie-breaking rules.**

- If a system has formal schemas *and* natural-language tool
  descriptions (typical for LLM-era protocols), score 1.0 unless the
  schemas are required for operation (not merely informative).
- Hybrid "JSON Schema + natural-language description" systems map to
  1.0; JSON Schema is structural, not semantic.
- "Typed tool parameters" are Axis-1 1.0 so long as the type system is
  structural (TypeScript-like) and not ontological.

**Worked examples.**

- JADE / FIPA-ACL → 0.5 (performatives: inform, request, cfp, …).
- OWL-S service description → 0.0 (requires OWL classes).
- MCP tool with JSON-Schema params + NL description → 1.0.
- A2A Agent Card (skills in NL, optional JSON examples) → 1.0.

--------------------------------------------------------------------
## Axis 2 — Communication Paradigm

**Question:** *What is the primary abstraction of a message?*

| Value | Label | Observable criterion |
|-------|-------|----------------------|
| 0.0 | Performative | Messages are speech acts with explicit illocutionary force; the spec defines a finite vocabulary of performatives and their interaction protocols. |
| 0.5 | Resource-oriented | Interactions are modelled as operations on URI-identified resources (GET/PUT/POST/DELETE or SPARQL CRUD); hypermedia links in responses drive state transitions (HATEOAS). |
| 1.0 | RPC-style | Messages are named procedure invocations with typed arguments; the canonical wire formats are JSON-RPC 2.0, gRPC, or equivalent; no hypermedia. |

**Tie-breaking.**

- A spec that uses HTTP verbs but conveys RPC-style action names in
  the body (e.g., `POST /tools/invoke {"method":"x"}`) scores 1.0.
- Streaming transports (SSE, WebSocket) do not by themselves change
  the paradigm; classify by the unit of exchange.

**Worked examples.**

- FIPA ACL over HTTP → 0.0.
- REST/HATEOAS service described by OWL-S → 0.5.
- MCP (JSON-RPC) → 1.0. A2A v0.3 (JSON-RPC + streaming) → 1.0.

--------------------------------------------------------------------
## Axis 3 — Locus of Intelligence

**Question:** *Which component of the system performs non-trivial
inference at task-execution time?*

| Value | Label | Observable criterion |
|-------|-------|----------------------|
| 0.0 | Data | Reasoning is performed by applying domain ontologies and rule bases over RDF triples or similar; the agent executable is a thin query engine. |
| 0.5 | Platform | The middleware provides coordination services (directory facilitators, interaction protocols, matchmakers) that encode domain-agnostic reasoning; individual agents are procedural. |
| 1.0 | Agent / Model | A language model within the agent performs open-ended reasoning over natural-language inputs; the protocol layer carries data but not reasoning. |

**Tie-breaking.**

- RAG pipelines still score 1.0 on Axis 3: the model does the reasoning,
  the retrieval system supplies context.
- Systems that invoke an external LLM via a tool call (e.g., a JADE
  agent that delegates to a frontier LLM) score 1.0 when the LLM
  decides actions, else 0.5.

**Worked examples.**

- OWL-S + SPARQL endpoints → 0.0.
- JADE with Contract-Net protocol → 0.5.
- MCP client backed by a frontier LLM with no external KB → 1.0.

--------------------------------------------------------------------
## Axis 4 — Discovery Mechanism

**Question:** *How does one agent locate a peer that provides a
required capability?*

| Value | Label | Observable criterion |
|-------|-------|----------------------|
| 0.0 | Centralized registry | A single administrative authority operates a service that must be queried for capability lookup (FIPA DF, UDDI, a canonical MCP registry). |
| 0.5 | Standardized metadata | Capability descriptors live at well-known URLs on the provider itself (e.g., `/.well-known/agent.json`) and are discovered by convention rather than through a central index. |
| 1.0 | Decentralized / networked | Discovery is mediated by a peer-to-peer substrate (DIDs, DHT, gossip) with no single authoritative registry. |

**Tie-breaking.**

- A system that offers *both* a well-known file and an optional central
  registry scores 0.5 if the well-known file is authoritative, else 0.0.
- "GitHub search" and similar general-purpose indexers do not count as
  discovery mechanisms.

**Worked examples.**

- FIPA DF / UDDI → 0.0.
- A2A Agent Cards at `/.well-known/agent.json` → 0.5.
- MCP with central `registry.modelcontextprotocol.io` → 0.0.
  (Classify by the default path, not by optional alternatives.)
- ANP with DID-based peer discovery → 1.0.

--------------------------------------------------------------------
## Coherence score

For each system S with axis values (a1, a2, a3, a4) ∈ [0,1]^4:

    coherence(S) = 1 − 2 · std_dev(a1, a2, a3, a4)

Coherence = 1 when all axes agree; coherence ≈ 0 for a zigzag profile.
The axis-coherence hypothesis (H2) states that log-adoption covaries
positively with coherence after controlling for generation and domain.

--------------------------------------------------------------------
## Coding procedure

1. Each coder receives (i) the canonical specification URL, (ii) one
   reference implementation repository, (iii) this codebook. No access
   to the paper under review.
2. Coder fills a row in the CSV template
   (`system, a1, a2, a3, a4, a1_evidence, … , a4_evidence`) where each
   evidence field is a ≤50-word quote or file path supporting the value.
3. Disagreements are resolved by consensus meeting after independent
   coding; pre-consensus values feed the Krippendorff's α calculation.

## Change log

v1.0 — initial release accompanying the pilot study of 5 systems.
