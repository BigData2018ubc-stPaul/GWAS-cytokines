#!/usr/bin/env Rscript

# this is a Rscript to generate manhattan plot
# usage via command line: Rscript --vanilla manhattan.R inputFile outputFile
# inputFile: gwasResultFile
# outputFile: png of manhattan
args = commandArgs(trailingOnly=TRUE)
if (length(args)<2) {
  stop("At least two argument must be supplied (input and output file).n", call.=FALSE)
}

input_file = args[1]
output_file = args[2]
is.installed <- function(mypkg) is.element(mypkg, installed.packages()[,1]) 
if (!is.installed('qqman')){
    install.packages('qqman', repo='http://cran.r-project.org') # This only needs to be done once
}
data<-read.table(file=input_file, header=T)
library('qqman')
data<-na.omit(data) # drop NaN's
png(filename=output_file)
manhattan(data)
dev.off()
