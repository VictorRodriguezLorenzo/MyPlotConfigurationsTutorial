# 03 — Complete TTDMsimp dileptonic analysis

This directory is a self-contained copy of the whole analysis setup. It includes
`Full2022v12`, `Full2022EEv12`, `Full2023v12`, `Full2023BPixv12`,
`Full2024v15`, the development `Full2025v15` content, shared macros/data,
`MergeRun3`, and `limits`.

## 1. Run every production year

Start mkShapesRDF and enter one year directory:

```bash
cd <working-directory>/mkShapesRDF
source start.sh
cd PlotsConfigurationsRun3/topDM/TTDMsimp_dileptonic/tutorial/03_complete
cd Full2022v12       # repeat for every production-ready Full20XX directory
```

For every year:

```bash
mkShapesRDF --c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
mkShapesRDF -o 0 -f . -b 1
mkShapesRDF -o 1 -f .
mkShapesRDF -o 1 -f . -r 1
mkShapesRDF -o 2 -f .
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png

```

Check the luminosity, production names, writable output paths, signal input, and
DNN model files separately for every year before submission.

For this folder, nuisances theory normalizations have been added for CRs and signal samples,
so running:

```bash
python3 mkTheoryNormalizations.py --samplesFile samples.py --year {YEAR} --verbose 2
```
is required.

## 2. Merge Run 3

After all year outputs are complete:

```bash
cd ../MergeRun3
python mkMergeYears.py -help
python mkMergePlots.py --help
```

Set the input paths in `merge_configuration.py`, run the scripts with the
arguments shown by their help, and verify that each merged yield equals the sum
of the corresponding year yields.

## 3. Datacards

The year and merged folders contain `mkDatacards_topDM.py`:

```bash
python mkDatacards_topDM.py --help
```

Inspect `nuisances_ALL.py`, `structure.py`, and every nominal/up/down histogram
before producing the final cards.

## 4. Combine and limits

Use the collaboration-supported CMSSW/Combine environment:

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
This will create the combine framework, so that limits can later be extracted

For this analysis, everything is comprised in `mk_Limits.py`, so to first create the workspace:

```bash
python3 limits/mk_Limits.py --work-dir MergeRun3 --task WS  --cmssw-dir /afs/cern.ch/user/v/victorr/CMSSW_14_1_0_pre4/src
```

and to extract limits:

```bash
python3 limits/mk_Limits.py --work-dir MergeRun3 --task LIMITS --plot --limit-run blind
```

This can be done for a specific campaign just changing `MergeRun3` by the intended year (running the whole datacard generation process first).

To plot the year combination, run:

```
python3 mkMergePlots.py -i {outputFolder}/mkShapes__ttDM_dilep_Run3.root -o {plotPath}/Plots/MergeRun3 -p ratio
```
