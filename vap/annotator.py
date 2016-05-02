# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import select

class Annotation(object):
    def __init__(
            self,
            chrom,
            pos,
            ref,
            alt,
            gene,
            protein,
            aa_change,
            hvar_pred,
            hvar_prob,
            hdiv_pred,
            hdiv_prob):
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.gene = gene
        self.protein = protein
        self.aa_change = aa_change
        self.hvar_pred = hvar_pred
        self.hvar_prob = hvar_prob
        self.hdiv_pred = hdiv_pred
        self.hdiv_prob = hdiv_prob

def annotate_variant(conn, chrom, pos, ref, alt):
    query_template = ("SELECT chrom, chrpos, nt1, nt2,"
                      " gene, acc, pos, aa1, aa2, "
                      " hvar_prediction, hvar_prob, "
                      " hdiv_prediction, hdiv_prob "
                      "FROM features JOIN scores USING(id) "
                      "WHERE chrom = '{}' AND chrpos = {}"
                      " AND nt1 = '{}' AND nt2 = '{}'")
    query = query_template.format(chrom, pos, ref, alt)
    res = conn.execute(query).fetchone()
    if res is None:
        return None
    else:
        return Annotation(
                        res[0], res[1], res[2], res[3],
                        res[4], res[5],
                        "{}{}{}".format(res[7], res[6], res[8]),
                        res[9], res[10], res[11], res[12])
