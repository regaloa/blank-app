import streamlit as st
import database

st.set_page_config(page_title="目標設定", page_icon="🎯", layout="wide")
st.title("🎯 目標設定")
st.write("学習の目標（問題数および目標学習時間）を設定します。")

goal = database.get_goal()
goal_problems = goal.get("goal_problems", 10)
goal_time = goal.get("goal_time", 300)

with st.form("goal_form"):
    new_problems = st.number_input("目標問題数 (問)", min_value=1, max_value=1000, value=goal_problems)
    new_time = st.number_input("目標学習時間 (分)", min_value=10, max_value=10000, value=goal_time)
    submitted = st.form_submit_button("目標を保存")
    if submitted:
        database.update_goal(new_problems, new_time)
        st.success("目標を設定しました！")
