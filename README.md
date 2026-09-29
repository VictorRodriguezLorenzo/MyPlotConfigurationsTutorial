# mkShapesRDF — from first plot to a full Run 3 analysis

This repository is a **progressive tutorial** for the `mkShapesRDF` framework.
It is intentionally split into two audiences:


- Module 00: for understanding where the input NanoAOD files come from and how the mkShapesRDF post-processing stage fits into the workflow. It introduces the difference between official CMS NanoAOD, centrally post-processed Latino samples, and analysis-level processing.

- Modules 1–2: based on a WW analysis, for someone who only needs to make a small analysis run. The configuration is already realistic: data, fakes, scale factors, b-tagging and nuisances are all present, but these ingredients are treated as pre-existing infrastructure rather than teaching topics. The focus is on the basic run commands, regions, variables, samples and overall configuration flow.

- Modules 3–6: based on the tt+DM dileptonic analysis, for someone building a full CMS Run 3 analysis and who needs to understand and modify the underlying machinery rather than only copy an existing configuration. These modules cover corrections and weights, fake-rate and b-tagging implementations, systematic uncertainties, custom C++ code, extended modules, machine-learning inference, multi-year configurations and statistical analysis.

The examples are built from two real configurations:

- the dileptonic `TTDMsimp` top+DM analysis (NPS-26-025), used heavily for corrections, b tagging, custom observables, ML, multi-year combination and limits;

- the Run 3 WW analysis, used as a complementary example of a compact dilepton analysis and simple DY/WW/top regions.

The first two modules are **deliberately simpler than either real analysis**.

## Course map

| Module | Goal | Complexity |
|---|---|---|
| [01 — Making it run](01_making_it_run/README.md) | install, compile, test, submit, check, merge and plot a tiny DY/WW example | beginner |
| [02 — Understanding the configuration](02_understanding_the_configuration/README.md) | understand every core `.py` file and make simple edits safely | beginner |
| [03 — Data and corrections](03_data_and_corrections/README.md) | data streams, triggers, lepton SFs, b tagging, efficiency maps and event weights | analysis |
| [04 — Nuisances and systematics](04_nuisances_and_systematics/README.md) | weight/shape nuisances, JES/JER/MET/lepton variations, b-tag uncertainties and `afterNuis` | analysis |
| [05 — Custom code, extended and ML](05_custom_code_extended_and_ml/README.md) | C++ macros, `extended/`, vector-returning producers, fake-rate helpers and DNN inference/training | advanced |
| [06 — Complete Run 3 analysis](06_complete_run3_analysis/README.md) | multiple campaigns, theory normalizations, merging, datacards and Combine limits | advanced |

Also keep these beside you:

- [Command cheat sheet](COMMAND_CHEATSHEET.md)
- [File-by-file reference](FILE_BY_FILE_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)

## The standard workflow in one picture

```text
configuration.py
      |
      +--> samples.py      which ROOT files and event weights?
      +--> aliases.py      which derived columns / corrections?
      +--> cuts.py         which regions/categories?
      +--> variables.py    which histograms?
      +--> plot.py         how are processes plotted/grouped?
      +--> nuisances.py    which systematic variations?
      +--> structure.py    signal/background/data roles for statistics
      |
      v
mkShapesRDF -c 1                  compile configuration
      |
      v
mkShapesRDF -o 0 ... -b 0        short local test
      |
      v
mkShapesRDF -o 0 ... -b 1        HTCondor production
      |
      v
mkShapesRDF -o 1 ...              inspect job logs / resubmit failures
      |
      v
mkShapesRDF -o 2 ...              merge job ROOT files
      |
      +--> mkPlot                  plots
      +--> mkDatacards / scripts  statistical model
                                  |
                                  v
                                Combine
```

## Recommended order

Finish Modules 1 and 2 first. For a short student project, that may already be enough. 

For analysis work, continue sequentially because each later module assumes the vocabulary introduced before it.

For further understanding on the Latinos framework post-processing, look at Module 0.
