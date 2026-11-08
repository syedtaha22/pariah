> [!NOTE]  
> This file was written by Claude Sonnet 5.5. The steps were validated by [Syed Taha](https://github.com/syedtaha22)

# Reproduction changelog

This file records everything done in a checkout of the upstream repository to run Flash: the steps, and every
deviation from the upstream instructions. Commands run from the root of the upstream checkout made under Steps.

## Upstream

- Repository: https://github.com/DART-Laboratory/Flash-IDS (cloned 2026-11-07)
- Commit: ccbafee7eb796c76aceaabdc259ebd1f12b867cc (2024-05-15)
- Patches: `experiments/reproduction/NK-001_rehman2024flash/` holds `run.patch` and one patch per modified notebook
  (`Cadets.patch`, `Trace.patch`, `Theia.patch`, `Fivedirections.patch`, `OpTC.patch`, `streamspot.patch`).

## Machine

- OS: Ubuntu 24.04.4 LTS
- Processor: Intel Core i9-13900HX
- RAM: 15 GiB
- GPU: NVIDIA GeForce RTX 4060 (8 GiB)

## Steps

Get the upstream code at the commit named above. Every later command runs from the root of the upstream checkout,
`Flash-IDS/`:

```bash
git clone https://github.com/DART-Laboratory/Flash-IDS.git
cd Flash-IDS
git checkout ccbafee7eb796c76aceaabdc259ebd1f12b867cc
```

1. Create the environment and install the dependencies:

   ```bash
   uv venv --python 3.10 .venv
   uv pip install --python .venv/bin/python -r requirements.txt \
     -f https://download.pytorch.org/whl/torch_stable.html \
     -f https://data.pyg.org/whl/torch-1.12.0+cu113.html
   uv pip install --python .venv/bin/python scipy==1.10.1 \
     nvidia-cusparse-cu11 nvidia-cusolver-cu11 nvidia-curand-cu11 \
     orjson gdown==5.2.0 matplotlib jupyter ipykernel
   ```

   - Python 3.10: the README names no version, and torch 1.12.0 has wheels up to 3.10.
   - Two `-f` indexes: `pip install -r requirements.txt` as written fails with `No solution found when resolving
     dependencies: Because there is no version of torch==1.12.0+cu113 and you require torch==1.12.0+cu113`. The
     `+cu113` and `+pt112cu113` builds are not on PyPI and the README names no index. The PyTorch stable index serves
     torch. The PyG index for torch 1.12.0 with CUDA 11.3 serves torch-cluster, torch-sparse and torch-spline-conv.
     `torch-scatter==2.0.9` is built from source, since the PyG indexes only list 2.1.0.
   - Unpinned packages: `requirements.txt` does not pin all transitive packages. The resolver chose, among others,
     requests 2.34.2 and urllib3 2.8.0.
   - `scipy==1.10.1`: `import gensim` fails with scipy 1.13.1 (`ImportError: cannot import name 'triu' from
     'scipy.linalg'`). scipy 1.13 removed `scipy.linalg.triu`, and gensim 4.3.0 imports it.
   - `nvidia-cusparse-cu11`, `nvidia-cusolver-cu11`, `nvidia-curand-cu11`: `import torch_sparse` fails with `OSError:
     libcusparse.so.11: cannot open shared object file`. The torch 1.12.0+cu113 wheel does not ship cusparse. These
     packages supply the CUDA 11 libraries, and the process needs their folders on `LD_LIBRARY_PATH`.
   - `orjson`, `gdown`, `matplotlib`: the notebooks import them and `requirements.txt` lacks them. `jupyter`,
     `ipykernel`: the README lists Jupyter as a prerequisite.
   - `gdown==5.2.0`: the download cells call `gdown.download(url, quiet=False, use_cookies=False, fuzzy=True)`, gdown
     6.x removed `fuzzy`, and `requirements.txt` does not pin gdown.

2. Add the script that runs a notebook as a memory-limited service, with its cell-by-cell runner ([Deviation 1][d1]).
   `$PARIAH` is a checkout of https://github.com/syedtaha22/pariah, and `$DATA` is a folder that holds the files
   downloaded in a browser in the steps below:

   ```bash
   export PARIAH=/path/to/pariah
   export FILES=$PARIAH/experiments/reproduction/NK-001_rehman2024flash
   export DATA=/path/to/the/folder/with/the/downloaded/files
   git apply $FILES/run.patch
   ```

3. Cadets ([Deviation 2][d2]). The archives come from the links in the download cell of `Cadets.ipynb`:

   ```bash
   cp -v $DATA/{ta1-cadets-e3-official,ta1-cadets-e3-official-2}.json.tar.gz .
   git apply $FILES/Cadets.patch
   ./run.sh Cadets.ipynb
   ```

4. Trace ([Deviation 3][d3]). The archive comes from the link in the download cell of `Trace.ipynb`:

   ```bash
   cp -v $DATA/ta1-trace-e3-official-1.json.tar.gz .
   git apply $FILES/Trace.patch
   ./run.sh Trace.ipynb
   ```

5. Theia ([Deviation 4][d4]). The archives come from the links in the download cell of `Theia.ipynb`:

   ```bash
   cp -v $DATA/{ta1-theia-e3-official-1r,ta1-theia-e3-official-6r}.json.tar.gz .
   git apply $FILES/Theia.patch
   ./run.sh Theia.ipynb
   ```

6. FiveDirections ([Deviation 5][d5]). The archive comes from the link in the download cell of
   `Fivedirections.ipynb`:

   ```bash
   cp -v $DATA/ta1-fivedirections-e3-official-2.json.tar.gz .
   git apply $FILES/Fivedirections.patch
   ./run.sh Fivedirections.ipynb
   ```

7. OpTC ([Deviation 6][d6]). The files come from the links in the download cell of `OpTC.ipynb`:

   ```bash
   cp -v $DATA/AIA-*.json.gz $DATA/optc.txt $DATA/w2v_optc.model .
   git apply $FILES/OpTC.patch
   ./run.sh OpTC.ipynb
   ```

8. StreamSpot ([Deviation 7][d7]):

   ```bash
   wget https://github.com/sbustreamspot/sbustreamspot-data/raw/07942da41ae3ba7202b146c758fcf0c30d2cb7b6/all.tar.gz
   git apply $FILES/streamspot.patch
   ./run.sh streamspot.ipynb
   ```

9. Unicorn. The notebook downloads its own data:

   ```bash
   ./run.sh unicorn.ipynb
   ```

## Added files

| Path | What |
| --- | --- |
| `.venv/` | Python 3.10 virtual environment |
| `ta1-cadets-e3-official.json.tar.gz`, `ta1-cadets-e3-official-2.json.tar.gz` | Cadets archives ([Deviation 2][d2]) |
| `ta1-trace-e3-official-1.json.tar.gz` | Trace archive ([Deviation 3][d3]) |
| `ta1-theia-e3-official-1r.json.tar.gz`, `ta1-theia-e3-official-6r.json.tar.gz` | Theia archives ([Deviation 4][d4]) |
| `ta1-fivedirections-e3-official-2.json.tar.gz` | FiveDirections archive ([Deviation 5][d5]) |
| `AIA-*.json.gz`, `optc.txt`, `w2v_optc.model` | OpTC data ([Deviation 6][d6]) |
| `all.tar.gz` | StreamSpot data |
| `run.sh` | Starts a notebook as a memory-limited service ([Deviation 1][d1]) |
| `run_notebook.py` | Cell-by-cell runner ([Deviation 1][d1]) |

## Results

All runs use the pre-trained weights and no training. Each notebook ran with `./run.sh` ([Deviation 1][d1]) on
2026-11-07. All seven notebooks ran to the end. Durations and peak memory are those printed by the runner.

### Cadets (`Cadets.ipynb`)

All cells ran in 547 s, peak 5.8 GB ([Deviation 2][d2]).

| | Precision | Recall | F-score | TP | FP | FN |
| --- | --- | --- | --- | --- | --- | --- |
| Paper, Table 2, FLASH (GNN), Cadets (E3) | 0.94 | 0.99 | 0.96 | 12851 | 818 | 1 |
| This run | 0.93 | 1.0 | 0.96 | 12851 | 1003 | 7 |

The true positives match. The false positives and false negatives differ, and the cause was not
determined. The notebook does not print the true negatives.

### Trace (`Trace.ipynb`)

All cells ran in 1145 s, peak 5.0 GB ([Deviation 3][d3]).

| | Precision | Recall | F-score | TP | FP | FN |
| --- | --- | --- | --- | --- | --- | --- |
| Paper, Table 2, FLASH (GNN), Trace (E3) | 0.95 | 0.99 | 0.97 | 67382 | 3477 | 1 |
| This run | 0.95 | 0.99 | 0.97 | 67383 | 3477 | 790 |

Precision, recall and F-score match at the printed precision, and FP is identical. TP differs by
one and FN is 790 against 1. The cause was not determined. The notebook does not print the true
negatives.

### Theia (`Theia.ipynb`)

All cells ran in 2119 s, peak 5.8 GB ([Deviation 4][d4]).

| | Precision | Recall | F-score | TP | FP | FN |
| --- | --- | --- | --- | --- | --- | --- |
| Paper, Table 2, FLASH (GNN), Theia (E3) | 0.92 | 0.99 | 0.95 | 25318 | 2282 | 44 |
| This run | 0.92 | 1.0 | 0.96 | 25318 | 2273 | 41 |

TP is identical, FP is 9 lower and FN is 3 lower. The notebook prints recall as 1.0 and F-score as
0.96 where the paper's table shows 0.99 and 0.95 for these counts (25318/25359 = 0.9984 and F =
0.956), which looks like truncation against rounding. The notebook does not print the true negatives.

