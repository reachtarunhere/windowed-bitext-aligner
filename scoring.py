def sentence_len_ratio(s1, s2, cos_scores):
    l1, l2 = len(s1.split()), len(s2.split())
    return l1/l2 if l1 > l2 else l2/l1


def cos_second_margin(s1, s2, cos_scores):
    pass


def cos_avg_margin(s1, s2, cos_scores):
    pass


def cos_avg_ratio_margin(s1, s2, cos_scores):
    pass
