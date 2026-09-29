# 01 — Making it run

## Goal

This module has one purpose: **make a small but realistic mkShapesRDF configuration run from beginning to end**.

You will produce histograms in three deliberately simple regions:

- `DYtautauCR`: an opposite-sign (e\mu) control region with low dilepton transverse momentum, low dilepton mass, and a b-jet veto;

- `WWSR`: an opposite-sign (e\mu) region with (m_{\ell\ell} > 85) GeV and a b-jet veto;

- `Top_CR`: an opposite-sign (e\mu) control region with (m_{\ell\ell} > 85) GeV and at least one b-tagged jet.

Each region is further split into simple jet-multiplicity categories.

The configuration already contains the normal analysis machinery: **real data, a nonprompt/fake estimate, lepton working points and scale factors, trigger weights, b-tagging efficiencies and scale factors, and `nuisances.py`**.

---

# mkShapesRDF documentation

### Useful links

- [mkShapesRDF repository](https://github.com/latinos/mkShapesRDF)
- [PlotsConfigurationsRun3 repository](https://github.com/latinos/PlotsConfigurationsRun3)
- [mkShapesRDF documentation](https://mkshapesrdf.readthedocs.io/)
- [mkShapesRDF tutorial slides](https://docs.google.com/presentation/d/1UlJUYIIA2-Kbpj_wDD4EKDMNEH01GeI-9GDHDYxhfpI/edit?slide=id.g2df8cadc7b0_0_269#slide=id.g2df8cadc7b0_0_269)
- [CMS NanoAOD content documentation](https://cms-xpog.docs.cern.ch/autoDoc/)
- [HTCondor documentation](https://htcondor.readthedocs.io/)

## 1. Install mkShapesRDF

Log into lxplus:

```bash
ssh -Y <username>@lxplus.cern.ch -o ServerAliveInterval=240
```

Command by command:

- `ssh`: start a remote shell session;
- `-o ServerAliveInterval=240`: send a keep-alive every 240 s so idle connections are less likely to die.

Clone and install the framework:

```bash
git clone https://github.com/latinos/mkShapesRDF.git
cd mkShapesRDF
./install.sh
```

You only install once. In later sessions you only activate the environment.

---

## 2. Start a working session

```bash
cd <working-directory>/mkShapesRDF
source start.sh
cd <path-to-this-repository>/01_making_it_run/Full2022v12
```

`source start.sh` changes the current shell environment: Python paths, ROOT-related paths and the command-line programs such as `mkShapesRDF` become available in **this terminal**.

Check that the command exists:

```bash
which mkShapesRDF
mkShapesRDF --help
```

---

## 3. Know the eight files

For now, remember only this:

| File | Meaning |
|---|---|
| `configuration.py` | connects the other files and chooses output paths |
| `samples.py` | chooses input datasets and weights |
| `aliases.py` | defines derived quantities and analysis corrections; leave it alone for now |
| `cuts.py` | defines the regions |
| `variables.py` | defines histograms |
| `plot.py` | styles/groups processes |
| `nuisances.py` | systematic uncertainties; already active, but explained later |
| `structure.py` | marks backgrounds, fake estimate and data for statistical tools |

---

## 4. Compile the configuration

Before starting, make sure all the dependencies in `../extended` are properly compiled. To do this, run:
```bash
root <file>.cc+
```
If 'undeclared' errors arise, ignore :)

Run:

```bash
mkShapesRDF -c 1
```

Meaning:

- `-c 1`: compile/read the configuration files and build the executable configuration stored in `configs/`.

Run this again **after every change to the configuration**. If you edit `cuts.py` and then run old compiled files, your edit will not be used.

Inspect what appeared:

---

## 5. Always make a tiny local test first

```bash
mkShapesRDF -o 0 -f . -b 0 -l 10
```

Breakdown:

- `-o 0`: execute the shape-production operation;
- `-f .`: use the configuration in the current directory (`.` means “here”);
- `-b 0`: do **not** send jobs to HTCondor; run locally;
- `-l 10`: process only 10 events per task, which makes this a syntax/runtime smoke test.

This is just to know “does the complete configuration compile and execute?” The smoke test therefore also catches problems in fake weights, b-tag SF code, data definitions and nuisance expressions even though those topics have not been taught yet.

If this fails, fix it **before** submitting hundreds of batch jobs.

---

## 6. Submit the real production to HTCondor

```bash
mkShapesRDF -o 0 -f . -b 1
```

The only important change is:

- `-b 1`: create and submit batch jobs instead of running them in your interactive lxplus process.

Useful related commands:

```bash
condor_q
condor_rm <ClusterId>
```

- `condor_q`: show your running jobs;
- `condor_rm <ClusterId>`: cancel one submitted cluster. Do not use `condor_rm -all` unless you really intend to cancel everything.

NOTE: If at some point your jobs are stuck for a while, you can change pool of jobs with:

```bash
myschedd bump
```

---

## 7. Check jobs

After jobs have run:

```bash
mkShapesRDF -o 1 -f .
```

This asks mkShapesRDF to inspect the batch production and report failures/warnings found in the logs.

If failed jobs should be resubmitted:

```bash
mkShapesRDF -o 1 -f . -r 1
```

Here `-r 1` means resubmit the failed tasks identified by the check operation.

Do **not** merge first and hope missing jobs do not matter. Check the production before merging.
Another way to check this is to use the `doCheck.py` file, using:
```bash
python3 doCheck.py
```
This just checks if an output for each sample exists, which is usually more handy.

---

## 8. Merge the job outputs

```bash
mkShapesRDF -o 2 -f .
```

`-o 2` merges the many per-job ROOT files into the analysis ROOT output configured by `outputFile`/`outputFolder` in `configuration.py`.

A common workflow is therefore:

```bash
mkShapesRDF -c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
mkShapesRDF -o 0 -f . -b 1
mkShapesRDF -o 1 -f .
mkShapesRDF -o 2 -f .
```

---

## 9. Make plots

```bash
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
```

- `mkPlot`: read the merged histograms and apply `plot.py`;
- `--onlyPlot cratio`: make the standard comparison/ratio-style plot;
- `--showIntegralLegend 1`: print process number of events in the legend;
- `--fileFormats png`: save only PNG files.

The output location comes from `plotPath` in `configuration.py`.

---