### FiveDirections (`Fivedirections.ipynb`)

All cells ran in 1259 s, peak 6.1 GB ([Deviation 5][d5]). The streaming pass reported `streamed 53 members, 7253145
nodes, 0 conflicting node types`.

| | Precision | Recall | F-score | TP | FP | FN |
| --- | --- | --- | --- | --- | --- | --- |
| Paper, Table 2, FLASH (GNN), Fivedirections (E3) | 0.72 | 0.93 | 0.81 | 395 | 150 | 30 |
| This run | 0.72 | 0.93 | 0.81 | 395 | 150 | 30 |

All printed values are identical. The notebook does not print the true negatives.

### OpTC (`OpTC.ipynb`)

All cells ran in 305 s, peak 4.2 GB ([Deviation 6][d6]). This notebook uses the decoupled pipeline (stored GNN
embeddings and the XGBoost classifier), so it corresponds to the "FLASH (GNN + XGBoost)" columns of Table 2. It prints
precision, recall and F-score only, not the counts.

| Notebook section (host) | Notebook result (P / R / F) | Paper, Table 2, FLASH (GNN + XGBoost) | Paper TP / FP / FN |
| --- | --- | --- | --- |
| Plain PowerShell Empire Attack (201) | 0.81 / 0.95 / 0.87 | Attack 1: 0.90 / 0.92 / 0.91 | 57 / 6 / 5 |
| Custom PowerShell Empire Attack (501) | 0.94 / 0.92 / 0.93 | Attack 2: 0.94 / 0.92 / 0.93 | 378 / 22 / 32 |
| Malicious Upgrade Attack (051) | 0.93 / 0.92 / 0.93 | Attack 3: 0.92 / 0.93 / 0.92 | 165 / 15 / 13 |

