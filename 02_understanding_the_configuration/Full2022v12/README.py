## Configuration files

The analysis configuration is split across several Python files, each with a specific role:

- `aliases.py`  
  Defines derived quantities, helper expressions, and custom C++/Python calculations that are not stored directly in NanoAOD during our post-processing step. These aliases can then be used in selections and histogram definitions.

- `configuration.py`  
  Main steering file for the analysis. It connects the different configuration components and defines the general execution setup.

- `cuts.py`  
  Defines the event selections and analysis regions, including the preselection and the different signal/control categories.
   - Signal Region (SR): region optimized to enhance the expected signal relative to the background.
   - Control Region (CR): region enriched in a specific background, used to validate or constrain its prediction.

- `doCheck.py`  
  Auxiliary script used to perform consistency checks on the analysis setup or produced outputs.

- `nuisances.py`  
  Defines a reduced set of systematic uncertainties for checking purposed.

- `nuisances_ALL.py`  
  Extended nuisance configuration containing the full set of available systematic uncertainties.

- `plot.py`  
  Defines how samples are displayed in plots, including labels, colors, signal/background grouping, plotting order, and legend configuration. This is following the latest recommendations on accesible/inclusive color schemes: [arXiv:2107.02270](https://arxiv.org/abs/2107.02270)

- `samples.py`  
  Defines the datasets used in the analysis, including signal, background, and data samples, together with their corresponding files and sample-specific weights.

- `structure.py`  
  Defines how each process is interpreted when producing datacards, for example whether it is signal, background, or data.

- `variables.py`  
  Defines the histograms produced by the analysis, including the variable expression, binning, axis label, and overflow/underflow handling.
