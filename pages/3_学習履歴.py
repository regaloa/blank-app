import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="学習履歴", page_icon="📋", layout="wide")
st.title("📋 学習履歴")
st.write("これまでの学習の記録一覧です。")

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "study.db")

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT study_date as 日付, study_time as 時間分, category as カテゴリ, problem_name as 問題名, result as 結果, memo as メモ FROM study_logs ORDER BY id DESC", conn)
    conn.close()
    return df

try:
    df = get_all_logs()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("学習履歴がまだありません。")
except Exception as e:
    st.info("学習履歴データがまだありません。")
