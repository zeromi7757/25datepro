import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 업로드 (또는 로컬 CSV 로드)
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded_file, encoding='cp949')  # 인코딩은 파일에 따라 조정 (cp949, utf-8 등)
    st.write("데이터 미리보기:", df.head())

    # 열 정보 출력
    st.write("열 정보:", df.columns.tolist())

    # 예: 특정 열 선택해서 시각화하기
    # 사용자가 선택하도록 설정
    x_axis = st.selectbox("X축 열 선택", df.columns)
    y_axis = st.selectbox("Y축 열 선택", df.columns)

    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
    st.plotly_chart(fig)
else:
    st.info("CSV 파일을 업로드해주세요.")