Only one row of this mapping comes from the paper: Appendix C describes Attack 3 as the malicious
software update (Notepad++ backdoor), which is the notebook's Malicious Upgrade section, and Attack 1
as PowerShell Empire staging. The paper says the second attack is explained in Section 2 and does not
name the two PowerShell Empire scenarios, so the other two rows follow the chronological order of the
OpTC attack days and the printed numbers, and should be read as inferred. On that mapping the Malicious
Upgrade and Custom PowerShell Empire results are close to or equal to the paper at the printed
precision, and the Plain PowerShell Empire result is lower (precision 0.81 against 0.90, F-score 0.87
against 0.91); the cause was not determined.

### StreamSpot (`streamspot.ipynb`)

All cells ran in 2175 s, peak 2.1 GB ([Deviation 7][d7]).

| | Precision | Recall | F-score | TP | FP | FN | TN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Paper, Table 3, FLASH, StreamSpot | 1.0 | 0.96 | 0.98 | | | | |
| This run | 1.0 | 0.95 | 0.974 | 95 | 0 | 5 | 150 |

Precision is identical. Recall is 95 of 100 attack graphs against the paper's 0.96, which is one
graph fewer, so the F-score is 0.974 against 0.98. The notebook evaluates 100 attack and 150 benign
graphs.

