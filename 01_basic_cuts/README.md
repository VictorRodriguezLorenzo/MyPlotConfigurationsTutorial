# 01 — Basic TTDMsimp dileptonic setup

This is the original `Full2022v12` analysis structure with only the advanced
region removed. It keeps the original samples, aliases, selections, variables,
plots, nuisances, and structure style. It does **not** contain or calculate:

- `doubleNu_producer`: this module acts as a ttbar system reconstructor;
- `Fake factor method` setup not included, using only MC;
- additional `topDMVars` and rest-frame variables;
- DNN discriminants or DNN training/evaluation files;
- ttZ lepton indices, the `ttZcr` alias, or the `ttZcr` cut.

The analysis, thus, is based on two categories: `2l_2b`,`nLepton == 2 && nbjets >= 2`; and `2l_1b`,`nLepton == 2 && nbjets == 1`,

## 1. Installation

Log in to CERN LXPLUS:

```bash
ssh -Y -l <username> lxplus.cern.ch -o ServerAliveInterval=240
```

Clone and install mkShapesRDF:

```bash
git clone https://github.com/latinos/mkShapesRDF.git
cd mkShapesRDF
./install.sh
```
this will download the `master` branch with the latest changes, and initialize the installation of the framework.

## 2. Always do

At the start of every session:

```bash
ssh -Y -l <username> lxplus.cern.ch -o ServerAliveInterval=240
cd <working-directory>/mkShapesRDF
source start.sh
cd MyPlotConfigurationsTutorial/01_basic_cuts/Full2022v12
```

The folder is self-contained. `aliases.py` resolves `../macros`, `../extended`,
and `../data` from this setup. 

#### The first time running the code, do:

```bash
cd ../extended
root -l -b -q 'evaluate_btagSFbc.cc++'
root -l -b -q 'evaluate_btagSFlight.cc++'
cd ../Full2022v12
```
this will allow the b-tagging efficiency maps to be evaluated for the analysis, which will be used to weight the MC
NOTE: Don't worry about failures like: 
```
input_line_15:2:3: error: use of undeclared identifier 'evaluate_btagSFbc'
 (evaluate_btagSFbc())
```

## 3. Produce the analysis histograms

| Action | Command |
|---|---|
| Compile configuration | `mkShapesRDF -c 1` |
| Run locally (this runs 10 events) | `mkShapesRDF -0 0 -f . -b 0 -l 10` |
| Run on batch | `mkShapesRDF -o 0 -f . -b 1` |
| Check finished jobs | `mkShapesRDF -o 1 -f .` |
| Resubmit failed jobs | `mkShapesRDF -0 1 -f . -r 1` |
| Merge ROOT files | `mkShapesRDF -o 2 -f .` |
| Available arguments | `mkShapesRDF --help` |

Always modify, compile, test locally with 10 events (to make sure you don't run unnecesarily 
in HTCondor, submit to batch, check the jobs, and merge in that order. Compilation is required 
after every configuration change.

A better alternative to check on the running jobs is to use the `doCheck.py` script within each folder

```bash
python3 doCheck.py
```

The key diffence is that `mkShapesRDF -o 1 -f .` checks if any job gave unexpected errors/warnings in 
the log.txt files, wherease `python3 doCheck.py` checks if the outputs have been created. The latter is 
usually preferred.

### IMPORTANT: If some samples are not running, make sure that you have rights to access all files defined in `samples.py`, both signals and backgrounds.

## 4. Check job status

```bash
condor_q
```

Cancel one cluster with `condor_rm <ClusterId>`. Cancel all your running jobs only when
intended:

```bash
condor_rm -all
```

If jobs have been stuck for a while in HTCondor, you can run:

```bash
myschedd bump
```
which will change to a less crowded pool of jobs (you will have to submit the jobs again, tho)

## 5. Plot

To run the whole plotting pipeline, run:

```bash
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
```

## 6. Share on the web

If the `plotPath` in the configuration.py file is aiming to your `/eos/user/x/x/www/` folder, you will be able to see your plots on the web:

Enable your [CERN webEOS area](https://resources-portal.web.cern.ch/service/website-and-application-hosting) and add the standard index file if this is your first time.
