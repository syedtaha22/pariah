# Selection criteria

These criteria decide which papers enter the taxonomy.

## Scope

The taxonomy covers learning-based intrusion detectors that use graph-structured data, with a
graph neural network (GNN), a graph Transformer, or a hybrid of the two. Two domains are in scope, and each paper is
marked in the `domain` column:

| Domain | Graph | Data source |
| --- | --- | --- |
| Network | Hosts, flows, traffic records or feature patches as nodes; connections, flows or similarity links between them as edges | Traffic captures, NetFlow |
| Provenance | System entities (processes, files, sockets) as nodes, system events as edges | Operating system audit logs |

## Date range

Papers published from **1 January 2017** to **29 September 2026**, the search date. The
Transformer dates from 2017, so no GNN-Transformer hybrid can predate it. The widely used GNN
architectures that intrusion detectors build on appeared from 2017 onward: the graph convolutional
network (2017), GraphSAGE (2017) and the graph attention network (2018).

## Venue

Venue rank is not an inclusion criterion. Peer-reviewed papers from any venue are eligible, and
preprints are not. The `venue` column records where each paper appeared.

## Sources

| Source | Use |
| --- | --- |
| IEEE Xplore | Journals and conferences (S&P, TIFS, TDSC, ...) |
| ACM Digital Library | CCS, KDD, and ACM journals |
| USENIX and NDSS proceedings | USENIX Security, NDSS |
| Proceedings of NeurIPS, ICML and ICLR | ML venues |
| Google Scholar | Broad search and citation tracking. Preprint results are ignored. |
| DBLP | Venue-level checks |

Citation chasing (backward through references and forward through citing papers) starts from the
seed papers already in [references.bib](../paper/references.bib) that fall within scope.

## Search terms

Queries combine one term from each group. Exact strings, the source they were run on and the date
are recorded in the search log.

| Group | Terms |
| --- | --- |
| Model | "graph neural network", "GNN", "graph convolutional", "graph attention", "graph transformer", "transformer", "self-attention" |
| Task | "intrusion detection", "NIDS", "anomaly detection", "attack detection", "threat detection" |
| Data | "network traffic", "NetFlow", "flow", "provenance graph", "audit log", "APT" |

## Inclusion criteria

A paper is included if it meets all of these:

1. It proposes or evaluates a learning-based intrusion detector.
2. The detector takes graph-structured data as input and uses a GNN, a graph Transformer, or a
   hybrid of the two.
3. It targets network traffic or host provenance.
4. It is peer-reviewed, published in a journal or in conference or workshop proceedings.
5. It was published between 1 January 2017 and 29 September 2026.
6. It is written in English.
7. Its full text is accessible.

A paper that evaluates several detectors qualifies if at least one evaluated detector meets the
criterion.

## Exclusion criteria

A paper is excluded if any of these apply:

1. Graphs are used only for visualization or analysis, not as model input.
2. The Transformer works on flat features or sequences, with no graph-structured input.
3. It is an abstract, poster or extended abstract with no evaluation.
4. It is an earlier version of another included paper, or a different publication of the same
   work. The most complete version is kept.
5. It addresses a different task with no intrusion detection component, such as malware
   classification, fraud detection, provenance capture, forensic tooling, recommendation, attacks
   on models or studies of analysts.
6. It is a general GNN, Transformer or machine learning method, benchmark, library or theory with
   no security data or security evaluation.
7. It is a survey, systematization, taxonomy or position paper that proposes no detector. Such
   papers are used as references and are not annotated.

## Recording the reason

Every excluded paper gets one reason code in the sheet. `I1` to `I7` mean the paper fails
inclusion criterion 1 to 7. `E1` to `E7` mean exclusion criterion 1 to 7 applies.

The code should be the first row of this table that applies to the paper:

| Order | Code | The paper is excluded with this code when |
| --- | --- | --- |
| 1 | `E7` | It is a survey, systematization, taxonomy or position paper that proposes no detector. |
| 2 | `E6` | It is a general method, benchmark, library or theory with no security data. |
| 3 | `E5` | It addresses a security different task with no intrusion detection component. |
| 4 | `I1` | It is an intrusion detector that is not learning-based. |
| 5 | `E1` | It is a learning-based detector that uses graphs only for visualization or analysis. |
| 6 | `E2` | It is a learning-based detector whose Transformer has no graph-structured input. |
| 7 | `I2` | It is a learning-based detector with no graph input, or with graph input but no GNN, graph Transformer or hybrid. |
| 8 | `I3` | It is a detector for data other than network traffic or host provenance. |
| 9 | `E3` | It is an abstract, poster or extended abstract with no evaluation. |
| 10 | `I4` | It is not peer reviewed. |
| 11 | `I5` | It was published outside the date range. |
| 12 | `I6` | It is not written in English. |
| 13 | `I7` | Its full text is not accessible. |
| 14 | `E4` | It is an earlier version of another included paper, or a different publication of the same work. |

Orders 1 to 3 decide whether the paper is about intrusion detection at all. A paper that fails
them gets an `E` code, because it is not an intrusion detector to be tested against inclusion
criterion 1.

## Screening stages

1. **Identification.** Run the searches and citation chasing. Record the number of results per
   source.
2. **Deduplication.** Remove duplicates across sources.
3. **Title and abstract screening.** Apply the inclusion and exclusion criteria. Papers that
   cannot be decided move on to the next stage.
4. **Full-text screening.** Apply the criteria to the full text. Record the reason for every
   exclusion using the reason codes above.
5. **Inclusion.** Papers that pass are added to the `annotation` tab of the sheet, each
   with a `citation_key` in [references.bib](../paper/references.bib).
