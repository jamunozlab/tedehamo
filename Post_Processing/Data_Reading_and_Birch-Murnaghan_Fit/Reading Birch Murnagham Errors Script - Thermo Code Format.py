# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 09:08:38 2022

@author: Cesar Diaz
cdiazcarav@miners.utep.edu
cesar.dc1509@gmail.com

The University of Texas at El Paso

Code created as part of the scripts needed for writing the paper "Computational
Determination of the Metastable FeV phase diagram" 

The program reads the values of the errors given by the Birch-Murnaghan fit 
equation for the bulk modulus, bulk modulus derivative, lattice parameter, and 
minimum internal energy of the system. This is based out of reading excel files
that export the error in the "EoS Birch-Murnaghan.py" code for getting the fit 
to this equation. 

"""

import numpy as np 
import os
import pandas as pd
import matplotlib.pyplot as plt
import math


compositions = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
output_array = np.empty((0, 11))

temp = 1300 # K, value for naming outputs
arrmt = 'Random' # arrmt - short for arrangement
prefix = 'dis' # for output labling in format for thermo code

def conf_entropy_calculation(comp):
    return -1*comp*math.log(comp) + (1-comp)*math.log(1-comp)

#%% Reading the energies from the specified Lattice Parameters directories

for comp in compositions:
    
    # Defining the list of directories to read the energies from
    sub_directory = 'Fe{}V{}'.format((1-comp), comp)
    parent_dir = os.getcwd()
    
    new_directory = os.path.join(parent_dir, sub_directory)
    os.chdir(new_directory)
    
    df_name = "Errors and Parameters Birch Murnaghan {}.csv".format(comp)
    
    df_input = pd.read_csv(df_name)
    params = np.array(df_input.loc[:, "Value"]).transpose()
    errors = np.array(df_input.loc[:, "Error"]).transpose()
    
    row_output = []
    
    # Appending to list parameters and errors for each quantity alternated
    for i in range(len(params)):
        row_output.append(params[i])
        row_output.append(errors[i])
    
    # Appending configurational entropy
    row_output.append(conf_entropy_calculation(comp))
    
    output_array = np.vstack([output_array, np.array(row_output)])
    
    os.chdir(parent_dir)


columns = ("internal_energy_{}K_{}".format(temp, prefix), 
           "internal_energy_{}K_{}_error".format(temp, prefix),
           "volume_{}K_{}".format(temp, prefix),
           "volume_{}K_{}_error".format(temp, prefix),
           "bulk_modulus_{}K_{}".format(temp, prefix),
           "bulk_modulus_{}K_{}_error".format(temp, prefix),
           "bulk_modulus_derivative_{}K_{}".format(temp, prefix),
           "bulk_modulus_derivative_{}K_{}_error".format(temp, prefix),
           "lattice_parameter_{}K_{}".format(temp, prefix),
           "lattice_parameter_{}K_{}_error".format(temp, prefix),
           "configurational_entropy_{}K_{}".format(temp, prefix))

df_output = pd.DataFrame(output_array, index = compositions, columns = columns)

df_output.to_csv('Birch-Murnaghan errors and parameters {} K - '.format(temp) + arrmt + '.csv')