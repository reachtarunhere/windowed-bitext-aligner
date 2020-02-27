from embed import *
import os
import sys

# get environment
assert os.environ.get('LASER'), 'Please set the enviornment variable LASER'
LASER = os.environ['LASER']

sys.path.append(LASER + '/source')


def tokenize_and_bpe(sentences, token_lang, source_is_file=False):

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

        return open(bpe_fname).readlines()
