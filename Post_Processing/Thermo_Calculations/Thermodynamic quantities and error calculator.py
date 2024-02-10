# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 19:46:44 2023

@author: Cesar Diaz-Caraveo, Jorge Muñoz
cdiazcarav@miners.utep.edu, cesar.dc1509@gmail.com, jamunoz@utep.edu

The University of Texas at El Paso

Code written as part of the computations required for the paper "Computational
Prediction of the Metastable Fe-V phase diagram". The code caluclates the 
Debye temperature, vibrational entropy and free energy for each temperature 
and order state passed to the system. The code also determines numerically 
the error range for the vibrational entropy, debye temperature, and free energy 
(target quantities), based on the standard deviation and mean value for the 
lattice parameter, bulk modulus, and internal energy. This is done by 
calculating the target quantities a certain predetermined number of times and 
using the resulting data for calculating the mean and standard deviation of 
each composition.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def error_calculation(suffix, temp):
    
    df = pd.read_csv('Fe-V' + suffix + '.csv')
    temp_num = temp
    
    columns = ['lattice_parameter', 'bulk_modulus', 'atomic_mass', 'debye_temperature', 
               'entropy', 'internal_energy', 'configurational_entropy', 'free_energy']
    temp = '_' + str(temp_num) + 'K'
    print(temp)
    
    # Creating a column dictionary for the specific columns of the given 
    # temperature and suffix
    cdict = {}
    for column in columns:
        cdict[column] = column + temp + suffix
        #print(cdict[column])
    
    #print(cdict)
    
    compositions = np.array(df["V_composition"])
    compositions = compositions.reshape((len(compositions), 1))
    
    # Computing random quantities for each of the compositions the given number 
    # of times in iterations - used for determining standard deviation and mean
    # of debye temperature, entropy, and free energy
    iterations = 1000
    
    # Arrays for concatinating the output of each iteration (each set of random
    # quantities). Concatinated below in the for loops over the orizonal axis
    # with np.hstack
    debye_temp_values = np.empty((len(compositions), 0))
    vibrational_entropy_values = np.empty((len(compositions), 0))
    configurational_entropy_values = np.empty((len(compositions), 0))
    free_energy_values = np.empty((len(compositions), 0))
    
    for i in range(iterations):
        
        lattice_param_list = []
        bulk_modulus_list = []
        internal_energy_list = []
        
        for j in range(len(compositions)):
                        
            lattice_param_list.append(np.random.normal(loc = df.loc[j, cdict['lattice_parameter']], 
                                                  scale = df.loc[j, cdict['lattice_parameter']+"_error"]))
            #print(i)
            #print(lattice_param_list)
            #print()
            bulk_modulus_list.append(np.random.normal(loc = df.loc[j, cdict['bulk_modulus']], 
                                                  scale = df.loc[j, cdict['bulk_modulus']+"_error"]))
            internal_energy_list.append(np.random.normal(loc = df.loc[j, cdict['internal_energy']], 
                                                  scale = df.loc[j, cdict['internal_energy']+"_error"]))
        
        lattice_params = np.array(lattice_param_list).reshape((len(compositions), 1))
        bulk_modulus = np.array(bulk_modulus_list).reshape((len(compositions), 1))
        internal_energy = np.array(internal_energy_list).reshape((len(compositions), 1))
        
        thermo_array = np.hstack([df[["Fe_composition"]], compositions, lattice_params, 
                                  bulk_modulus, internal_energy, df[[cdict['configurational_entropy']]]])
        
        labels = ['Fe_composition', 'V_composition', cdict['lattice_parameter'], 
                  cdict['bulk_modulus'], cdict['internal_energy'], cdict['configurational_entropy']]
        
        df_thermo = pd.DataFrame(thermo_array, columns = labels)
        df_thermo.to_csv("df_thermo.csv")
        #print(df_thermo)
        
        Fe_composition = get_iron_composition(suffix, temp_num)
        # print(Fe_composition.values)
        
        # Output from below functions as pandas series. Converted to numpy arrays
        # for easier array and concatination manipulation
        debye_temp = np.array(calculate_debye_temperature(df_thermo, suffix, temp_num))
        vibrational_entropy = np.array(calculate_vibrational_entropy(df_thermo, suffix, temp_num))
        configurational_entropy = np.array(calculate_configurational_entropy(df_thermo, suffix, temp_num))
        free_energy = np.array(calculate_free_energy(df_thermo, suffix, temp_num))
        
        # Reshaping arrays for horizontal concatination
        debye_temp = debye_temp.reshape((len(debye_temp), 1))
        vibrational_entropy = vibrational_entropy.reshape((len(vibrational_entropy), 1))
        configurational_entropy = configurational_entropy.reshape((len(configurational_entropy), 1))
        free_energy = free_energy.reshape((len(free_energy), 1))
        
        # Concatinating arrays horizonally - random amounts of the quantities 
        # generated on each iteration
        debye_temp_values = np.hstack([debye_temp_values, debye_temp])
        vibrational_entropy_values = np.hstack([vibrational_entropy_values, vibrational_entropy])
        configurational_entropy_values = np.hstack([configurational_entropy_values, configurational_entropy])
        free_energy_values = np.hstack([free_energy_values, free_energy])
    
    
    # Creating column names for the output folder of all results in iterations
    debye_columns_output_all_data = []
    for i in range(iterations):
        name = "debye_random_" + str(temp_num) + "K" + suffix + "_" + str(i)
        debye_columns_output_all_data.append(name)
    
    v_entr_columns_output_all_data = []
    for i in range(iterations):
        name = "entropy_random_" + str(temp_num) + "K" + suffix + "_" + str(i)
        v_entr_columns_output_all_data.append(name)
    
    c_entr_columns_output_all_data = []
    for i in range(iterations):
        name = "configurational_entropy_random_" + str(temp_num) + "K" + suffix + "_" + str(i)
        c_entr_columns_output_all_data.append(name)
    
    free_energy_columns_output_all_data = []
    for i in range(iterations):
        name = "free_energy_random_" + str(temp_num) + "K" + suffix + "_" + str(i)
        free_energy_columns_output_all_data.append(name)
    
    # Creating data frames for the bulk of simulations and exporting data
    
    df_debye_temp = pd.DataFrame(debye_temp_values, index = df["V_composition"], 
                                 columns = debye_columns_output_all_data)
    df_debye_temp.to_csv('Debye temp array_{}_{}.csv'.format(temp, suffix))
    
    df_vib_entropy = pd.DataFrame(vibrational_entropy_values, index = df["V_composition"], 
                                  columns = v_entr_columns_output_all_data)
    df_vib_entropy.to_csv('Vibrational entropy_{}_{}.csv'.format(temp, suffix))
    
    df_conf_entropy = pd.DataFrame(configurational_entropy_values, index = df["V_composition"], 
                                   columns = c_entr_columns_output_all_data)
    df_conf_entropy.to_csv('Configurational entropy_{}_{}.csv'.format(temp, suffix))
    
    df_free_energy = pd.DataFrame(free_energy_values, index = df["V_composition"], 
                                  columns = free_energy_columns_output_all_data)
    df_free_energy.to_csv('Free energy_{}_{}.csv'.format(temp, suffix))
    
    df_dic = {"debye_temperature": df_debye_temp, "entropy": df_vib_entropy, 
              "configurational_entropy": df_conf_entropy, "free_energy": df_free_energy}
    #print(df_dic)
    
    df_output = calculate_statistics(df_dic, suffix, temp_num)
    #print(df_output)
    
    return df_output

