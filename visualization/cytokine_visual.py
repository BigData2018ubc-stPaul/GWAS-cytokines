import os
import sys
import math
script_dir = os.path.split(os.path.realpath(__file__))[0]

root_path = os.path.dirname(script_dir)
print(root_path)
data_path = os.path.join(root_path, "data/")
export_path = os.path.join(root_path, "visualization/cytokineVSpatient")
if not os.path.exists(export_path):
    os.mkdir(export_path)
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


df = pd.read_excel(os.path.join(data_path, 'Sepsis_patient_cytokine_levels.xlsx'), sheet_name='Sheet2')

# print("Column headings:")
# print(df.columns)
# for head in df.columns:
#     print(head)
# for index in df.index:
#     print(df['SampleNumber'][index])

import numpy as np
import matplotlib as matplt
matplt.use('TkAgg')  # https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
import matplotlib.pyplot as pyplt
import matplotlib.colors as colors
import matplotlib.axis as axis
import matplotlib.ticker as ticker

pyplt.style.use('ggplot')

# plot number of patient in each cytokine level
for cytokine in df.columns[1:]:
    data_list = [] # {cytokine_level:numer of patient}
    for index in df.index:
        data = df[cytokine][index]
        # TODO: how to deal with missing data
        if math.isnan(data):
            continue
            # data = -10 # assign with a negative value
        data_list.append(data)
    fig = pyplt.figure()
    ax = fig.add_subplot(111)
    # ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
    n, bins, patches = ax.hist(data_list, bins=len(data_list))
    # We'll color code by height, but you could use any scalar
    fracs = n / n.max()
    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())
    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = pyplt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)


    pyplt.xlabel('cytokine level')
    pyplt.ylabel('#patient')
    pyplt.title('Histogram - ' + cytokine)
    pyplt.grid(True)
    fig.savefig(os.path.join(export_path, cytokine + '.png'))






