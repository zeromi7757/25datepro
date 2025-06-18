# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("연령별 인구현황 시각화")

# ✅ 로컬 CSV 파일 경로 지정
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# CSV 읽기
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

# 연령 컬럼 숫자 추출
region_data["연령"] = region_data["연령"].str.extract(r'(\d+)').astype(int)

# ✅ x축, y축 바꿔서 Plotly 시각화 (가로 막대)
fig = px.bar(
    region_data,
    x="인구수",
    y="연령",
    orientation='h',
    labels={"연령": "연령(세)", "인구수": "인구수"},
    title=f"{region} 연령별 인구 분포 (가로 막대그래프)"
)

# y축 내림차순으로 뒤집기 (연령 높은 게 위로)
fig.update_yaxes(categoryorder='total ascending')

st.plotly_chart(fig)

# 데이터 확인
st.dataframe(region_data)
