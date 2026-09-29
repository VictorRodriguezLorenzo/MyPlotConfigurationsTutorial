# 02 — Understanding the configuration

## Goal

The physics remains deliberately simple. This module teaches **what every core mkShapesRDF configuration file does and how the files talk to one another**.

Use the same run commands as Module 1. The new material is the configuration itself.

---

## 1. `configuration.py` — the wiring diagram

Important lines:

```python
tag = "tutorial_02_2022"
outputFile = f"mkShapes__{tag}.root"
lumi = 7.9804
```

- `tag` distinguishes this production from another one;
- `outputFile` is the final merged ROOT file;
- `lumi` is the luminosity used by the framework to normalize MC yields.

Then the file names:

```python
samplesFile = "samples.py"
aliasesFile = "aliases.py"
cutsFile = "cuts.py"
variablesFile = "variables.py"
plotFile = "plot.py"
nuisancesFile = "nuisances.py"
structureFile = "structure.py"
```

`filesToExec` tells the compiler which files to execute, and `varsToKeep` tells it which resulting Python objects must survive into the compiled configuration.

---

## 2. `samples.py` — input files and event weights

The key helper is:

```python
searchFiles = SearchFiles()
```

and then:

```python
nanoGetSampleFiles(mcDirectory, "WWTo2L2Nu")
```

This searches the production directory and returns the ROOT files belonging to that dataset tag.

A sample entry has the form:

```python
samples["WW"] = {
    "name": nanoGetSampleFiles(mcDirectory, "WWTo2L2Nu"),
    "weight": mcCommonWeight,
    "FilesPerJob": 10,
}
```

- dictionary key `"WW"`: process name used by the rest of the configuration;
- `name`: physical input files, possibly composed from several dataset tags;
- `weight`: expression multiplied into each selected event;
- `FilesPerJob`: how the file list is split across batch jobs.

The sample weights are already analysis-like. For MC, the common event weight includes the cross-section normalization, event filters and `SFweight`; the latter is built in `aliases.py` from the relevant correction factors. `samples.py` also defines `DATA` and the data-driven `Fake` contribution.

---

## 3. `aliases.py` — derived quantities and hidden analysis machinery

It contains, among other things:

- lepton working-point cuts and lepton scale factors;
- the fake/nonprompt transfer factor and its variations;
- jet and b-jet definitions;
- b-tagging working points;
- b-tag efficiency-map based scale-factor evaluation;
- the combined `SFweight`;
- derived observables, such as `mT2`.

The useful skill here is only recognizing that a name used in `cuts.py` or `samples.py` can come from `aliases.py`.

For example, the simple beginner selection uses:

```python
'bVeto'
```

but the actual definition of `bVeto`, the chosen tagger/working point and the b-tag SF machinery live in `aliases.py`. 

## 4. `cuts.py` — preselection, regions and categories

The global preselection is:

```python
preselections = " && ".join([...])
```

It is applied before every region.

A region is then defined as:

```python
cuts["WWSR"] = {
    "expr": "...",
    "categories": {
        "inclusive": "1",
        "0j": "zeroJet",
    },
}
```

A category expression of `"1"` means “no additional requirement.”

---

## 5. `variables.py` — histograms

Example:

```python
variables["mll"] = {
    "name": "mll",
    "range": (30, 0, 150),
    "xaxis": "m_{ll} [GeV]",
    "fold": 3,
}
```

- key `mll`: histogram identifier;
- `name`: RDataFrame expression to histogram;
- `range`: `(number_of_bins, xmin, xmax)`;
- `xaxis`: label passed to plotting;
- `fold`: underflow/overflow folding convention used by the framework.

For irregular bins, real analyses can pass an explicit bin-edge list

---

## 6. `plot.py` — visual grouping, not event selection

Two concepts appear:

- `plot[...]`: style of an individual sample;
- `groupPlot[...]`: combine several samples under one legend/process group.

---

## 7. `nuisances.py` 

The analysis uses the nuisance file selected in `configuration.py`:

```python
nuisancesFile = "nuisances.py"
```


nuisances.py contains a reduced set of the main uncertainties, for example:
- luminosity
- lepton efficiencies
- trigger efficiency
- b-tagging
- fake-rate uncertainties
- MC statistical uncertainties

It is usually used while developing or testing the analysis because it is faster and produces fewer systematic variations.
nuisances_ALL.py contains the full set of systematic uncertainties used for the final analysis.

This, schematically:
```test
nuisances.py
    ↓
smaller set of uncertainties
    ↓
development / testing

nuisances_ALL.py
    ↓
full uncertainty model
    ↓
final production
```

To switch between them, change:
```
nuisancesFile = "nuisances.py"/"nuisances_ALL.py"
```

## 8. `structure.py` — statistical roles

The file contains entries such as:

```python
structure["WW"] = {
    "isSignal": 0,
    "isData": 0,
}
```

The file already distinguishes simulated backgrounds, the data-driven `Fake` process and observed `DATA`. `structure.py` becomes especially important when building datacards, where the statistical model must know which entries correspond to data, backgrounds and possible signals.

---

## 10. Your first safe edits

If you really one to change a few things now, try only these three things:

1. Change the Z window in `cuts.py` from `15` GeV to `10` GeV.
2. Change the binning of `mll` in `variables.py`.
3. Add one existing branch as a new variable, so that it gets plotted.

After **each** edit:

```bash
mkShapesRDF -c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
```

Only submit again after the short test passes.
