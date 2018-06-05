import pandas as pd
import math
import os
import subprocess

cytokines = pd.read_excel("Sepsis_patient_cytokine_levels.xlsx")
mean_cytokine = cytokines.mean(0)

ped = pd.read_csv("sample.ped", sep=' ',
                  names=["fid", "iid", "father", "mother", "gender", "trait"])

cwd = os.getcwd()

for cytokine in mean_cytokine.iteritems():
    destination = os.path.join(cwd, 'binary_cytokines/'+cytokine[0])
    for index,row in ped.iterrows():
        cytokine_level = float(cytokines.loc[cytokines['SampleNumber'] == row['fid']][cytokine[0]].values)
        if math.isnan(cytokine_level):
            ped.drop(ped.index[index])
        elif cytokine_level < mean_cytokine[cytokine[0]]:
            ped.at[index, 'trait'] = 1
        else:
            ped.at[index, 'trait'] = 2
    if not os.path.exists(destination):
        os.makedirs(destination)
    ped.to_csv(os.path.join(destination, cytokine[0]+".ped"),
               header=None, index=None, sep=' ', mode='a')
    subprocess.call(['cp', 'sample.map', destination])
    subprocess.call(['mv', os.path.join(destination, 'sample.map'), os.path.join(destination, cytokine[0]+".map")])
#     os.chdir(destination)
#     subprocess.call(['plink', '--file', cytokine[0], '--make-bed', '--out', cytokine[0]])
#     os.chdir(cwd)
