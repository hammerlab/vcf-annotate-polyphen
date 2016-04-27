# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import select

import sys

import vcf
from vcf.parser import _Info as VcfInfo, field_counts as vcf_field_counts

from optparse import OptionParser

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

    query_template = ("SELECT chrom, chrpos, gene, nt1, nt2, acc, pos, aa1, aa2, hvar_prediction, hvar_prob "
                      "FROM features JOIN scores USING(id) "
                      "WHERE chrom = '{}' AND chrpos = {} AND nt1 = '{}' AND nt2 = '{}'")
    def record_to_query(record):
        chrom = "chr{}".format(record.CHROM)
        return query_template.format(chrom, record.POS, record.REF, record.ALT[0])

    annotation_identifier = "PP2"
    def annotate_record_with_result(record, result):
        if result is None:
            annotation = [".", ".", ".", ".", "."]
        else:
            annotation = [result[2],
                          result[5],
                          "{}{}{}".format(result[7], result[6], result[8]),
                          result[9],
                          result[10]]
        record.add_info(annotation_identifier, annotation)
        return record

    reader = vcf.Reader(open(input_vcf, 'r'))
    reader.infos[annotation_identifier] = VcfInfo(
        annotation_identifier,
        1,
        'String',
        ("PolyPhen2 annotations in the following order:"
         "Gene name; "
         "UniProt id; "
         "Amino acid change; "
         "ClinVar effect category; "
         "Strength of effect (probability)"),
        'PolyPhen2',
        'PGV001')
    writer = vcf.Writer(open(output_vcf, 'w'), reader, lineterminator='\n')
    for record in reader:
        query = record_to_query(record)
        res = conn.execute(query).fetchone()
        writer.write_record(annotate_record_with_result(record, res))

if __name__ == '__main__':
    main()