def calculate_statistics(df_dic, suffix, temp):
    
    temp_num = temp
    
    columns = ['debye_temperature', 'entropy', 'configurational_entropy', 'free_energy']
    temp = '_' + str(temp_num) + 'K'
    
    # Creating a column dictionary for the specific columns of the given 
    # temperature and suffix
    cdict = {}
    for column in columns:
        cdict[column] = column + temp + suffix
        
    cdict_error = {}
    for column in columns:
        cdict_error[column] = column + temp + suffix + "_error"
        
    cdict_up = {}
    for column in columns:
        cdict_up[column] = column + temp + suffix + "_up"
        
    cdict_down = {}
    for column in columns:
        cdict_down[column] = column + temp + suffix + "_down"
        
    #print(cdict_error)
    
    compositions = df_dic[columns[0]].index
    df_output = pd.DataFrame(data = [], index = compositions)
    
    # Iterating for all quantities of interest, in this case stored in the 
    # columns list
    for column in columns:
        
        means_list = []
        stds_list = []
        
        # Iterating through each composition value for quantities of interest
        # calculating mean and standard deviation
        for i in range(len(df_dic[column].index)):
            mean = np.mean(df_dic[column].iloc[i, :])
            std = np.std(df_dic[column].iloc[i, :])
            
            means_list.append(mean)
            stds_list.append(std)
            
        #print(cdict[column])
        #print(cdict_error[column])
        df_output[cdict[column]] = means_list
        df_output[cdict_error[column]] = stds_list
        
        up_boundary_list = []
        down_boundary_list = []
        
        for i in range(len(means_list)):
            up = means_list[i] + stds_list[i]
            down = means_list[i] - stds_list[i]
            up_boundary_list.append(up)
            down_boundary_list.append(down)
        
        df_output[cdict_up[column]] = up_boundary_list
        df_output[cdict_down[column]] = down_boundary_list
        
    print(df_output.columns)
    
    return df_output

