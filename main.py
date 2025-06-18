import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("대한민국 연령별 인구 구조 시각화")

# CSV 파일 경로 (루트 폴더 기준)
file_path = '202505_202505_연령별인구현황_월간.csv'

# CSV 읽기
try:
    df = pd.read_csv(file_path, encoding='cp949', engine='python')
except Exception as e:
    st.error(f"CSV 파일을 읽는 데 문제가 발생했습니다: {e}")
    st.stop()

# 파일 구조 확인 및 기본 전처리
if '행정구역' not in df.columns:
    st.error("파일에 '행정구역' 컬럼이 없습니다. 올바른 파일을 업로드했는지 확인해주세요.")
    st.stop()

# 지역 선택
regions = df['행정구역'].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

region_data = df[df['행정구역'] == selected_region]

# 연령별 컬럼만 추출 (예: '0세', '1세', ..., '100세 이상')
age_columns = [col for col in df.columns if ('세' in col or '이상' in col) and col != '총인구수']

# 최근 데이터 한 건만 사용 (보통 가장 마지막 월 기준)
latest_data = region_data.iloc[-1]

# 연령과 인구수 데이터 준비
ages = []
populations = []
for age_col in age_columns:
    age_label = age_col.replace('세','').replace('이상','+')
    try:
        population = int(str(latest_data[age_col]).replace(",", "").strip())
    except:
        population = 0
    ages.append(age_label)
    populations.append(population)

# 인구 피라미드 그리기
fig = go.Figure(go.Bar(
    x=populations,
    y=ages,
    orientation='h',
    marker=dict(color='skyblue')
))

fig.update_layout(
    title=f"{selected_region} 인구 피라미드 (최신월)",
    xaxis_title="인구수",
    yaxis_title="연령",
    height=800
)

st.plotly_chart(fig)
