# vcf-annotate-polyphen
A tool to annotate human VCF files with PolyPhen-2 effect measures.
This tool only works on human variants,
collects ClinVar scores,
and assumes the VCF follows `hg19/GRCh37` conventions.

## Install
### via PyPi
```
$ pip install vcf-annotate-polyphen
```

### via Source Code
```
$ git checkout https://github.com/hammerlab/vcf-annotate-polyphen.git
$ cd vcf-annotate-polyphen/
$ python setup.py
```

## Usage
After installing the package, you can invoke the command line utility as follows:

```
$ vcf-annotate-polyphen --help
Usage: vcf-annotate-polyphen polyphen.whess.sqlite input.vcf output.vcf

Options:
  -h, --help  show this help message and exit
```

As listed above in the help text, this tool expects three arguments from the user:

1. [PolyPhen-2 WHESS](ftp://genetics.bwh.harvard.edu/pph2/whess) in SQLite format
2. Input VCF to be annotated
3. Output VCF to be written with annotations

The output file should have an additional `INFO` field as described below:

```
##INFO=<ID=PP2,Number=1,Type=String,Description="PolyPhen2 annotations in the following order:Gene name; UniProt id; Amino acid change; ClinVar effect category; Strength of effect (probability)">
```

which manifests itself for each variant description:

```
...
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  SAMPLE
2       165351172       .       T       A       .       PASS    SOMATIC;VT=SNP;PP2=.,.,.,.,.    GT:AD:BQ:DP:FA:SS       0:11,0:.:11:0.0:0       0/1:3,5:30.0:8:0.625:22       179247908       .       C       G       .       PASS    SOMATIC;VT=SNP;PP2=OSBPL6,Q9BZF3,N593K,probably damaging,0.998  GT:AD:BQ:DP:FA:SS       0:27,2:.:29:0.069:0     0/1:27,4:28.0:31:0.129:2
7       99796940        .       G       A       .       PASS    SOMATIC;VT=SNP;PP2=STAG3,Q9UJ98,R508Q,benign,0.0        GT:AD:BQ:DP:FA:SS       0:37,0:.:37:0.0:0       0/1:49,10:30.0:59:0.169:2
...
```

Here is an annotated VCF: [example/TCGA-55-6543.annotated.vcf](example/TCGA-55-6543.annotated.vcf).

### Example usage
```
$ cd example/
# The following file is ~7 GB!!!
$ wget "ftp://genetics.bwh.harvard.edu/pph2/whess/polyphen-2.2.2-whess-2011_12.sqlite.bz2"
$ bunzip2 polyphen-2.2.2-whess-2011_12.sqlite.bz2
$ vcf-annotate-polyphen ./TCGA-55-6543.vcf ./TCGA-55-6543.annotated.vcf
$ less ./TCGA-55-6543.annotated.vcf
```
