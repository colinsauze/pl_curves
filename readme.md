This software is automatically tested by Travis-CI after each build. Its current status is shown below:
![Build status](https://travis-ci.org/cdt-aimlac/pl_curves.svg?branch=master)

# Introduction

This program calculates Pareto–Lorenz (PL) curves for calculating the relative abundance of different bacteria in a community. It also calculates a Gini coefficient to show how evenly distributed the different bacteria are. There are tests written for most functions. Your task is to:

1. Fork this repository
2. If you don't already have one, create a travis-ci (https://travis-ci.org/) account. Sign in with your github to this.
3. Add a new repository in Travis by clicking on the + button 
4. You should now be able to view the state of each build on the Travis webpage. Every push to the repository will trigger Travis to rebuild.
5. There is a link to a badge automatically produced by Travis at the top of this readme file, you will need to update this to the address of your own repository.
6. Fix the broken tests.
7. Add python 3.8 as a target language in the .travis.yml file, fix any errors which result from this.

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


