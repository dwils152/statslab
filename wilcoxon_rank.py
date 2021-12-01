
import pandas as pd
import numpy as np
import scipy
from scipy import stats
from scipy.stats.stats import ranksums
import plotly.express as px
from statsmodels.stats.multitest import multipletests
import xlsxwriter

#load in data to pandas dataframe
data = pd.read_csv('GSE135769_CTCF_TPM.txt', sep= '\t', header=0, index_col=0)

#create subsets of the data for the first technical replicates
#there are 24 cells for WT and 24 cells for KD
wild_type = data.iloc[:, 0:24]
knock_down = data.iloc[:, 24:48]

p_vals = list()
significant_genes = list()
all_genes = list(data.index)
ids = list()

#perform wilcoxon rank sum test for each gene
for i in range(24057):

    stat = scipy.stats.ranksums(wild_type.iloc[i, :], knock_down.iloc[i, :])
    p_vals.append(stat.pvalue)

#adjust the p-values for multiple testing
adjusted = multipletests(p_vals, alpha=0.05, method='fdr_bh', is_sorted=False, returnsorted=False)

#p-values for significant genes
sig_p_vals = [p_val for p_val in adjusted[1] if p_val < 0.05]

#booleans indicating whether we accept or reject the hypothesis
accept_reject = adjusted[0]
gene_list = data.index
p = adjusted[1]
subset_p = list()

#get names for DE genes
for result, gene, pval in zip(accept_reject, gene_list, p):

    if result == True:

        significant_genes.append(gene)
        subset_p.append(pval)


#plot p-values
fig = px.histogram(adjusted[1])
fig.update_xaxes(title="p-values")
fig.update_yaxes(title="Frequency")
fig.add_vline(x=0.5, line_width=3, line_dash="dash", line_color="red")
fig.show()

with open('conversions3', 'r') as fin:

    for line in fin.readlines():

        ids.append(line.strip())

#with open('all_genes.txt', 'w') as fin:

 #   for gene in all_genes:

  #      fin.write(gene)
   #     fin.write(f'\n')

d = {'genes': significant_genes, 'symbol':ids, 'p-value':subset_p}
df = pd.DataFrame(d)

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
t = df.to_excel(writer, sheet_name='test', index=False, header=False)
writer.save()

