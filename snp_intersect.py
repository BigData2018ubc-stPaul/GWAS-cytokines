#/usr/bin/env python
import sys
import os
import getopt

def get_cytokine_paths(cytokine_dir):
    cytokine_paths = []
    for file in os.listdir(cytokine_dir):
        if file.endswith(".assoc"):
            name = file.split('.')[0]
            cytokine_paths.append((name,os.path.join(cytokine_dir,file))) 
    return cytokine_paths

def get_cytokine_snps(cytokine_paths,alpha):
    cytokine_snps = {} 
    for (name,path) in cytokine_paths: 
        snps = []
        with open(path,'r') as file:
            for line in file:
                tokens = line.split()
                if tokens[8] not in ["NA","P"," ","\t","\n"] and float(tokens[8]) <= alpha:
                    snps.append(tokens[1])
        assert(len(snps) > 0)
        cytokine_snps[name] = snps
    return cytokine_snps

def get_survival_snps(survival_path,alpha):
    snps = []
    with open(survival_path,'r') as file:
        for line in file:
            tokens = line.split()
            if tokens[8] not in ["NA","P"," ","\t","\n"] and float(tokens[8]) <= alpha:
                snps.append(tokens[1])
    assert(len(snps) > 0)
    return snps

def intersect_snps(cytokine_snps,survival_snps):
    intersection = {}
    for cytokine in cytokine_snps:
        snps = []
        for snp in survival_snps:
            if snp in cytokine_snps[cytokine]:
                snps.append(snp)
        intersection[cytokine] = snps
    return intersection

def output_snps(intersected_snps,output):
    path = output + ".tsv"
    with open(path,'a') as file:
        if sum(1 for line in open(output+ ".tsv")) < 1:
            file.write("Cytokine \t SNPs\n")
        for cytokine in intersected_snps:
            snps = ""
            for snp in intersected_snps[cytokine]:
                snps = snps + snp + "\t"
            snps.rstrip('\t')
            file.write(cytokine + "\t" + snps + "\n")
            print(cytokine, snps)

def main(argv):
    help_message = "Finds SNPs which are both correlated with raised levels of particular cytokines, and survival."
    usage_message = "[-h help and usage] [-s path to survival association file] [-c path to directory containing cytokine assoc files] [-a desired alpha P-value cutoff]"
    options = "hs:c:o:a:"

    try:
        opts,args = getopt.getopt(argv[1:],options)
    except getopt.GetoptError:
        print("Error: unable to read command line arguments.")
        sys.exit(1)

    if len(argv) == 1:
        print(help_message)
        print(usage_message)
        sys.exit(1)    
    
    survival_path = None
    cytokine_dir = None
    output = None
    alpha = None

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            print(usage_message)
        elif opt == '-s':
            survival_path = arg
        elif opt == '-c':
            cytokine_dir = arg
        elif opt == '-o':
            output = arg
        elif opt == '-a':
            alpha = float(arg)

    opts_incomplete = False

    if survival_path is None:
        print("Error: please provide your survival SNP association file.")
        opts_incomplete = True
    if cytokine_dir is None:
        print("Error: please provide the directory containing your cytokine SNP association files.")
        opts_incomplete = True
    if output is None:
        print("Error: please provide an output prefix.")
        opts_incomplete = True
    if alpha is None:
        print("Error: please provide an alpha value for the P-value cutoff.")
        opts_incomplete = True
    
    if opts_incomplete:
        print(usage_message)
        sys.exit(1)

    cytokine_paths = get_cytokine_paths(cytokine_dir)
    cytokine_snps = get_cytokine_snps(cytokine_paths,alpha)
    survival_snps = get_survival_snps(survival_path,alpha)
    intersected_snps = intersect_snps(cytokine_snps,survival_snps)
    output_snps(intersected_snps,output)
    
if __name__ == "__main__":
    main(sys.argv)
