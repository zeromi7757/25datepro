import streamlit as st
import pandas as pd
import plotly.express as px
import koreanize_matplotlib  # 한글 깨짐 방지

# 페이지 설정
st.set_page_config(page_title="🗺️ 지역별 인구 구조 대시보드", layout="wide")

# -------------------------------
# 📥 데이터 로드
# -------------------------------
@st.cache_data
def load_data() -> tuple[pd.DataFrame, list, list]:
    """
    CSV를 읽고 필요한 컬럼 정리 및 연령 레이블 반환 (숫자)
    """
    df = pd.read_csv("/mnt/data/202505_202505_연령별인구현황_월간 (1).csv", encoding="cp949")
    df["지역"] = df["행정구역"].str.split("(").str[0].str.strip()

    # 연령별 컬럼만 필터링
    age_cols = [col for col in df.columns if "_계_" in col and (col.endswith("세") or "이상" in col)]

    # '2025년_계_0세' → 숫자만 추출 (0, 1, ..., 100)
    age_labels = []
    for col in age_cols:
        num = "".join(filter(str.isdigit, col.split("_")[-1]))
        if num == "":
            num = "100"  # '100세 이상'
        age_labels.append(int(num))

    # 콤마 제거 후 숫자로 변환
    for col in age_cols:
        df[col] = df[col].astype(str).str.replace(",", "", regex=False).astype(int)

    return df, age_cols, age_labels

# -------------------------------
# 🧩 UI 요소
# -------------------------------
st.title("🔍 지역별 인구 구조 대시보드")

df, age_cols, age_labels = load_data()

regions = sorted(df["지역"].unique())
selected = st.sidebar.multiselect("✅ 분석할 지역(복수 선택 가능)", regions, default=["서울특별시"])

if not selected:
    st.info("왼쪽 사이드바에서 최소 1개 지역을 선택하세요!")
    st.stop()

chart_type = st.sidebar.selectbox("차트 유형", ("꺾은선 그래프", "막대 그래프 (Population Pyramid용)"))

# -------------------------------
# 🔑 데이터 가공
# -------------------------------
subset = df[df["지역"].isin(selected)]
agg = subset.groupby("지역")[age_cols].sum().T
agg.index = age_labels  # 인덱스를 숫자 나이로 설정

# -------------------------------
# 📊 그래프 출력
# -------------------------------
if chart_type.startswith("꺾은선"):
    # 📈 꺾은선 그래프: x=나이, y=인구수
    fig = px.line(
        agg.reset_index().melt(id_vars="index", var_name="지역", value_name="인구 수"),
        x="index",
        y="인구 수",
        color="지역",
        labels={"index": "나이", "인구 수": "인구 수"},
        title="연령별 인구 분포 (선 그래프)"
    )

else:
    if len(selected) == 1:
        # 📊 단일 지역: 인구 피라미드
        pop = agg[selected[0]]
        pop_neg = pop * -1  # 왼쪽 값 (음수)

        pyr = pd.DataFrame({
            "나이": agg.index,
            "왼쪽": pop_neg,
            "오른쪽": pop
        })

        fig = px.bar(
            pyr.melt(id_vars="나이", var_name="방향", value_name="인구 수"),
            x="인구 수",
            y="나이",
            color="방향",
            orientation="h",
            labels={"나이": "나이", "인구 수": "인구 수"},
            title=f"{selected[0]} 인구 피라미드"
        )
    else:
        # 📊 다중 지역: 그룹 막대 그래프 (x=나이, y=인구수)
        df_long = agg.reset_index().melt(id_vars="index", var_name="지역", value_name="인구 수")
        fig = px.bar(
            df_long,
            x="index",
            y="인구 수",
            color="지역",
            barmode="group",
            labels={"index": "나이", "인구 수": "인구 수"},
            title="연령별 인구 분포 (막대 그래프)"
        )

fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
st.caption("📊 데이터 출처: 행정안전부 주민등록 인구 통계")
