
from goatools.obo_parser import GODag
from goatools.anno.genetogo_reader import Gene2GoReader
from genes_NCBI_10090_ProteinCoding import GENEID2NT as GeneID2nt_mus
from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS
import os
import xlsxwriter
from goatools.godag_plot import plot_gos, plot_results, plot_goid2goobj
import plotly.express as px

obodag = GODag("go-basic.obo")
fin_gene2go = 'gene2go'

objanno = Gene2GoReader(fin_gene2go, taxids=[10090])
ns2assoc = objanno.get_ns2assc()

for nspc, id2gos in ns2assoc.items():
    print("{NS} {N:,} annotated mouse genes".format(NS=nspc, N=len(id2gos)))

goeaobj = GOEnrichmentStudyNS(
        GeneID2nt_mus.keys(), # List of mouse protein-coding genes
        ns2assoc, # geneid/GO associations
        obodag, # Ontologies
        propagate_counts = False,
        alpha = 0.05, # default significance cut-off
        methods = ['fdr_bh']) # defult multipletest correction method

din_xlsx = 'test.xlsx'

geneid2symbol = {}

if os.path.isfile(din_xlsx):  
    import xlrd
    book = xlrd.open_workbook(din_xlsx)
    pg = book.sheet_by_index(0)
    for r in range(pg.nrows):
        symbol, geneid, pval = [pg.cell_value(r, c) for c in range(pg.ncols)]
        if geneid:
            geneid2symbol[int(geneid)] = symbol
    print('{N} genes READ: {XLSX}'.format(N=len(geneid2symbol), XLSX=din_xlsx))
else:
    raise RuntimeError('FILE NOT FOUND: {XLSX}'.format(XLSX=din_xlsx))

geneids_study = geneid2symbol.keys()
goea_results_all = goeaobj.run_study(geneids_study)
goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < 0.05]

#goeaobj.wr_xlsx("test_out.xlsx", goea_results_sig)
#goeaobj.wr_txt("test_out.txt", goea_results_sig)
#plot_results("test_out{NS}.png", goea_results_sig)

#fig = px.histogram(goea_results_all)
#fig.update_xaxes(title="p-values")
#fig.update_yaxes(title="Frequency")
#fig.add_vline(x=0.5, line_width=3, line_dash="dash", line_color="red")
#fig.show()

adjusted_pvals = [p.p_fdr_bh for p in goea_results_all]
print(adjusted_pvals)

fig = px.histogram(adjusted_pvals)
fig.update_xaxes(title="p-values")
fig.update_yaxes(title="Frequency")
fig.add_vline(x=0.05, line_width=3, line_dash="dash", line_color="red")
fig.show()