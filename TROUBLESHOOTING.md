# Troubleshooting

## “I edited a cut but nothing changed”
Recompile:

```bash
mkShapesRDF -c 1
```

Then make a short local test. mkShapesRDF normally runs from the compiled configuration, not directly from the freshly edited source file.

## `use of undeclared identifier ...`
Usually one of:

1. alias dependency defined after use;
2. C++ macro was not included;
3. shared library was not loaded;
4. object/function name differs from the C++ definition;
5. expression is evaluated in a phase where the helper is not available.

Search the name everywhere:

```bash
grep -R "IdentifierName" -n .
```

## Missing ROOT column
Check spelling and campaign/NanoAOD version. A branch available in one production may not exist in another. Also check whether the name is supposed to be an alias rather than a physical branch.

## “Argument list too long”
The shell expanded too many pathnames before running the command. Prefer tools that traverse internally, for example:

```bash
find <directory> -maxdepth 1 -type f
```

rather than `ls <directory>/*` for huge directories.

## Jobs finish but merge is missing samples
Check job outputs, not only Condor state. A batch job can leave the queue without producing a valid ROOT file. Use the framework check and any analysis `doCheck.py` helper before merging.

## Batch works differently from local
Look for absolute paths, local-only files, uncompiled `.so` libraries, model files. Batch workers do not magically see arbitrary files from your lxplus working directory unless the framework transfers them or they are on a shared filesystem.

## B-tag SF errors

Verify the compiled `evaluate_btagSF*_cc.so` exists and `analysisRoot` resolves where expected.

## Combine command cannot find `HiggsAnalysis`
You are probably outside the intended CMSSW runtime or Combine is not installed/built in that release area. Enter the CMSSW `src`, run `cmsenv`, then verify the expected package path/build.
