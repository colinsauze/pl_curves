[![Python Testing](https://github.com/colinsauze/pl_curves/actions/workflows/main.yml/badge.svg)](https://github.com/colinsauze/pl_curves/actions/workflows/main.yml)

# Introduction

A program for graphically describing the evenness of bacterial communities using
 Pareto–Lorenz (PL) curves, by plotting the cumulative relative abundance 
against the cumulative proportion of each taxonomical bins (based on e.g. T-RFs
, OTUs). The more the plotted line deviates from the 1:1 line (45° diagonal), 
the lower the evenness of the community.

For each sample individually, empty bins are removed and the remaining bins are
 sorted in decreasing order of relative abundance. The cumulative relative 
abundance (range 0-1) and cumulative proportion of bins (range 0-1) are 
calculated and the data plotted so that the first (left most) data point 
represents the contribution of the bin with the highest relative abundance. 
Data for all samples in the imported data set are plotted on the same graph, 
to facilitate comparisons between samples. 

The program also calculates the Gini-coefficient for each community, which 
describes the evenness of a community as the ratio of the area between the PL 
curve and the equality line and the whole triangular area above the equality 
line. The Gini coefficient ranges from 0 (perfect evenness) to 1 (perfect 
unevenness). The reported Gini coefficient has been corrected for the number 
of taxonomical units in the sample by multiplying the ratio with n/(n-1).

This implements the method described in the following papers:


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


## Build Status

This software is automatically tested by Travis-CI after each build. Its current status is shown below:
[![Build status](https://travis-ci.org/colinsauze/pl_curves.svg?branch=master)](https://travis-ci.org/colinsauze/pl_curves)

[![codecov](https://codecov.io/gh/colinsauze/pl_curves/branch/master/graph/badge.svg)](https://codecov.io/gh/colinsauze/pl_curves)


