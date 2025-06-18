import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로 (Streamlit Cloud에서는 파일 업로드 위젯을 사용)
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949', engine='python')
    except:
        st.error("CSV 파일을 읽는 데 문제가 발생했습니다. 인코딩이나 파일 형식을 확인해주세요.")
        st.stop()

    # 기본 전처리 (컬럼명 확인 및 필요 컬럼 선택)
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
        ages.append(age_label)
        populations.append(int(str(latest_data[age_col]).replace(",", "")))

    # 인구 피라미드 그리기
    fig = go.Figure(go.Bar(
        x=populations,
        y=ages,
        orientation='h',
        marker=dict(color='skyblue')
    ))

    fig.update_layout(
        title=f"{selected_region} 인구 피라미드",
        xaxis_title="인구수",
        yaxis_title="연령",
        height=800
    )

    st.plotly_chart(fig)
else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