### Unicorn (`unicorn.ipynb`)

All cells ran in 801 s, peak 1.7 GB. The notebook downloaded its own data with its unchanged gdown cell
(`unicorn.zip`, 97.6 MB).

| | Precision | Recall | F-score | TP | FP | FN | TN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Paper, Table 3, FLASH, Unicorn SC-1 | 0.92 | 0.96 | 0.94 | | | | |
| Paper, Table 3, FLASH, Unicorn SC-2 | 0.96 | 0.96 | 0.96 | | | | |
| This run | 0.96 | 0.96 | 0.96 | 24 | 1 | 1 | 24 |

The result equals the SC-2 row and differs from the SC-1 row. The notebook does not state which
scenario it evaluates, only that its data comes from https://github.com/margoseltzer/shellshock-apt,
so which row it corresponds to was not established.

## Deviations

### 1. Runner (`run.patch`)

**Problem:** A notebook run inside the editor's process group exhausts the memory of the machine, and the kernel
out-of-memory handler kills the editor together with the notebook.

**Change:** `run.sh` starts the notebook in its own memory-limited systemd user service and `run_notebook.py` executes the
cells, so only the notebook process is killed at the limit. Command: `./run.sh <notebook>.ipynb`

### 2. Cadets (`Cadets.patch`)

| Id | Problem | Change |
| --- | --- | --- |
| 2.1 | Cell 3 (download): Google Drive refuses both files with gdown (`Too many users have viewed or downloaded this file recently`). | Lines 61 to 65 are commented out. The archives were downloaded in a browser from the same links and placed in the root of the checkout ([Checksums][sha]). |
| 2.2 | Cell 14 (`add_attributes`): the kernel out-of-memory handler kills the Python process at 7.9 GB resident. The function parses every EVENT line of a 3 to 4 GB file into Python dicts at once (`data = [json.loads(x) for x in f if "EVENT" in x]`) and merges them with the edge table in one step. | The function reads the file line by line and merges every 250000 EVENT lines with the edge table (new optional argument `chunk_events=250000`). Duplicate rows are removed from the edge table once and from each event chunk and merged chunk, because the merge multiplies every repeated (actor, object, action, timestamp) row by each matching event (a 250000-row chunk expanded to 1.8 million merged rows). The chunks are concatenated in the original row order, and the upstream final `drop_duplicates()` stays. |

### 3. Trace (`Trace.patch`)

| Id | Problem | Change |
| --- | --- | --- |
| 3.1 | Cell 3 (download): Google Drive refuses the file with gdown, as in [2.1][d2]. | Lines 61 to 65 are commented out. The archive was downloaded in a browser from the same link and placed in the root of the checkout ([Checksums][sha]). |
| 3.2 | Cell 14 (`add_attributes`): the memory limit is reached, for the reason in [2.2][d2]. | The `add_attributes` of [2.2][d2]. |

### 4. Theia (`Theia.patch`)

