import streamlit as st
import time
import SessionState
import base64

from window_align import get_scoring_matrix_from_lines, make_alignment_dataframe
from matchscoring import *

session = SessionState.get(src_lines=[], tgt_lines=[], df=None)

st.title("Windowed LASER Aligner")
st.text("By Tarun")


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Right clock and download csv file</a>'
    return href


def get_alignment_df(src_lines, tgt_lines, src_lang="en", tgt_lang="en", window_size=5):
    scoring_matrix = get_scoring_matrix_from_lines(
        src_lines, tgt_lines, src_lang, tgt_lang)
    df = make_alignment_dataframe(
        src_lines, tgt_lines, scoring_matrix, window_size)
    del scoring_matrix
    return df


display_view = st.sidebar.selectbox(
    'Select Display',
    ('Data Input', 'Alignment Explorer'))


if display_view == 'Data Input':
    st.subheader('Data Input')
    src_text_area = st.text_area('Source Sentences')
    tgt_text_area = st.text_area('Target Sentences')
    if st.button("Align"):
        session.src_lines = src_text_area.splitlines()
        session.tgt_lines = tgt_text_area.splitlines()
        session.df = get_alignment_df(session.src_lines, session.tgt_lines)
        st.balloons()
        st.write("Switch to the Alignment Explorer to view alignment")


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

        st.table(session.df.sort_values(by=[sort_by], ascending=descending))
        st.markdown(get_table_download_link(
            session.df), unsafe_allow_html=True)
    else:
        st.write("Switch the Data Input Display to align text.")
