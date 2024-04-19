# -*- coding: utf-8 -*-
"""

@authors: Cesar Diaz-Caraveo, Jorge Muñoz
cdiazcarav@miners.utep.edu, cesar.dc1509@gmail.com
jamunoz@utep.edu

The University of Texas at El Paso

The following program is used to generate multiple LAMMPS simulations
automatically, increasing the lattice parameter each time by a desired amount.
It uses the os library to send the input files into the terminal, creates a new 
directory for each lattice parameter, and copies the potential and input files 
to each of these new directories. As intial parameters for the simulation, you 
have the vanadium composition, and intial lattice parameter value.

Compared to previous order and disordered compositions generators, this program
introduces a finite amount of defects in a disordered B2 lattice, specified by
the user via the defect percentage value (percentage relative to the total
atoms in the simulation)

"""

import numpy as np
import os
import shutil
import pandas as pd


#%% Location of potential and input files - name input by user
#   Input file must follow the template found in the GitHub repository, and 
#   it needs to be modified depending on the temperature, simulation duration, 
#   and dumping of output values.

file_directory = "C:/Users/cdiazcarav/OneDrive - University of Texas at El Paso/Documents/AA - UTEP/Munoz team/PRM Paper/MD Simulations at 1300K/"

#%% Lattice parameters list definition and iteration

lattice_parameters = []
vanadium_composition = 0.5
lattice_value_for = 2.81

for i in range(39):
    lattice_parameters.append(lattice_value_for)
    lattice_value_for += 0.01

#%% Size of the system cell in unit cells, assuming a cubic cell, starting at the origin
system_size = 20

#%% Amount of order defects/swaps introduced in the simulation
total_atoms = 2 * (system_size ** 3)

defect_percentage = 5
total_order_defects = int(total_atoms*defect_percentage/100)

#%% Array for randomly selected swaps
range_total_atoms = np.arange(1, total_atoms + 1)
random_defects_array = np.random.choice(range_total_atoms, total_order_defects, 
                                                replace=False)
print(np.sort(random_defects_array))
#print(len(random_defects_array))

df_random_positions = pd.DataFrame(random_defects_array)

#%% Array of 1s and 2s for initial B2 ordered structure
atom_type_array = np.zeros((total_atoms))

for i in range(total_atoms):
    if ((i+1) % 2 == 0):
        atom_type_array[i] = 2
    else:
        atom_type_array[i] = 1

#%% Swaps in B2 structure
for i in random_defects_array:
    if(atom_type_array[i-1] == 1):
        atom_type_array[i-1] = 2 
    else:
        atom_type_array[i-1] = 1

# Computing composition of type two atom
total_atoms_2 = 0

for i in range(total_atoms):
    if atom_type_array[i] == 2:
        total_atoms_2 += 1

composition = total_atoms_2/total_atoms
print(composition)

#%% Calculates the directory for each lattice parameter, creates the atoms' 
#   positions, and runs the simulations 

for lattice_parameter in lattice_parameters:
    
    # Defining unit cell
    basis = np.array([[0.5, 0.0, 0.0], 
                      [0.0, 0.5, 0.0],
                      [0.0, 0.0, 0.5]])*lattice_parameter
    
    base_atoms = np.array([[0.0, 0.0, 0.0], 
                           [0.5, 0.5, 0.5]])*lattice_parameter
    
    # Generate atom positions
    positions = []
    for i in range(system_size):
        for j in range(system_size):
            for k in range(system_size):
                base_position = np.array([i, j, k])
                cart_position = np.inner(basis.T, base_position)
                for atom in base_atoms:
                    positions.append(cart_position + atom)
    
    sub_directory = 'Simulation_Lattice_{}'.format(round(lattice_parameter, 2))
    parent_dir = os.getcwd()
    
    new_directory = os.path.join(parent_dir, sub_directory)
    os.makedirs(new_directory)
    
    os.chdir(new_directory)
    
    # Copies potentials and input files to each of the directories
    
    potential_library_dest = os.path.join(new_directory, "FeV.library.meam")
    shutil.copy(file_directory+"FeV.library.meam", potential_library_dest)
    
    potential_FeV_dest = os.path.join(new_directory, "FeV.meam")
    shutil.copy(file_directory+"FeV.meam", potential_FeV_dest)
    
    input_file_dest = os.path.join(new_directory, "FeV_external_positions_input_file.in")
    shutil.copy(file_directory+"FeV_external_positions_input_file.in", input_file_dest)
    
    # Writing positions and atom information into .data file
    with open('atoms_positions.data', 'w') as fdata:
            #-----Header-----#
            # Specify number of atoms and atom types
            fdata.write('# lattice parameter {} \n \n'.format(round(lattice_parameter, 2)))
            fdata.write('# atom type 2 composition {} \n \n'.format(round(composition, 4)))
            fdata.write('{} atoms\n'.format(len(positions)))
            fdata.write('{} atom types\n'.format(2))
            
            # Specify box dimensions
            fdata.write('{} {} xlo xhi\n'.format(0.0, system_size*lattice_parameter))
            fdata.write('{} {} ylo yhi\n'.format(0.0, system_size*lattice_parameter))
            fdata.write('{} {} zlo zhi\n'.format(0.0, system_size*lattice_parameter))
            fdata.write('\n')
            
            # Atoms section
            fdata.write('Atoms\n\n')
            
            # Write each position
            for i,pos in enumerate(positions):
                if atom_type_array[i] == 2:
                    fdata.write('{} 2 {} {} {}\n'.format(i+1, *pos))
                    total_atoms_2 += 1
                else:
                    fdata.write('{} 1 {} {} {}\n'.format(i+1, *pos))
    
    os.popen("lammps-shell.exe -in FeV_external_positions_input_file.in")
    
    os.chdir(parent_dir)
