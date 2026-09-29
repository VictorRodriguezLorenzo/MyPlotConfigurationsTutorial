# 05 — Custom C++, `extended/`, reconstruction and machine learning

## Goal

Use code when a simple RDataFrame expression is no longer enough. This module is based on the extended dileptonic top+DM setup and includes examples of both lightweight helper functions and complete event reconstruction.

It covers:

- `macros/` loaded with `linesToAdd`;
- precompiled helpers in `extended/` loaded with `linesToProcess`/`gSystem.Load`;
- scalar-returning C++ functions;
- vector-returning producers such as `doubleNu_producer`;
- extracting many aliases from one expensive calculation;
- fake-rate and jet-veto helpers;
- DNN snapshot preparation, training and inference.

---

## 1. `macros/` versus `extended/`

This repositories can use two common patterns.

### Include source directly

```python
'linesToAdd': [f'#include "{analysisRoot}/macros/computeMT2.cc"']
```

ROOT's interpreter sees the C++ definition, and the alias calls the function in `expr`.

Good for self-contained helper functions and headers.

### Load compiled code / instantiate helper objects

```python
'linesToProcess': [
    'ROOT.gSystem.Load("..._cc.so", "", ROOT.kTRUE)',
    "ROOT.gInterpreter.ProcessLine('...')",
]
```

Useful when the helper has external dependencies, initialization state or calibration payloads.

The folder name is only convention; the actual behavior is controlled by how `aliases.py` loads the code.

---

## 2. A scalar macro: `computeMT2.cc`

The alias has two pieces:

```python
'linesToAdd': ['#include ".../computeMT2.cc"'],
'expr': 'computeMT2(...)',
```

`linesToAdd` makes the function known to ROOT; `expr` evaluates it event by event.

---

## 3. A vector producer: `doubleNu_producer`

Open:

```bash
less ../macros/doubleNu_producer.cc
less ../macros/doubleNu_producer.h
```

The expensive reconstruction is executed once and returns multiple values in a vector. `aliases.py` stores that vector in an intermediate alias and then exposes individual elements.

Pattern:

```python
aliases['doubleNu'] = {
    'linesToAdd': ['#include ".../doubleNu_producer.cc"'],
    'expr': 'doubleNu_producer(...)',
}

aliases['someObservable'] = {
    'expr': 'doubleNu[INDEX]',
}
```

This is preferable to running the same reconstruction independently for every observable.

Whenever you append outputs, document the index contract in one place and keep old indices stable when downstream code depends on them.

---

## 4. Compile the extended helpers

As explained before, always remember to compile the helpers before running.From `Full2022v12`:

```bash
cd ../extended
root -l -b -q 'evaluate_btagSFbc.cc++'
root -l -b -q 'evaluate_btagSFlight.cc++'
root -l -b -q 'fake_rate_reader_class.cc++'
root -l -b -q 'jet_horns.cc++'
cd ../Full2022v12
```

Then always test the real configuration:

```bash
mkShapesRDF -c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
```

A standalone C++ compile is necessary but not sufficient: the actual alias call may still have the wrong argument type or unavailable column.

---

## 6. DNN workflow

Enter:

```bash
cd DNNmodels
ls
```

The intended stages are:

```text
analysis ntuples
   -> training snapshots
   -> train model + preprocessing
   -> save model
   -> inference wrapper
   -> alias in mkShapesRDF
   -> DNN score used in cuts/variables
```

### Prepare snapshots

```bash
python3 prepare_snapshots_submit.py
```

This sends/organizes the preparation of smaller training files containing the selected events and features.

### Train

```bash
python3 train_from_snapshots_ttDM.py
python3 train_from_snapshots_tWDM.py
```

Do not interpret a training script as part of normal histogram production. Training is an offline step that creates a model. The production only needs the resulting model/preprocessing plus the inference implementation.

### Inference

Search:

```bash
grep -R "EvaluateDNN\|evaluate_DNN" -n Full2022v12
```

The DNN inference is connected through the alias using two helper files:

```text
alias
   ↓
evaluate_....cc
   ↓
Evaluate....py
   ↓
trained model
   ↓
DNN score
```
The alias loads the C++ evaluator and calls it:
```bash
aliases['evaluate_dnn'] = {
    'linesToAdd': [
        '#include "evaluate_dnn.cc"'
    ],
    'expr': 'evaluate_dnn(...)'
}
```
The C++ file acts as the interface used by ROOT/mkShapesRDF. It receives the event variables and forwards them to the Python evaluator.

---

