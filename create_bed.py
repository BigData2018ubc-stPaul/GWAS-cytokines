import pandas as pd
import math
import os
import subprocess

def call_process(command):
    subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Creating template files
if not os.path.exists("template/"):
    call_process(["tar", "-zxvf", "template.tar.gz"])
    call_process(["plink", "--bfile", "template/template", "--recode", "--tab", "--out", "template/template", "--noweb"])
    call_process(["cut", "-f", "7-", "template/template.ped", ">>", "template/cut_template.ped"])

cytokines = pd.read_excel("Sepsis_patient_cytokine_levels.xlsx")
mean_cytokine = cytokines.mean(0)

ped = pd.read_csv("template/template.fam", sep=' ',
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
    ped.to_csv(os.path.join(destination, cytokine[0]+"_temp.ped"),
               header=None, index=None, sep=' ', mode='a')
    call_process(['cp', 'template/template.map', destination])
    call_process(['mv', os.path.join(destination, 'template.map'), os.path.join(destination, cytokine[0]+".map")])
    call_process(["paste", "-d' '", "%s", "template/cut_template.ped", ">>", "%s"] % (os.path.join(destination, cytokine[0]+"_temp.ped"), os.path.join(destination, cytokine[0]+".ped")))
    call_process(["plink", "--file", "%s", "--make-bed", "--out", "%s", "--noweb"] % (os.path.join(destination, cytokine[0]), os.path.join(destination, cytokine[0])))
    call_process(["plink", "--bfile", "%s", "--assoc", "--out", "%s", "--noweb"] % (os.path.join(destination, cytokine[0]), os.path.join(destination, cytokine[0])))
    call_process(["Rscript", "--vanilla", "../../visualization/manhattan.R", "%s", "%s"] % (os.path.join(destination, cytokine[0]+".assoc"), os.path.join(destination, cytokine[0]+".png")))
    call_process(["rm", "%s"] % os.path.join(destination, cytokine[0]+".ped"))