def calculate_free_energy(df, suffix, temp):
    
    temp_num = temp
    suffix = suffix #'_dis'
    
    collect_dict = {}
    
    columns = ['lattice_parameter', 'bulk_modulus', 'atomic_mass', 'debye_temperature', 'entropy', 'internal_energy', 'configurational_entropy', 'free_energy']
    temp = '_' + str(temp_num) + 'K'
    
    # Creating a column dictionary for the specific columns of the given 
    # temperature and suffix
    cdict = {}
    for column in columns:
        cdict[column] = column + temp + suffix
    
    def debye(theta, T):
        if T == 0: return 0
        df_dict = {}
        df_dict['x'] = pd.Series([i/100 for i in range(2000)])
        df_dict['y'] = pd.Series(df_dict['x'].apply(lambda x: x**3 / (np.exp(x) - 1)))
        df = pd.DataFrame(df_dict)
        x_D = theta/T

        return (3/(x_D**3)) * df.loc[df.x <= x_D].y.mul(1/100).sum()
    
    def debye2(theta, T):
        if T == 0: return 0
        x_D = theta/T
        return - np.log(1 - np.exp(-x_D))
    
    h = 4.135e-15 #eV times second
    k_B = 8.617e-5 # eV/K
    # constant = ((6 * np.pi**2)**(1/3)) * ((h)/( 2 * np.pi * k_B)) * ( ((4 * np.pi) / (3))**(1/6) ) * ( (1/2)**(1/6) ) # K times s
    # constant = ((6 * np.pi**2)**(1/3)) * ((h)/( 2 * np.pi * k_B)) * ( (1/2)**(1/6) ) # K times s
    # constant = ((6 * np.pi**2)**(1/3)) * ((h)/( 2 * np.pi * k_B)) * ( (1 / 2)**(1/6) )  # K times s
    constant = ((6 * np.pi**2)**(1/3)) * ((h)/( 2 * np.pi * k_B)) * ( ((4 * np.pi) / (3))**(1/6) )  # K times s
    
    
    df[cdict['atomic_mass']] = df['Fe_composition'].multiply(55.845-50.9415).add(50.9415).mul(1.66e-27)
        
    if(suffix == '_dis'):
        df[cdict['debye_temperature']] = df[cdict['lattice_parameter']].mul(1.0743e-10).mul(df[cdict['bulk_modulus']].mul(1e9)).div(df[cdict['atomic_mass']]).pow(1/2).mul(constant*0.758)
    elif(suffix == '_ord'):
        df[cdict['debye_temperature']] = df[cdict['lattice_parameter']].mul(1.0743e-10).mul(df[cdict['bulk_modulus']].mul(1e9)).div(df[cdict['atomic_mass']]).pow(1/2).mul(constant*0.682)
    else:
        error_message = ("Input suffix must be either '_dis' or '_ord'")
        
        raise Exception(error_message)
    
    # print(df[cdict['debye_temperature']])
    
    #print(temp_num)
    #print([temp_num])
    
    d1 = df[cdict['debye_temperature']].apply(debye, args=([temp_num])) 
    d2 = df[cdict['debye_temperature']].apply(debye2, args=([temp_num]))
    
    tmp_ser = d1.mul(4/3).add(d2).mul(3)
    df[cdict['entropy']] = pd.Series(tmp_ser.values)#, index=df['Fe_composition'])
    
    df[cdict['free_energy']] = df[cdict['internal_energy']].add(df[cdict['entropy']].mul(-1*temp_num*k_B)).add(df[cdict['configurational_entropy']].mul(-1*temp_num*k_B))
    
    # df.plot(kind='scatter', x='Fe_composition', y=cdict['free_energy'], xlim=(0,1), ylim=(-6, -4))
    # print(df[cdict['free_energy']])
    
    collect_dict[cdict['free_energy']] = pd.Series(df[cdict['free_energy']].values, index=df['Fe_composition'].values)
    df = pd.DataFrame(collect_dict)
    
    return df[cdict['free_energy']]

