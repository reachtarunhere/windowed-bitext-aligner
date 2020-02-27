from embed import *
import os
import sys

import numpy as np

# get environment
assert os.environ.get('LASER'), 'Please set the enviornment variable LASER'
LASER = os.environ['LASER']

sys.path.append(LASER + '/source')

ENCODER = SentenceEncoder(f'{LASER}/ models/bilstm.93langs.2018-12-26.pt',
                          'quicksort')


def tokenize_bpe_and_encode(sentences, token_lang, source_is_file=False):

    with tempfile.TemporaryDirectory() as tmpdir:

        if not source_is_file:
            sentence_file_name = os.path.join(tmpdir, 'sents')
            open(sentence_file_name, "w").writelines(sentences)
            ifname = sentence_file_name

        tok_fname = os.path.join(tmpdir, 'tok')
        Token(ifname,
              tok_fname,
              lang=token_lang,
              romanize=True if token_lang == 'el' else False,
              lower_case=True, gzip=False,
              over_write=False)
        ifname = tok_fname

        bpe_fname = os.path.join(tmpdir, 'bpe')
        BPEfastApply(ifname,
                     bpe_fname,
                     f'{LASER}/models/93langs.fcodes',
                     over_write=False)
        ifname = bpe_fname

        return ENCODER.encode_sentences(open(bpe_fname).readlines())


def ScoringMatrix(emb_src, emb_tgt):
    return emb_src @ emb_tgt.T


def read_embed(filename):
    dim = 1024
    X = np.fromfile(filename, dtype=np.float32, count=-1)
    X.resize(X.shape[0] // dim, dim)
    return X
