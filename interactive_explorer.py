import streamlit as st
import time
import SessionState
import base64
import spacy

from window_align import get_scoring_matrix_from_lines, make_alignment_dataframe
from matchscoring import *

session = SessionState.get(src_lines=[], tgt_lines=[], df=None)

st.title("Windowed LASER Aligner")
st.text("By Tarun")

# current segmenter is one for english can customize later
nlp = spacy.load('en_core_web_sm')


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Right click and download csv file</a>'
    return href


def get_alignment_df(src_lines, tgt_lines, src_lang="en", tgt_lang="en", window_size=5):
    scoring_matrix = get_scoring_matrix_from_lines(
        src_lines, tgt_lines, src_lang, tgt_lang)
    df = make_alignment_dataframe(
        src_lines, tgt_lines, scoring_matrix, window_size)
    del scoring_matrix
    return df


def segment_sentences(lines):
    all_sents = []
    for l in lines:
        doc = nlp(l)
        all_sents += [s.text.strip() for s in doc.sents if s.text.strip()]
    return all_sents


display_view = st.sidebar.selectbox(
    'Select Display',
    ('Data Input', 'Alignment Explorer'))


if display_view == 'Data Input':
    st.subheader('Data Input')
    src_text_area = st.text_area(
        'Source Sentences', '\n'.join(session.src_lines))
    tgt_text_area = st.text_area(
        'Target Sentences', '\n'.join(session.tgt_lines))
    window_size = st.sidebar.slider("Window Size", 1, 100, value=5)
    segment_sents = st.sidebar.checkbox('Segment Sentences', value=True)

    if st.button("Align"):
        session.src_lines = src_text_area.splitlines()
        session.tgt_lines = tgt_text_area.splitlines()
        if segment_sents:
            session.src_lines = segment_sentences(session.src_lines)
            session.tgt_lines = segment_sentences(session.tgt_lines)

        session.df = get_alignment_df(session.src_lines, session.tgt_lines,
                                      window_size=window_size)
        # st.balloons()
        st.write("Switch to the Alignment Explorer to view alignment")

    if st.button("Clear Input"):
        session.src_lines, session.tgt_lines = [], []
        session.df = None


if display_view == 'Alignment Explorer':
    st.subheader('Alignment Explorer')

    if session.df is not None:
        sort_by = st.sidebar.selectbox('Order By', session.df.columns)
        descending = st.sidebar.checkbox('Descending', value=True)

        sentence_len_ratio = st.sidebar.slider("Sentence Length Ratio Less Than",
                                               0.0, 5.0, value=5.0)

        match_score = st.sidebar.slider("Match Score More Than",
                                        0.0, 1.0, value=0.0)

        margin_second_best = st.sidebar.slider("Margin Second Best More Than",
                                               0.0, 1.0, value=0.0)

        margin_avg = st.sidebar.slider("Margin Avg More Than",
                                       0.0, 1.0, value=0.0)

        ratio_second_best = st.sidebar.slider("Ratio Second Less Than",
                                              0.0, 1.0, value=1.0)

        ratio_avg = st.sidebar.slider("Ratio Second Best Less Than",
                                      0.0, 1.0, value=1.0)

        df = session.df
        df = df[
            (df["Sentence Length Ratio"] <= sentence_len_ratio) &
            (df["Match Score"] >= match_score) &
            (df["Margin Second Best"] >= margin_second_best) &
            (df["Margin Avg"] >= margin_avg) &
            (df["Ratio Second Best"] <= ratio_second_best) &
            (df["Ratio Avg"] <= ratio_avg)]

        df = df.sort_values(by=[sort_by], ascending=not descending)

        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        st.table(df)
    else:
        st.write("Switch the Data Input Display to align text.")