| Id | Problem | Change |
| --- | --- | --- |
| 4.1 | Cell 3 (download): Google Drive refuses both files with gdown, as in [2.1][d2]. | Lines 61 to 65 are commented out. The archives were downloaded in a browser from the same links and placed in the root of the checkout ([Checksums][sha]). |
| 4.2 | Cell 14 (`add_attributes`): the memory limit is reached, for the reason in [2.2][d2]. | The `add_attributes` of [2.2][d2]. Theia's function reads `cmdLine` where the others read `exec`. |
| 4.3 | Cell 21 (edge-list loading): the cell reads the whole edge list into a list of lists before building the DataFrame (`f.read().split('\n')`, then `[line.split('\t') ...]`). For the 9.4 million rows of the test list this needs about three times the memory of the table, and the memory limit kills the run 10 seconds into the cell. | The file is read with `pandas.read_csv`, the five repeated columns as categories converted back to ordinary object columns that share their strings, and sorted on the same timestamp column, so ties are ordered as before. The original lines are kept as comments. |
| 4.4 | Cell 23: the notebook enters the evaluation cell with 4.1 GB in use, and the memory limit kills it there. | The end of the cell deletes `df`, `data` and `phrases` and calls `gc.collect()`. No later cell uses them. |

### 5. FiveDirections (`Fivedirections.patch`)

| Id | Problem | Change |
| --- | --- | --- |
| 5.1 | Cell 3 (download): Google Drive refuses the file with gdown, as in [2.1][d2]. | Lines 61 to 65 are commented out. The archive was downloaded in a browser from the same link and placed in the root of the checkout ([Checksums][sha]). |
| 5.2 | Cell 15 (`add_attributes`): the memory limit is reached, for the reason in [2.2][d2]. | The `add_attributes` of [2.2][d2]. |
| 5.3 | Cell 6 (extraction): the archive (12.4 GB compressed) holds 53 files that total 213.5 GB, the largest 4.26 GB, and the notebook extracts all of them with `tar` before processing. With 175 GB free it fails with `OSError: [Errno 28] No space left on device` during `process_edges`. The full extraction plus the generated edge lists need about 240 GB. | `run_data_processing()` calls a new function `stream_process`, and the original `tar`, `process_data` and `process_edges` lines are kept as comments. `stream_process` reads the archive as a stream, writes one member at a time under the notebook's base file name, runs the notebook's own `process_data` on it and deletes it. It merges the per-member node-type maps in archive order and prints the number of conflicting node types (the upstream function merges in numeric order). A second pass runs the notebook's own `process_edges` only for `ta1-fivedirections-e3-official-2.json` (train) and `ta1-fivedirections-e3-official-2.json.23` (test), the two edge lists that later cells read. The raw test member `.23` stays in the root of the checkout (the `keep` argument), because `add_attributes` reads it again. |

### 6. OpTC (`OpTC.patch`)

| Id | Problem | Change |
| --- | --- | --- |
| 6.1 | Cell 7 (download): Google Drive refuses the files with gdown, as in [2.1][d2]. | The `urls` list and the `for url in urls` download loop (12 lines) are commented out, and the log extraction below them is unchanged. The seven files were downloaded in a browser from the links in the cell and placed in the root of the checkout ([Checksums][sha]). The downloaded `optc.txt` is not the same file as `data_files/optc.txt` in the repository, and the notebook reads it from the root of the checkout. |
| 6.2 | Cells 33, 35 and 37 (event loading): `load_events_from_hosts` loads every event of a host into a list of Python dicts. The memory limit kills the run in the second evaluation cell (host 201, an 834 MB file), after the first one (host 051, 626 MB) used 6.2 GB. The host 501 file is 2.4 GB. | New function `load_events_from_hosts_lean` (cell 29), called from cells 33, 35 and 37 with the original lines kept as comments. It reads the file line by line, reduces every event to the fields that the later cells use, applies the notebook's own `Extract_Semantic_Info` and `is_valid_entry` and the `Traversal_Rules` de-duplication key while reading, and keeps the set of all actor and object ids separately, because `EntitySet` is built from every event. |

