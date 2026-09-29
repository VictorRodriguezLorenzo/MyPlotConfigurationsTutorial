# 02 — TTDMsimp dileptonic setup with macros and DNNs

After completing `01_basic_cuts`, this module is a continuation with the same
configuration style, adding everything intentionally
removed from setup 01:

- `doubleNu_producer` and its reconstructed quantities;
- `Fake factor method`, with its corresponding macro implemented;
- `topDMVars`, rest-frame variables, `mT2`, and `mt2blbl`;
- ttZ lepton-index calculation and the ttZ control region;
- ttDM and tWDM scalar/pseudoscalar DNN aliases;
- DNN snapshot, training, and evaluation programs.

## 1. Start the environment

```bash
cd <working-directory>/mkShapesRDF
source start.sh
cd PlotsConfigurationsRun3/topDM/TTDMsimp_dileptonic/tutorial/02_extended/Full2022v12
```

All analysis-local paths used by `aliases.py` are calculated from this folder.
The setup does not load macros or configurations from `../../Full2022v12`.

## 2. Compile the b-tag helpers

```bash
cd ../extended
root -l -b -q 'evaluate_btagSFbc.cc++'
root -l -b -q 'evaluate_btagSFlight.cc++'
root -l -b -q 'fake_rate_reader_class.cc'
root -l -b -q 'jet_horns.cc'
cd ../Full2022v12
```

## 3. Using custom C++ macros 

Custom C++ code can be added to the analysis through `aliases.py`. This is useful when a quantity is too complex to express directly as a simple `RDataFrame` expression, or basically when it wasn't added already into our Latinos Ntuples

In this setup, two common patterns are used.

### 1. Macro returning a single value: `computeMT2`

For relatively simple calculations, the C++ file can define a function that directly returns the quantity of interest. For example, `computeMT2.cc` provides the function used to calculate the `mT2` variable.

The macro is first loaded from `aliases.py`, for example with:

```python
aliases['mT2'] = {
    'linesToAdd': [
        '#include "path/to/computeMT2.cc"'
    ],
    'expr': 'computeMT2(...)',
    'samples': mc + data
}
```

The important parts are:

- `linesToAdd`  
  Adds the C++ source code to the ROOT interpreter. In this case, the macro is included with `#include`.

- `expr`  
  Calls the C++ function for every event. The returned value becomes the value of the alias.


### 2. Macro returning several values: `doubleNu_producer`

For more complex reconstruction algorithms, a single C++ call may calculate several related observables at once. The `doubleNu_producer` is an example of this approach. It performs the dileptonic top reconstruction and returns a vector containing several quantities.

The macro can again be loaded in `aliases.py`:

```python
aliases['doubleNu'] = {
    'linesToAdd': [
        '#include "path/to/doubleNu_producer.cc"'
    ],
    'expr': 'doubleNu_producer(...)',
    'samples': mc + data
}
```

The result of the C++ function is stored in an intermediate alias:

```text
doubleNu
```

which contains several values, for example:

```text
doubleNu[0]  -> neutrino 1 px
doubleNu[1]  -> neutrino 1 py
doubleNu[2]  -> neutrino 2 px
doubleNu[3]  -> neutrino 2 py
doubleNu[4]  -> reconstructed top 1 pT
doubleNu[5]  -> reconstructed top 2 pT
doubleNu[6]  -> chel
doubleNu[7]  -> dphi_ttbar
doubleNu[8]  -> pdark
doubleNu[9]  -> valid reconstruction flag
```

Individual observables can then be exposed as separate aliases:

```python
aliases['chel'] = {
    'expr': 'doubleNu[6]',
    'samples': mc + data
}

aliases['dphi_ttbar'] = {
    'expr': 'doubleNu[7]',
    'samples': mc + data
}

aliases['pdark'] = {
    'expr': 'doubleNu[8]',
    'samples': mc + data
}

aliases['tt_reco'] = {
    'expr': 'doubleNu[9]',
    'samples': mc + data
}
```

The advantage of this approach is that the expensive reconstruction is performed only once per event and several observables can be extracted from the same result.

## 4. DNN models

The DNNmodels/ directory contains the scripts used to prepare the training samples and train the DNNs used in the analysis.

The workflow is:

1. Prepare the training snapshots

```bash
cd DNNmodels
```

and to run the preparation through batch jobs:

```bash
python prepare_snapshots_submit.py
```

This scripts reads the analysis ROOT files, apply the required selection, and create smaller ROOT files containing only the events and variables needed for training.

2. Train the DNN

For the ttDM network:

```bash
python train_from_snapshots_ttDM.py
```

For the tWDM network:

```bash
python train_from_snapshots_tWDM.py 
```

The training scripts read the snapshots, train the neural network, and save the trained model and preprocessing files in DNNmodels/Models/.

Once the model is trained, it is loaded from aliases.py. The corresponding alias calls the DNN evaluation code and defines the DNN score as a new analysis variable, for example:

```bash
aliases['DNN'] = {
    'linesToAdd': [
        '#include "path/to/DNN_evaluation.cc"'
    ],
    'expr': 'evaluateDNN(...)',
    'samples': mc
}
```

The DNN output can then be used like any other variable in cuts.py or variables.py. The evaluation takes place with the modules `EvaluateDNN_tXDM_Y.py` and `evaluate_DNN_tXDM.cc`, which use the trained models for event discrimination inference when running the analysis. 

## 5. Run

```bash
mkShapesRDF --c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
mkShapesRDF -o 0 -f . -b 1
mkShapesRDF -o 1 -f .
mkShapesRDF -o 1 -f . -r 1
mkShapesRDF -o 2 -f .
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
```

