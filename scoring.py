def sentence_len_ratio(s1, s2):
    l1, l2 = len(s1.split()), len(s2.split())
    return l1/l2 if l1 > l2 else l2/l1


def margin_second_largest(cos_scores):
    sorted_scores = np.sort(cos_scores)
    return sorted_scores[-1]-sorted_scores[-2]


def cos_avg_margin(s1, s2, cos_scores):
    pass


def cos_avg_ratio_margin(s1, s2, cos_scores):
    pass
