import numpy as np


def match_score(cos_scores):
    return max(cos_scores)


def sentence_len_ratio(s1, s2):
    l1, l2 = len(s1.split()), len(s2.split())
    return l1/l2 if l1 > l2 else l2/l1


def margin_second_largest(cos_scores):
    sorted_scores = np.sort(cos_scores)
    return sorted_scores[-1]-sorted_scores[-2]


def margin_avg(cos_scores):
    return max(cos_scores) - cos_scores.mean()


def ratio_second_largest(cos_scores):
    sorted_scores = np.sort(cos_scores)
    return sorted_scores[-2]/sorted_scores[-1]


def ratio_avg(cos_scores):
    return cos_scores.mean()/cos_scores.max()
