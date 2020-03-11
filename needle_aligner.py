from Bio import pairwise2


def create_fake_unicode_string(l):
    """return list of same size composed of unicode characters from 46 to length of l"""
    return ''.join(chr(i+46) for i in range(len(l)))


def fake_unicode_string_to_indexes(s):
    return [ord(c)-46 for c in s]  # -1 means no match


def calcuate_alignment_indexes(src_lines, tgt_lines, scoring_matrix):

    def char_match_fn(c1, c2): return dot_scores[ord(c1)-46, ord(c2)-46]

    aligner_out = pairwise2.align.globalcx(create_fake_unicode_string(src_lines),
                                           create_fake_unicode_string(tgt_lines), char_match_fn)

    return fake_unicode_string_to_indexes(aligner_out[0][0], aligner_out[0][1])


def make_alignment_dataframe(src_lines, tgt_lines, scoring_matrix):
    pass
