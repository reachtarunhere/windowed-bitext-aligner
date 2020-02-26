import numpy as np
import pandas as pd

from scoring import margin_second_largest, margin_avg, ratio_second_largest, ratio_avg, sentence_len_ratio


def CandidateGenerator(trg_max, window_size):
    """ trg_max is len of trg sentences file"""

    half_margin = window_size//2

    def gen_candidate(i):
        def valid_trg(x): return 0 <= x < trg_max

        return [x for x in range(i-half_margin, i+half_margin+1) if valid_trg(x)]

    return gen_candidate


def CosScoreFinder(dot_scores, get_candidate_fn):

    def get_score(src_i):
        candidate_indexes = get_candidate_fn(src_i)
        candidate_scores = dot_scores[src_i][np.array(candidate_indexes)]
        best_cand_index = candidate_indexes[candidate_scores.argmax()]
        return best_cand_index, candidate_scores

    return get_score


def make_alignment_dataframe(src_lines, tgt_lines, get_cos_score_fn):

    sentence_scorers = [sentence_len_ratio]
    cos_scorers = [margin_second_largest,
                   margin_avg, ratio_second_largest, ratio_avg]
    # combined_scorers = [] -> maybe implemented in future

    def prepare_single_record(src_i):
        tgt_i, scores_src_i = get_score_fn(src_i)
        src_sent, tgt_sent = src_lines[src_i], tgt_lines[tgt_i]
        sent_scores = [f(src_sent, tgt_sent) for f in sentence_scorers]
        cos_scores = [f(scores_src_i) for f in cos_scorers]

        return [src_i, tgt_i, scr_sent, tgt_sent] + sent_scores + cos_scores

    complete_record = [prepare_single_record(i) for i in range(len(src_lines))]

    return pd.DataFrame.from_records(complete_record)


def ScoringMatrix(emb_src, emb_tgt):
    return emb_scr @ emb_tgt.T


def read_embed(filename):
    X = np.fromfile(filename, dtype=np.float32, count=-1)
    X.resize(X.shape[0] // dim, dim)
    return X


def read_texts(src, tgt):
    return open(src).readlines(), open(tgt).readlines()


def main(src_path, tgt_path, src_emb_path=None, tgt_emb_path=None, window_size=5):
    src_lines, tgt_lines = read_texts(src_path, tgt_path)
    emb_src, emb_tgt = read_embed(src_emb_path), read_embed(tgt_emb_path)
    scoring_matrix = ScoringMatrix(emb_src, emb_tgt)
    get_cos_score_fn = CosScoreFinder(scoring_matrix,
                                      CandidateGenerator(len(tgt_lines), window_size))
