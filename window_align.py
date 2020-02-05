import numpy as np


def CandidateGenerator(trg_max, window_size=5):
    """ trg_max is len of trg sentences file"""

    half_margin = window_size//2

    def gen_candidate(i):
        def valid_trg(x): return 0 <= x < trg_max

        return [x for x in range(i-half_margin, i+half_margin+1) if valid_trg(x)]

    return gen_candidate


def PairScoreFinder(dot_scores, get_candidate_fn):

    def get_score(src_i):
        candidate_indexes = get_candidate_fn(src_i)
        candidate_scores = dot_scores[src_i][np.array(candidate_indexes)]
        best_cand_index = candidate_indexes[candidate_scores.argmax()]
        return best_cand_index, candidate_scores

    return get_score


def scoring_matrix(emb_src, emb_tgt):
    return emb_scr @ emb_tgt.T


def read_embed(filename):
    X = np.fromfile(filename, dtype=np.float32, count=-1)
    X.resize(X.shape[0] // dim, dim)
    return X


def read_texts(src, tgt):
    return open(src).readlines(), open(tgt).readlines()
