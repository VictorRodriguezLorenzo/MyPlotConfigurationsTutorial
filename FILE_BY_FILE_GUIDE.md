# File-by-file guide

## `configuration.py`
This file organized the whole setup, it names the component files, output locations, luminosity, compiled variables and runner settings.

## `samples.py`
Maps physics process names to physical ROOT files and event weights. This is where dataset composition, MC normalization factors, per-dataset extra weights, data primary datasets and trigger overlap logic normally live.

## `aliases.py`
Creates derived RDataFrame columns. Aliases range from one-line formulas to correction readers, b-tag weights, custom C++ reconstruction and ML inference. This is also where nuisance-aware recomputation (`afterNuis`) often becomes important.

## `cuts.py`
Defines one common `preselections` expression plus additonal control/signal regions and optional categories.

## `variables.py`
Defines histogram expressions, binning, labels and folding.

## `plot.py`
Controls display names, colors, grouping, signal/background appearance and data drawing/blinding.

## `nuisances.py` / `nuisances_ALL.py`
Defines systematic effects and maps them to samples. These are later included in the fit.

## `structure.py`
Declares statistical roles, especially signal versus background versus data. It becomes critical for datacards and Combine.

## `data/`
Analysis-local calibration payloads or derived maps. In this tutorial the key example is b-tag efficiency maps.

## `extended/`
Helper code that is often compiled/loaded as a library, especially correction evaluators or classes requiring initialization/state.

## `macros/`
Custom C++ calculations included into ROOT's interpreter, such as `mT2`, top reconstruction and derived kinematics.

## `DNNmodels/`
Offline dataset preparation/training plus stored model/preprocessing material. Training and production inference are separate workflows.

## `MergeRun3/`
Combination logic that consumes already validated per-campaign outputs.

## `limits/`
Analysis wrappers around workspace/Combine tasks and plotting of statistical results.
