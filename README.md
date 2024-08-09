# Temperature-Dependent Harmonic Model (TDHM)

Welcome to TDHM, a simulation framework for computing the thermodynamic quantities and lattice dynamics of a system from molecular dynamics simulations in LAMMPS designed to study the combined effects of composition, chemical disorder, and finite temperature in binary alloys.

The set of Python codes in this repository is a comprehensive pipeline for sending multiple LAMMPS simulations for a given binary system, returning an internal energy vs volume curve for each composition of interest. After that, a fit from the Birch-Murgnagham equation of state is used to determine the lattice parameter, internal energy, bulk modulus, and bulk modulus derivative of the given composition based on the minimum internal energy value for the energy vs volume curve. The free energy of the system is then determined along with the Debye temperature and vibrational entropy functions using the Debye-Grüneisen lattice dynamics model and the Moruzzi-Janak-Schwarz (MJS) approximation for the vibrational entropy. 

The following are recorded YouTube tutorials that describe in detail how to use the whole simulation framework. Any questions or concerns can be addressed at jamunoz@utep.edu.

Tutorial #1 - Data Generation: https://www.youtube.com/channel/UCGrdCKajVVovcQkxH6rxs4A
Tutorial #2 - Post-Processing 1, Birch-Murnaghan fit: https://www.youtube.com/watch?v=9LGG5dRJ_g4&t=11s
Tutorial #3 - Post-Processing 2, Debye temperature, vibrational entropy, and free energy: https://www.youtube.com/watch?v=5COlzVsCl2M

The directory Data contains the data reported for the thermodynamic quantities in Figs. 2 and 3 of Ref. 1, for ordered (B2) and disordered (A2) simulations.  

References:
[1] Diaz-Caraveo, C., KC, B., and Muñoz San Martín, J. "Lattice dynamics and free energies of Fe-V alloys with thermal and chemical disorder." Journal of Physics: Condensed Matter (2024).
