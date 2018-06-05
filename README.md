# GWAS-cytokines
Running GWAS on 50 cytokines

## HOW TO GENERATE PED FILES
Run this in the directory with VASST2.bed file
``plink --bfile VASST2 --recode --tab --out sample --noweb``

This will generate sample.ped, sample.map, and other files
