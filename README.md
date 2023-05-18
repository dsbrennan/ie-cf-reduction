# IE CF Reduction
This repository has been setup to contain an initial implementation of the Irreducible Element (IE) model Canonical Form (CF) reduction rules. 

The CF reduction rules were initially introduced in our ISMA 2022 paper as part of the Calculating structural similarity series:

> Daniel S. Brennan, Timothy J. Rogers, Elizabeth J. Cross, Keith Worden.  Calculating structure similarity via a Graph Neural Network in Population-based Structural Health Monitoring, ISMA 2022.

If you would like to find more information around the CF reduction rules, please read the ISMA 2022 paper.

The code within this repository, was initially built for our IWSHM 2023 paper. If you use any of the code from within this repository in an academic setting or paper, please cite the following paper:

> Daniel S. Brennan, Elizabeth J. Cross, Keith Worden. A comparison of structural similarity methodologies within Population-based Structural Health Monitoring, IWSHM 2023.

## Installation
You can install the repository using pip
```
pip install git+https://github.com/dsbrennan/ie-cf-reduction
```

## Using the Reduction Rules
To use the reduction rules code, simply call the static reduce_graph method within the CanonicalFormReduction class:

```python
from canonical_form_reduction import CanonicalFormReduction as cfr
cfr.reduce_graph(elements, relationships)
```
The method takes three arguments:
* elements: a list of IE model element objects
* relationships: a list of IE model relationship objects
* debug: output diagnostic information (true/false)