def calculate_vibrational_entropy(df, suffix, temp):

    temp_num = temp
    suffix = suffix #'_dis'
    
    collect_dict={}
    
    columns = ['lattice_parameter', 'bulk_modulus', 'atomic_mass', 'debye_temperature', 'entropy', 'internal_energy', 'configurational_entropy', 'free_energy']
    temp = '_' + str(temp_num) + 'K'
    
    index = df['Fe_composition']
    
    cdict = {}
    for column in columns:
        cdict[column] = column + temp + suffix
        
    def debye(theta, T):
        if T == 0: return 0
        df_dict = {}
        df_dict['x'] = pd.Series([i/100 for i in range(2000)])
        df_dict['y'] = pd.Series(df_dict['x'].apply(lambda x: x**3 / (np.exp(x) - 1)))
        df = pd.DataFrame(df_dict)
        x_D = theta/T
        return (3/(x_D**3)) * df.loc[df.x <= x_D].y.mul(1/100).sum()
    
    def debye2(theta, T):
        if T == 0: return 0
        x_D = theta/T
        return - np.log(1 - np.exp(-x_D))
    
    h = 4.135e-15 #eV times second
    k_B = 8.617e-5 # eV/K
    constant = ((6 * np.pi**2)**(1/3)) * ((h)/( 2 * np.pi * k_B)) * ( ((4 * np.pi) / (3))**(1/6) )  # K times s
    
    
    df[cdict['atomic_mass']] = df['Fe_composition'].multiply(55.845-50.9415).add(50.9415).mul(1.66e-27)
    
    if(suffix == '_dis'):
        df[cdict['debye_temperature']] = df[cdict['lattice_parameter']].mul(1.0743e-10).mul(df[cdict['bulk_modulus']].mul(1e9)).div(df[cdict['atomic_mass']]).pow(1/2).mul(constant*0.758)
    elif(suffix == '_ord'):
        df[cdict['debye_temperature']] = df[cdict['lattice_parameter']].mul(1.0743e-10).mul(df[cdict['bulk_modulus']].mul(1e9)).div(df[cdict['atomic_mass']]).pow(1/2).mul(constant*0.682)
    else:
        error_message = ("Input suffix must be either '_dis' or '_ord'")
        
        raise Exception(error_message)
        
    d1 = df[cdict['debye_temperature']].apply(debye, args=([temp_num])) 
    d2 = df[cdict['debye_temperature']].apply(debye2, args=([temp_num]))
    
    tmp_ser = d1.mul(4/3).add(d2).mul(3)
    df[cdict['entropy']] = pd.Series(tmp_ser.values)#, index=index)
    
    return df[cdict['entropy']]
    
def get_iron_composition(suffix, temp):

    temp_num = temp
    suffix = suffix #'_dis'
    
    temp = '_' + str(temp_num) + 'K'
    df = pd.read_csv('Fe-V' + suffix + '.csv')
    
    return df['Fe_composition']
    
