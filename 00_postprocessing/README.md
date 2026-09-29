# Module 00 — NanoAOD post-processing

Before running the analysis itself, it is useful to understand where the input ROOT files come from.

The mkShapesRDF workflow can be viewed as two main stages:

```text
official CMS NanoAOD
        ↓
post-processing
        ↓
Latino / analysis NanoAOD
        ↓
mkShapesRDF shape analysis
        ↓
histograms / plots / datacards
```

---

## 1. Official NanoAOD vs Latino NanoAOD

CMS centrally produces the official **NanoAOD** datasets, with the following [information](https://cms-xpog.docs.cern.ch/autoDoc/).

The samples commonly used by Latinos analyses are stored under directories such as

```text
/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/
```

These files are still based on NanoAOD, but they have usually passed through an additional **Latino post-processing step**, using the Latinos [processor.py](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/framework/processor.py).

Therefore, they should not be thought of simply as untouched copies of the centrally produced NanoAOD.

Schematically:

```text
CMS NanoAOD
    ↓
Latino post-processing
    ↓
nanoLatino ROOT files
```

The post-processing can add quantities that are useful for many analyses, for example:

- corrected physics objects;
- lepton collections: [LeptonMaker](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/modules/LeptonMaker.py);
- additional kinematic variables: [l2Kin](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/modules/l2KinProducer.py), [l3Kin](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/modules/l3KinProducer.py), [l4Kin](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/modules/l4KinProducer.py);
- pileup weights: [runDependentPuW.py](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/modules/runDependentPuW.py);
- trigger scale factors;
- lepton scale factors: [LeptonSF.py](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/modules/LeptonSF.py);
- b-tagging-related quantities;
- MET filters;
- generator-level information;
- systematic variations...

The exact content depends on the [production](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/framework/Productions_cfg.py)  and on the [processing steps](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/framework/Steps_cfg.py) that were run.

---

## 2. Why do we post-process?

The official NanoAOD contains the basic reconstructed CMS objects and information.

However, an analysis often repeatedly needs quantities such as

```text
tight leptons
dilepton variables
trilepton variables
corrected jets
corrected MET
pileup weights
trigger SFs
lepton SFs
systematic variations
```

Instead of recalculating all of these from scratch every time histograms are produced, many common quantities can be computed once during post-processing and stored as additional branches.

Conceptually:

```text
NanoAOD branch
     +
correction / producer module
     ↓
new NanoAOD branch
```

For example,

```text
Muon_pt, Electron_pt
        ↓
lepton producer
        ↓
Lepton_pt
```

or

```text
event information
        ↓
pileup correction
        ↓
puWeight
```

The analysis stage can then directly use these branches.

---

## 3. Post-processing and analysis are different stages

This distinction is important.

### Post-processing

The post-processing stage prepares the input events:

```text
NanoAOD
   ↓
corrections
new collections
new variables
weights
systematic object variations
   ↓
processed NanoAOD
```

### Shape analysis

The analysis configuration then decides how those quantities are used:

```text
processed NanoAOD
      ↓
samples.py
aliases.py
cuts.py
variables.py
nuisances.py
      ↓
histograms
```

For example, the post-processing may create

```text
puWeight
TriggerSFWeight
Lepton_RecoSF
```

but the analysis still decides how these terms enter the nominal event weight.

Likewise, object variations may already exist in the post-processed production, while `nuisances.py` determines whether and how those variations are propagated to the final histograms.

---

## 4. Systematic variations

Some object-related systematic variations are also produced during post-processing.

For example, a production directory may contain

```text
...__l2tight
...__l2tight__jerup_suffix
...__l2tight__jerdo_suffix
...__l2tight__jes...up_suffix
...__l2tight__jes...do_suffix
```

Schematically:

```text
nominal NanoAOD
       │
       ├── nominal objects
       │
       ├── JER Up
       ├── JER Down
       ├── JES Up
       └── JES Down
```

The analysis does **not** automatically use all of these variations.

Later, `nuisances.py` specifies which variations should be used when filling the systematic templates.

Therefore:

```text
post-processing
    → produces the variation

nuisances.py
    → tells mkShapesRDF to use it
```

---

## 5. Common producer modules

The processor is built from [modules](https://github.com/latinos/mkShapesRDF/tree/master/mkShapesRDF/processor/modules) that operate on the event RDataFrame and add or modify columns.

Some producers calculate quantities that are useful in many analyses.

For example, depending on the production, modules such as

```text
l2KinProducer
l3KinProducer
```

can provide commonly used two-lepton and three-lepton kinematic quantities.

Before implementing a new variable, it is therefore worth checking whether it already exists in the post-processed files.

For example, quantities such as

```text
mll
ptll
mlll
ΔR between leptons
```

may already be available.

---

## 6. Do I need to post-process every new variable?

No.

This is an important distinction.

Suppose you want a new quantity:

```text
new analysis variable
```

You have two possibilities.

### Option A — calculate it during post-processing

```text
NanoAOD
   ↓
producer module
   ↓
new branch stored in ROOT file
```

This is useful when the quantity is:

- expensive to calculate;
- required by many analyses;
- required repeatedly;
- naturally part of an object-correction chain.

### Option B — calculate it in `aliases.py`

```text
existing branches
       ↓
aliases.py
       ↓
new analysis column
```

This is often preferable for analysis-specific quantities.

For example:

```python
aliases['myVariable'] = {
    'expr': 'some_expression'
}
```

The variable then exists during the analysis without having to create a new NanoAOD production.

A useful rule is:

```text
common/reusable quantity
        → consider post-processing

analysis-specific quantity
        → usually aliases.py
```

---

## 7. Can mkShapesRDF use official NanoAOD directly?

Yes.

mkShapesRDF is not restricted to the centrally produced Latino files.

The framework can also work starting from official CMS NanoAOD or from your own processed/skimed samples.

The file utilities can search either ordinary directories or DAS datasets, so the framework is not intrinsically tied to the HWW EOS directory.

Schematically:

```text
                   ┌─ Latino central production
official NanoAOD ──┤
                   └─ your own post-processing
                              ↓
                         mkShapesRDF
```

Using the existing Latino production is usually easier because many common corrections and variables have already been prepared.

However, for a new analysis you may need samples that are not available centrally, or you may require a processing step specific to your analysis.

In that case, producing your own processed samples is perfectly valid.

---

## 8. Running the processor

The post-processing command is

```bash
mkPostProc
```

The basic syntax is

```bash
mkPostProc -o 0 -p <production> -s <step>
```

where

```text
-p
    production configuration

-s
    processing step

-o 0
    run/submit the post-processing
```

The framework documentation defines this interface directly in the processor scripts.

For example:

```bash
mkPostProc \
    -o 0 \
    -p <production> \
    -s <step> \
    -T <sample>
```

Here,

```text
-T
    process only the selected sample
```

A useful first test is to limit the number of files:

```bash
mkPostProc \
    -o 0 \
    -p <production> \
    -s <step> \
    -T <sample> \
    --limitFiles 1
```

You can also perform a dry run:

```bash
mkPostProc \
    -o 0 \
    -p <production> \
    -s <step> \
    -T <sample> \
    --limitFiles 1 \
    --dryRun 1
```

This prepares the job without submitting it.

The available `mkPostProc` options also include selecting/excluding samples, changing the input folder, choosing whether inputs use the Latino naming convention, using an XRootD redirector, and setting the maximum number of files per job.

---

## 9. Checking the jobs

After submission, the processor jobs can be checked with

```bash
mkPostProc \
    -o 1 \
    -p <production> \
    -s <step>
```

Conceptually,

```text
-o 0
    → run post-processing

-o 1
    → check post-processing jobs
```

Failed jobs can also be resubmitted through the corresponding `mkPostProc` option.

---

## 10. The processing chain

A production usually consists of several processing modules executed sequentially.

Conceptually:

```text
NanoAOD
   ↓
module 1
   ↓
module 2
   ↓
module 3
   ↓
...
   ↓
processed NanoAOD
```

For example:

```text
NanoAOD
   ↓
object corrections
   ↓
lepton selection
   ↓
kinematic producers
   ↓
scale factors
   ↓
systematic variations
   ↓
nanoLatino file
```

The exact sequence depends on the selected production and step.

This is why directory names in the central production often look like

```text
MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight
```

The name reflects the sequence of processing [Steps](https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/framework/Steps_cfg.py) that has been applied.

---

## 11. Where should I implement something?

When adding something new, first ask what kind of quantity it is.

```text
Do I need a new quantity?
          ↓
          ├── already in NanoAOD?
          │        → use it directly
          │
          ├── already produced by Latino post-processing?
          │        → use existing branch
          │
          ├── analysis-specific expression?
          │        → aliases.py
          │
          └── reusable correction / collection / expensive calculation?
                   → consider post-processing
```

For most beginner analyses, you will **not** need to modify the post-processing.

You will normally start from the existing centrally produced NanoAOD files and define your analysis-specific variables using `aliases.py`.

---

## 12. Full workflow

The complete picture is therefore:

```text
CMS DAS
│
│ official NanoAOD
▼
┌─────────────────────────────┐
│ mkShapesRDF post-processing │
│                             │
│ corrections                 │
│ collections                 │
│ scale factors               │
│ kinematic variables         │
│ systematic variations       │
└─────────────────────────────┘
              │
              │ nanoLatino ROOT files
              ▼
┌─────────────────────────────┐
│ mkShapesRDF shape analysis  │
│                             │
│ samples.py                  │
│ aliases.py                  │
│ cuts.py                     │
│ variables.py                │
│ nuisances.py                │
└─────────────────────────────┘
              │
              ▼
          histograms
              │
              ▼
            plots
              │
              ▼
          datacards
              │
              ▼
            Combine
```
