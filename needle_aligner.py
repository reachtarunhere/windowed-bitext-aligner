def create_fake_unicode_string(l):
    """return list of same size composed of unicode characters from 50 to length of l"""
    return ''.join(chr(i+50) for i in range(len(l)))


def make_alignment_dataframe(src_lines, tgt_lines, scoring_matrix):
    pass
