# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import select

import sys

import vcf
from vcf.parser import _Info as VcfInfo, field_counts as vcf_field_counts

from optparse import OptionParser

from .annotator import annotate_variant

def _get_args():
    parser = OptionParser(usage="usage: %prog polyphen.whess.sqlite input.vcf output.vcf")
    return parser, parser.parse_args()

def main():
    parser, (options, args) = _get_args()
    if len(args) != 3:
        parser.error("Missing arguments!")

    pp2file = args[0]
    input_vcf = args[1]
    output_vcf = args[2]

    engine = create_engine('sqlite:///{}'.format(pp2file))
    conn = engine.connect()

    annotation_identifier = "PP2"

    reader = vcf.Reader(open(input_vcf, 'r'))
    reader.infos[annotation_identifier] = VcfInfo(
        annotation_identifier,
        1,
        'String',
        ("PolyPhen2 annotations in the following order:"
         "Gene name; "
         "UniProt id; "
         "Amino acid change; "
         "HVar effect category; "
         "Strength of var effect (probability); ",
         "HDiv effect category; "
         "Strength of div effect (probability)"),
        'PolyPhen2',
        'PGV001')
    writer = vcf.Writer(open(output_vcf, 'w'), reader, lineterminator='\n')
    for v in reader:
        res = annotate_variant(
                    conn,
                    'chr{}'.format(v.CHROM),
                    v.POS,
                    v.REF,
                    v.ALT[0])
        if res is None:
            annotation = ['.', '.', '.', '.', '.', '.', '.']
        else:
            annotation = [
                res.gene,
                res.protein,
                res.aa_change,
                res.hvar_pred,
                res.hvar_prob,
                res.hdiv_pred,
                res.hdiv_prob]

        v.add_info(annotation_identifier, annotation)
        writer.write_record(v)

if __name__ == '__main__':
    main()
