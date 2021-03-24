Tests passing:
[![Python Testing](https://github.com/WYVERN2742/pl_curves/actions/workflows/main.yml/badge.svg)](https://github.com/WYVERN2742/pl_curves/actions/workflows/main.yml)

Code coverage:
[![codecov](https://codecov.io/gh/WYVERN2742/pl_curves/branch/master/graph/badge.svg)](https://codecov.io/gh/WYVERN2742/pl_curves)

# Introduction

This program calculates Pareto–Lorenz (PL) curves for calculating the relative abundance of different bacteria in a community. It also calculates a Gini coefficient to show how evenly distributed the different bacteria are. There are tests written for most functions. Your task is to:

1. Fork this repository
2. Fix the badge path and test github actions
    * Edit the URL at the top of this file to be your repository, not CDT-AIMLAC or:
      * Click on the actions tab and choose the "Python testing" workflow.
      * Press the 3 horizontal dots on left side and click "Create status badge".
      * Copy the markdown and replace the code on line 2 of this file with it.
    * Commiting a change to this file will cause the Github Actions to run.
    * The first run will take a few minutes to start, subsequent runs should be quicker. The first run will also fail due to some broken tests. Sometimes it will timeout when installing the dependencies, if this happens rerun it manually.
3. Setup codecov.io
   Codecov.io reports the test coverage percentage. Github Actions can produce and push reports to codecov. You need to create an account linked to your github page at https://codecov.io/login/gh.
   * Click on your user name and choose "add repository"
   * Find the pl_curves repository and go to Settings->Badge, copy the markdown and replace the codecov badge link on line 4 of this file.
4. Fix the broken tests.
5. Add python 3.7 and 3.8 as target languages in the .github/workflows/main.yml file, fix any errors which result from this.
6. Upgrade the operating system being tested from Ubuntu 18.04 to Ubuntu 20.04.
7. Upgrade to the most recent version of Pandas and see what breaks.
8. (optional) send a pull request to the original repository (https://github.com/colinsauze/pl_curves) with your fixes and improvements.


# Purpose

This code implements the method described in the following papers:

Possible interactions between bacterial diversity, microbial activity and
supraglacial hydrology of cryoconite holes in Svalbard" by Arwyn Edwards,
Alexandre M Anesio, Sara M Rassner, Birgit Sattler, Bryn Hubbard, William T
Perkins, Michael Young & Gareth W Griffith in The ISME Journal volume 5,
pages 150–160 (2011)
https://www.nature.com/articles/ismej2010100

and

Can the Bacterial Community of a
High Arctic Glacier Surface Escape Viral Control?" by Sara M. E. Rassner,
Alexandre M. Anesio, Susan E. Girdwood, Katherina Hell, Jarishma K. Gokul,
David E. Whitworth and Arwyn Edwards in Frontiers in Microbiology 21 June 2016
https://doi.org/10.3389/fmicb.2016.00956

## Citing this software

If you are using this software in an academic paper then please cite it. A machine readable citation.cff file and BibTex (citation.bib) file can also be found in this repository.

Colin Sauze and Sara Rassner, 2019, "PA script for generating Pareto–Lorenz (PL) curves", https://10.5281/zenodo.2630659

[![DOI](https://zenodo.org/badge/177189416.svg)](https://zenodo.org/badge/latestdoi/177189416)