def calculate_debye_temperature(df, suffix, temp):
    
    temp_num = temp
    suffix = suffix #'_dis'
    
    columns = ['lattice_parameter', 'bulk_modulus', 'atomic_mass', 'debye_temperature', 'entropy', 'internal_energy', 'configurational_entropy', 'free_energy']
    temp = '_' + str(temp_num) + 'K'
    
    cdict = {}
    for column in columns:
        cdict[column] = column + temp + suffix
        
    h = 4.135e-15 #eV times second
    k_B = 8.617e-5 # eV/K
    constant = ((6 * np.pi**2)**(1/3)) * ((h)/( 2 * np.pi * k_B)) * ( ((4 * np.pi) / (3))**(1/6) )  # K times s
    
    df[cdict['atomic_mass']] = df['Fe_composition'].multiply(55.845-50.9415).add(50.9415).mul(1.66e-27)
    
    # Changed new values for ordered and disordered compositions
    if(suffix == '_dis'):
        df[cdict['debye_temperature']] = df[cdict['lattice_parameter']].mul(1.0743e-10).mul(df[cdict['bulk_modulus']].mul(1e9)).div(df[cdict['atomic_mass']]).pow(1/2).mul(constant*0.758)
    elif(suffix == '_ord'):
        df[cdict['debye_temperature']] = df[cdict['lattice_parameter']].mul(1.0743e-10).mul(df[cdict['bulk_modulus']].mul(1e9)).div(df[cdict['atomic_mass']]).pow(1/2).mul(constant*0.682)
    else:
        error_message = ("Input suffix must be either '_dis' or '_ord'")
        
        raise Exception(error_message)
    
    return df[cdict['debye_temperature']]
    
def calculate_configurational_entropy(df, suffix, temp):

    temp_num = temp
    suffix = suffix #'_dis'
    
    columns = ['lattice_parameter', 'bulk_modulus', 'atomic_mass', 'debye_temperature', 'entropy', 'internal_energy', 'configurational_entropy', 'free_energy']
    temp = '_' + str(temp_num) + 'K'
    
    cdict = {}
    for column in columns:
        cdict[column] = column + temp + suffix
    
    h = 4.135e-15 #eV times second
    k_B = 8.617e-5 # eV/K
    
    ret = df[cdict['configurational_entropy']].mul(-1*temp_num*k_B)
    return ret

#%% Quantities and error calculation

df_output_dis_300 = error_calculation('_dis', 300)
df_output_dis_500 = error_calculation('_dis', 500)
'''df_output_0_ord = error_calculation('_ord', 0)
df_output_300_dis = error_calculation('_dis', 300)
df_output_300_ord = error_calculation('_ord', 300)
df_output_500_dis = error_calculation('_dis', 500)
df_output_500_ord = error_calculation('_ord', 500)
df_output_700_dis = error_calculation('_dis', 700)
df_output_700_ord = error_calculation('_ord', 700)
df_output_1000_dis = error_calculation('_dis', 1000)
df_output_1000_ord = error_calculation('_ord', 1000)
df_output_1300_dis = error_calculation('_dis', 1300)
df_output_1300_ord = error_calculation('_ord', 1300)

df_output_dis = pd.merge(pd.merge(df_output_0_dis, df_output_300_dis, on = "V_composition"), 
                         df_output_500_dis, on = "V_composition")
df_output_dis = pd.merge(pd.merge(df_output_dis, df_output_700_dis, on = "V_composition"), 
                         df_output_1000_dis, on = "V_composition")
df_output_dis = pd.merge(df_output_dis, df_output_1300_dis, on = "V_composition")

df_output_ord = pd.merge(pd.merge(df_output_0_ord, df_output_300_ord, on = "V_composition"), 
                         df_output_500_ord, on = "V_composition")
df_output_ord = pd.merge(pd.merge(df_output_ord, df_output_700_ord, on = "V_composition"), 
                         df_output_1000_ord, on = "V_composition")
df_output_ord = pd.merge(df_output_ord, df_output_1300_ord, on = "V_composition")'''

df_output_dis_300.to_csv('dataframe output dis 300K.csv')
df_output_dis_500.to_csv('dataframe output dis 500K.csv')