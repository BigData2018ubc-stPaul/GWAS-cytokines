install.packages('qqman')	# only need to do it once to install the package on your server

# read association file produced by plink
data<-read.table(file="as1.assoc", header=T)
head(data)
# omit NaN's
data<-na.omit(data)

library('qqman')
manhattan(data)

# basic doc:
# http://www.gettinggeneticsdone.com/2014/05/qqman-r-package-for-qq-and-manhattan-plots-for-gwas-results.html