### 7. StreamSpot (`streamspot.patch`)

**Problem:** The notebook fails in cell 17 with `FileNotFoundError: streamspot/400.txt`. No cell calls `parse_data()` (it
is only defined in cell 5), nothing creates the `streamspot/` directory, and `parse_data()` writes
`streamspot/{scene}/{graph}.txt` while the evaluation cells read `streamspot/{graph}.txt`.

**Change:** Cell 5: the three lines that create the per-scene directory and open `streamspot/{scene}/{graph}.txt` are kept
as comments, and the file is opened as `streamspot/{graph}.txt`. A new cell after cell 9 (where `time`, which
`parse_data()` uses, is imported) creates `streamspot/` and calls `parse_data()`.

## Checksums

The authors publish no checksums. The files downloaded in a browser ([Deviation 2][d2] to [Deviation 6][d6]):

| File | Size (bytes) | SHA-256 |
| --- | --- | --- |
| `ta1-cadets-e3-official.json.tar.gz` | 585737522 | `e2a81cb467a3097ba09ebea60db47b2250bd2bb9413b562ed397a41fc871911e` |
| `ta1-cadets-e3-official-2.json.tar.gz` | 358244121 | `8d2f090d372cfb0d21bfb72dba6824884ce7870b5c8d24df34e9081b9b09c793` |
| `ta1-trace-e3-official-1.json.tar.gz` | 1281892428 | `9f814e138582b7fc2ba9edfcff492250a814f3da719c45e0508cee61834dfff7` |
| `ta1-theia-e3-official-1r.json.tar.gz` | 1167693020 | `1645eb83e4796f31fea1bb75f266f51168466fb7af975abe5ef169384fbe0d9c` |
| `ta1-theia-e3-official-6r.json.tar.gz` | 1546028723 | `3384d1a62a71b1a3de43004d60e990881b3d1dc87fa9e7cf8938bc850300cc9c` |
| `ta1-fivedirections-e3-official-2.json.tar.gz` | 12393279673 | `245a35c12a8557a3bdbbe2187e40629a12b4b4f8d99368271721b02d3a9b5e2f` |
| `AIA-201-225.ecar-2019-12-08T11-05-10.046.json.gz` | 109692169 | `4b1e6000b5442597076c3ee22ca014c4c3b9398bb9113310ca1a8d1e492b6de3` |
| `AIA-201-225.ecar-last.json.gz` | 2217842713 | `faf181cbf7e4f00f9c912da3ec2d7bc19667e0249ce7a297d0d2a7be9bee5fd7` |
| `AIA-501-525.ecar-2019-11-17T04-01-58.625.json.gz` | 1800808230 | `6dfdc4830b5c9cebc1e3a2830629c50fa019722591b7775f5a51794e2634aaf7` |
| `AIA-501-525.ecar-last.json.gz` | 4012042204 | `5b809a9ef27fe9bb0237ae217fb8ba3815ff15653716187ec1e51b1334f9d3d2` |
| `AIA-51-75.ecar-last.json.gz` | 1444234333 | `6afd2056353f825efe9c083a887781068fe09dd134715dc34700353f21efd0b0` |
| `optc.txt` | 24160 | `84f50e1f82b199dd539ab5a950b63ba0022cf56ab3f42cbe1f61a88e4ee35dbf` |
| `w2v_optc.model` | 147330658 | `f7d1fc2ff9afa797ed9b58d2c20690a8bed3fe5161e1f99b095f7e81bf4d9581` |

[d1]: #1-runner-runpatch
[d2]: #2-cadets-cadetspatch
[d3]: #3-trace-tracepatch
[d4]: #4-theia-theiapatch
[d5]: #5-fivedirections-fivedirectionspatch
[d6]: #6-optc-optcpatch
[d7]: #7-streamspot-streamspotpatch
[sha]: #checksums
