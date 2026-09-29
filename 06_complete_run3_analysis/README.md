# 06 — Complete Run 3 analysis, datacards and limits

## Goal

This is the “take it to a full analysis” module. It preserves the complete dileptonic TTDMsimp setup across Run 3 campaigns and adds the production/statistical workflow around it.

Included configurations:

```text
Full2022v12
Full2022EEv12
Full2023v12
Full2023BPixv12
Full2024v15
MergeRun3
limits
```

Do not start here if you cannot explain Modules 1–5.

---

## 1. Treat every campaign as a separate analysis configuration

For example:

```bash
cd Full2022v12
mkShapesRDF -c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
mkShapesRDF -o 0 -f . -b 1
mkShapesRDF -o 1 -f .
mkShapesRDF -o 2 -f .
```

Repeat for each production-ready year/era.

Do not copy a 2022 configuration to 2024 and change only the luminosity. Campaign-dependent items can include:

- production and reconstruction tags;
- data streams;
- trigger logic;
- lepton working points/payloads;
- b-tag tagger/WP/calibration and efficiency map;
- jet/MET corrections and uncertainty sources;
- NanoAOD branch availability;
- DNN model/preprocessing when trained separately;
- nuisance names/correlations.

---

## 2. Theory normalizations

Where required by this analysis:

```bash
python3 mkTheoryNormalizations.py --samplesFile samples.py --year <YEAR> --verbose 2
```

- `--samplesFile samples.py`: use this campaign's sample definitions;
- `--year <YEAR>`: choose the calibration/year convention expected by the script;
- `--verbose 2`: print detailed progress/debug information.

Do this only with the campaign/environment for which the script is intended; then inspect the generated normalization inputs before relying on them.

---

## 3. Merge Run 3 (see [Sergio's slides ](https://indico.cern.ch/event/1663944/#176-implementation-of-mkmergey))

After each year is complete:

```bash
cd ../MergeRun3
python3 mkMergeYears.py --help
python3 mkMergePlots.py --help
```

Read `merge_configuration.py` and set/check the input files.

After merging, check numerically that a merged nominal yield is the sum of the constituent campaigns. 

---

## 5. Datacards

The campaign and merged folders contain `mkDatacards_topDM.py`.

Start with:

```bash
python3 mkDatacards_topDM.py --help
```

Before creating a final card, validate:

- `structure.py`: signal/background/data classification;
- `nuisances_ALL.py`: active uncertainties and correlations;
- nominal histograms;
- every important Up/Down pair;
- binning and empty/negative bins;
- process names expected by the script.

A syntactically valid datacard can still encode the wrong physics model.

For simpler setups, mkShapesRDF has an already implemented `mkDatacards` [module](mkShapesRDF/shapeAnalysis/latinos/mkDatacards.py), you can use it:
```bash

mkDatacards
```

---

## 6. Build a Combine environment. [Installation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/#installation-instructions)

Use a collaboration-supported CMSSW release. The configuration currently documents:

```bash
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git -c advice.detachedHead=false clone --depth 1 --branch v10.5.0 \
    https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git \
    HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scramv1 b clean
scramv1 b -j 8
```

Command meaning:

- `cmsrel ...`: create a CMSSW release area;
- `cmsenv`: load that release's runtime environment;
- `git clone --branch ...`: fetch the chosen Combine version;
- `scramv1 b clean`: clear old build products;
- `scramv1 b -j 8`: compile using up to eight parallel build jobs.

For a future analysis, check current CMS recommendations before freezing versions.

---

## 7. Workspace and limits in this analysis

Create workspaces with the analysis wrapper:

```bash
python3 limits/mk_Limits.py \
  --work-dir MergeRun3 \
  --task WS \
  --cmssw-dir /path/to/CMSSW_14_1_0_pre4/src
```

Then expected/blind limits:

```bash
python3 limits/mk_Limits.py \
  --work-dir MergeRun3 \
  --task LIMITS \
  --plot \
  --limit-run blind
```

Interpretation of the key switches:

- `--work-dir`: campaign/combination whose cards/histograms are used;
- `--task WS`: build the statistical workspace;
- `--task LIMITS`: run the limit stage;
- `--plot`: also make the limit visualization supported by the wrapper;
- `--limit-run blind`: use the blind/expected mode rather than revealing observed results.

Use the wrapper's `--help` to see all available options in your checkout.

---

