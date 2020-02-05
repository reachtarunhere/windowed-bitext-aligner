def sentence_len_ratio(s1, s2):
    l1, l2 = len(s1.split()), len(s2.split())
    return l1/l2 if l1 > l2 else l2/l1
