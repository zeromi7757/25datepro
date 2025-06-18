# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("연령별 인구현황 시각화")

# ✅ 로컬 CSV 파일 경로 지정 (업로드 아님!)
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# CSV 읽기 (한글 CSV는 euc-kr 권장)
try:
    df = pd.read_csv(FILE_PATH, encoding='euc-kr')
except Exception as e:
    st.error(f"CSV 파일을 읽을 수 없습니다: {e}")
    st.stop()

# 컬럼 이름 정리
df.columns = df.columns.str.strip()

# 숫자 컬럼 쉼표 제거 + 숫자형 변환
for col in df.columns[1:]:
    df[col] = df[col].astype(str).str.replace(",", "").astype(int)

# 연령 컬럼만 추출
age_cols = [col for col in df.columns if "세" in col or "이상" in col]

# 행정구역 선택
region = st.selectbox("행정구역을 선택하세요", df["행정구역"].unique())

# 선택한 행정구역 데이터
region_data = df[df["행정구역"] == region][age_cols].T.reset_index()
region_data.columns = ["연령", "인구수"]

# 연령 컬럼 정리 (숫자만 추출)
region_data["연령"] = region_data["연령"].str.extract(r'(\d+)').astype(int)

# Plotly 시각화
fig = px.bar(region_data, x="연령", y="인구수",
             labels={"연령": "연령(세)", "인구수": "인구수"},
             title=f"{region} 연령별 인구 분포")

st.plotly_chart(fig)

# 데이터프레임 확인
st.dataframe(region_data)
