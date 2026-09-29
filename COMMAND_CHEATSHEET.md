# Command cheat sheet

## Session

```bash
ssh -Y -l <username> lxplus.cern.ch -o ServerAliveInterval=240
cd <working-directory>/mkShapesRDF
source start.sh
cd <configuration-folder>
```

## Core mkShapesRDF cycle

```bash
mkShapesRDF -c 1                       # compile configuration
mkShapesRDF -o 0 -f . -b 0 -l 10     # tiny local smoke test
mkShapesRDF -o 0 -f . -b 1           # submit shape production to HTCondor
mkShapesRDF -o 1 -f .                 # inspect/check submitted production
mkShapesRDF -o 1 -f . -r 1           # resubmit failures found by check
mkShapesRDF -o 2 -f .                 # merge successful job ROOT files
mkShapesRDF --help                    # authoritative options for this install
```

## Batch

```bash
condor_q
condor_q <username>
condor_rm <ClusterId>
```

## Plotting

```bash
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
```

## Search/debug configuration

```bash
grep -R "NAME" -n --include='*.py' .
grep -n "PATTERN" file.py
less file.py
diff -u old.py new.py | less
```

## Compile ROOT helpers

```bash
root -l -b -q 'helper.cc++'
```

## Theory/statistical scripts

```bash
python3 mkTheoryNormalizations.py --help
python3 mkDatacards_topDM.py --help
python3 limits/mk_Limits.py --help
```

## Golden rule

After changing any configuration input:

```bash
mkShapesRDF -c 1
mkShapesRDF -o 0 -f . -b 0 -l 10
```
