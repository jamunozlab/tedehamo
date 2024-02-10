# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 09:08:38 2022

@author: Cesar Diaz-Caraveo, Jorge Muñoz
cdiazcarav@miners.utep.edu, cesar.dc1509@gmail.com
jamunoz@utep.edu

The University of Texas at El Paso

Code created as part of the scripts needed for writing the paper 
"Finite-temperature free energies of bcc-based Fe-V alloys with thermal and 
chemical disorder from molecular dynamics" 

The program reads the values of the errors given by the Birch-Murnaghan fit 
equation for the bulk modulus, bulk modulus derivative, lattice parameter, and 
minimum internal energy of the system. This is based out of reading excel files
that export the error in the "EoS Birch-Murnaghan.py" code for getting the fit 
to this equation. 

The list of vanadium compositions in for directory accesing needs to be changed
acoording to the compositions found in the directory, as well as the arrmt 
variable for output labling purposes.

"""

import numpy as np 
import os
import pandas as pd
import matplotlib.pyplot as plt


vanadium_compositions = [0.125, 0.25, 0.5, 0.75, 0.875, 1]
errors_array = np.empty((0, 5))
params_array = np.empty((0, 5))

temperature = 1300 # K, value for naming outputs
arrmt = 'Ordered' # arrmt - short for arrangement

#%% Reading the energies from the specified Lattice Parameters directories

for vanadium_composition in vanadium_compositions:
    
    # Defining the list of directories to read the energies from
    sub_directory = 'Fe{}V{}'.format((1-vanadium_composition), vanadium_composition)
    parent_dir = os.getcwd()
    
    new_directory = os.path.join(parent_dir, sub_directory)
    os.chdir(new_directory)
    
    df_name = "Errors and Parameters Birch Murnaghan {}.csv".format(vanadium_composition)
    
    df_input = pd.read_csv(df_name)
    params = np.array(df_input.loc[:, "Value"]).transpose()
    errors = np.array(df_input.loc[:, "Error"]).transpose()
    
    errors_array = np.vstack([errors_array, errors])
    params_array = np.vstack([params_array, params])
    
    os.chdir(parent_dir)


print(params_array)
print(params.shape)
print(errors_array)
print(errors.shape)

df_params = pd.DataFrame(params_array, index = vanadium_compositions, 
                         columns = ('E0','V0','B0','B0p','L0'))
df_errors = pd.DataFrame(errors_array, index = vanadium_compositions,
                         columns = ('E0','V0','B0','B0p','L0'))

df_params.to_csv('Birch-Murnaghan parameters {} K - '.format(temperature) + arrmt + '.csv')
df_errors.to_csv('Birch-Murnaghan errors {} K - '.format(temperature) + arrmt + '.csv')
