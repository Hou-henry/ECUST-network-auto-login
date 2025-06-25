import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("登录时间间隔可视化（自动格式化时间间隔）")

file_path = "login_log.jsonl"

def format_minutes(m):
    if pd.isna(m):
        return "-"
    m = int(m)
    days = m // (24 * 60)
    hours = (m % (24 * 60)) // 60
    minutes = m % 60
    parts = []
    if days > 0:
        parts.append(f"{days} 天")
    if hours > 0:
        parts.append(f"{hours} 小时")
    if minutes > 0 or not parts:
        parts.append(f"{minutes} 分钟")
    return " ".join(parts)

if os.path.exists(file_path):
    df = pd.read_json(file_path, lines=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['last_login'] = pd.to_datetime(df['last_login'], errors='coerce')

    # 自动补全 elapsed_min
    df['elapsed_min'] = df.apply(
        lambda row: (row['timestamp'] - row['last_login']).total_seconds() / 60
        if pd.isna(row['elapsed_min']) and pd.notna(row['last_login']) else row['elapsed_min'],
        axis=1
    )

    # 新增格式化列
    df['elapsed_pretty'] = df['elapsed_min'].apply(format_minutes)

    if st.checkbox("显示原始数据表格（含格式化时间间隔）"):
        st.dataframe(df[['timestamp', 'elapsed_min', 'elapsed_pretty']])

    fig = px.line(
        df,
        x='timestamp',
        y='elapsed_min',
        markers=True,
        title='登录时间间隔（分钟）随时间变化',
        labels={'elapsed_min': '时间间隔 (分钟)', 'timestamp': '时间戳'},
        hover_data={'elapsed_min': False, 'elapsed_pretty': True}  # 只显示格式化时间
    )

    st.plotly_chart(fig)
else:
    st.error("未找到 login_log.jsonl 文件，请确保文件存在！")
