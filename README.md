# `FrescoConstructor`
This program is used for constructing [`FRESCO`](http://www.fresco.org.uk/) coupled-channel reaction code inputs for (d,p) reactions in inverse kinematics.

## Running the code
`FrescoConstructor` is built in Python. Simply run the program via
```
python FrescoConstructor.py
```
The Python program requires user inputs such as element, mass number, beam energy, etc. 

Alternatively, the Jupyter Notebook `FrescoConstructor.ipynb` can be used. The notebook contains more information about the functions and calculations used in the `FrescoConstructor` program.

## Assumptions for `FrescoConstructor`
`FrescoConstructor` works under the following assumptions:

* The reaction is a (d,p) reaction being run in inverse kinematics
* The reaction is populating a single-particle neutron orbital via a single-step reaction mechanism

## Optical Model Potentials
`FrescoConstructor` currently offers a single neutron potential and two proton and deuteron potentials. These potentials are global potentials that generally suite medium-mass beams. The user is advised to check that these potentials are valid for their use case before running `FRESCO` calculations.

### Neutron Potential
The neutron potential used is that of D. Wilmore and P.E. Hodgson ([Nuclear Physics 55:673-694 (1964)](https://doi.org/10.1016/0029-5582(64)90184-1))

### Proton Potential
Two possible proton potentials are available for the `FrescoConstructor` program:

* The Becchetti and Greenless (BG) global proton potential ([Phys. Rev. 182:1190-1209 (1969)](https://doi.org/10.1103/PhysRev.182.1190))
* The Perey (P) global proton potential ([Phys. Rev. 131:745-763 (1963)](https://doi.org/10.1103/PhysRev.131.745))

The BG proton potential is the default potential used in `FrescoConstructor`.

### Deuteron Potential
Two possible deuteron potentials are available for the `FrescoConstructor` program:

* The Lohr and Haeberli (LH) global deuteron potential ([Nuclear Physics A, 232(2):381-397 (1974)](https://doi.org/10.1016/0375-9474(74)90627-7)
* The Daehnick global deuteron potential ([Phys. Rev. C 21:2253-2274 (1980)](https://doi.org/10.1103/PhysRevC.21.2253)

The LH deuteron potential is the default potential used in `FrescoConstructor`.
