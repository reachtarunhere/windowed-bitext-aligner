import numpy as np
import pandas as pd

from metrics import match_score, margin_second_largest, margin_avg, ratio_second_largest, ratio_avg, sentence_len_ratio
from matchscoring import read_embed, ScoringMatrix, get_scoring_matrix_from_lines


def CandidateGenerator(trg_max, window_size):
    """ trg_max is len of trg sentences file"""

    half_margin = window_size//2

    def gen_candidate(i):
        def valid_trg(x): return 0 <= x < trg_max

        return [x for x in range(i-half_margin, i+half_margin+1) if valid_trg(x)]

    return gen_candidate


def DotScoreFinder(dot_scores, get_candidate_fn):

    def get_score(src_i):
        candidate_indexes = get_candidate_fn(src_i)
        candidate_scores = dot_scores[src_i][np.array(candidate_indexes)]
        best_cand_index = candidate_indexes[candidate_scores.argmax()]
        return best_cand_index, candidate_scores

    return get_score


def make_alignment_dataframe(src_lines, tgt_lines, scoring_matrix, window_size):

    get_score_fn = DotScoreFinder(scoring_matrix,
                                  CandidateGenerator(len(tgt_lines), window_size))

    sentence_metric_fns = [sentence_len_ratio]
    dot_metric_fns = [match_score, margin_second_largest,
                      margin_avg, ratio_second_largest, ratio_avg]
    # combined_scorers = [] -> maybe implemented in future

    def prepare_single_record(src_i):
        tgt_i, scores_src_i = get_score_fn(src_i)
        src_sent, tgt_sent = src_lines[src_i], tgt_lines[tgt_i]
        sent_metrics = [f(src_sent, tgt_sent) for f in sentence_metric_fns]
        dot_metrics = [f(scores_src_i) for f in dot_metric_fns]

        return [src_i, tgt_i, src_sent.strip(), tgt_sent.strip()] + sent_metrics + dot_metrics

    complete_record = [prepare_single_record(i) for i in range(len(src_lines))]

    # hardcoded rn. Maybe fix later.
    column_names = ["Src Index", "Tgt Index", "Source Sentence", "Target Sentence",
                    "Sentence Length Ratio", "Match Score", "Margin Second Best", "Margin Avg",
                    "Ratio Second Best", "Ratio Avg"]

    return pd.DataFrame.from_records(complete_record, columns=column_names)


def read_texts(src, tgt):
    return open(src).readlines(), open(tgt).readlines()


def main(src_path, tgt_path, output_file_path, src_lang='en', tgt_lang='en',
         src_emb_path=None, tgt_emb_path=None, window_size=5):

    src_lines, tgt_lines = read_texts(src_path, tgt_path)

    if src_emb_path is not None and tgt_emb_path is not None:
        emb_src, emb_tgt = read_embed(src_emb_path), read_embed(tgt_emb_path)
        scoring_matrix = ScoringMatrix(emb_src, emb_tgt)
    else:
        scoring_matrix = get_scoring_matrix_from_lines(
            src_lines, tgt_lines, src_lang, tgt_lang)

    alignment_df = make_alignment_dataframe(
        src_lines, tgt_lines, scoring_matrix, window_size)

    alignment_df.to_csv(output_file_path)


if __name__ == '__main__':
    import plac
    plac.call(main)
