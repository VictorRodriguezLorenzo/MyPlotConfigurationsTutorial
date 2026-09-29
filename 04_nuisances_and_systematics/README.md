# 04 — Nuisances and systematic variations

## Goal

A nominal histogram is only part of an analysis. This module explains how mkShapesRDF produces and labels the variations used later in a statistical fit.

The working example is the same real 2022 TTDM configuration as Module 3, so you can focus on the systematic layer without simultaneously changing the physics selection.

---

## 1. Start with the nuisance dictionary

```bash
cd Full2022v12
less nuisances.py
less nuisances_ALL.py
```

A nuisance entry usually communicates four things:

```text
human/config key
    -> name written to statistical model
    -> mechanism (weight, suffix, lnN, auto-stat, ...)
    -> affected samples and Up/Down definitions
```

Do not begin by copying a large nuisance block. Pick one nuisance and trace its Up/Down input all the way back to the branch or alias that provides it.

---

## 2. Normalization versus shape effects

A normalization-only uncertainty changes the overall expected rate (lnN). A shape uncertainty can change different histogram bins by different amounts.

Typical examples:

- luminosity: often a multiplicative normalization (`lnN` in the statistical model);
```text
nuisances['lumi'] = {
    'name': 'lumi_13p6TeV_2022',
    'type': 'lnN',
    'samples': {
        'WW': '1.014',
        'top': '1.014',
    },
}
```
here:
key       → name ROOT identifier
name      → nuisance name in the datacard
type      → how the variation is interpreted
samples   → processes affected

- lepton SF Up/Down: event-weight variation and therefore a shape-capable effect;
- JES/JER: changes reconstructed jet kinematics, migrations between categories and derived observables; fundamentally an object/shape variation.

The word “shape” does not mean the total integral must stay fixed. It means the fit receives alternative binned templates rather than a single number.

---

## 3. Weight nuisances

A weight nuisance keeps the nominal event kinematics and changes the event weight.

These are, for example, lepton and b-tag variations in `aliases.py`:

If an Up/Down alias exists but no nuisance references it, it will not automatically become a fit uncertainty.

---

## 4. Object variations: JES/JER/MET/leptons

Object uncertainties are more subtle because a shifted jet or MET can change:

- a variable value;
- whether an event passes the selection;
- which category it belongs to;
- any derived quantity that uses the shifted object.

This is why real configurations distinguish aliases that must be recalculated after nuisance-shifted columns exist.

For example, `nbjets`, a jet-bin alias, `mT2`, or a full top reconstruction may need to follow the shifted inputs rather than remain frozen at its nominal value.

---

## 5. `nuisances.py` versus `nuisances_ALL.py`

The exact split is analysis-specific. In this repository, treat `nuisances.py` as the working/selected nuisance configuration and `nuisances_ALL.py` as the more complete collection used when producing the full analysis/statistical model.

Check which one is active in:

```bash
grep -n "nuisancesFile" configuration.py
```

Do not edit one and assume mkShapesRDF is reading it; always verify the active file and recompile.

---

## 6. MC statistical uncertainty

Find the `stat` nuisance. Auto/statistical uncertainties are not detector calibrations; they encode limited MC statistics in histogram bins.

They can dominate when you use very fine binning with sparse samples. 

---

## 7. Run sequence

When you change a nuisance or any alias it depends on:

```bash
mkShapesRDF -c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
```

Then the normal batch cycle:

```bash
mkShapesRDF -o 0 -f . -b 1
mkShapesRDF -o 1 -f .
mkShapesRDF -o 1 -f . -r 1   # only if failures exist
mkShapesRDF -o 2 -f .
```

