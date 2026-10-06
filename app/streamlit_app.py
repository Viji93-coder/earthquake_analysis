import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from analytics import ANALYTICS
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# Database Connection & Data Loading

password = quote_plus("*********")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/global")

@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM global_table", con=engine)
    df["time"] = pd.to_datetime(df["time"])
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["month_name"] = df["time"].dt.month_name()
    df["day_name"] = df["time"].dt.day_name()
    return df

df = load_data()

# ==================================================
# Page Config
# =================================================
st.set_page_config(
    page_title="Earthquake Analytics Dashboard",
    page_icon="🌍",
    layout="wide")

earthquake_url = r"C:\Users\ADMIN\OneDrive\Desktop\viji\Earthquake_Analytics_Project\SCEMD-earthquake.jpg"
st.image( earthquake_url,use_container_width=True)

#===================================================
# SIDEBAR
# ==================================================
st.sidebar.title("🌍 Global Seismic Trends")

# ====================================================
# Sidebar Menu (Native Segmented Control)
# ====================================================
from streamlit_option_menu import option_menu

# ===================================================
# Sidebar Menu (streamlit-option-menu)
# =================================================
with st.sidebar:
    menu = option_menu(
        menu_title="",
        options=["Extracted Data", "Cleaning", "Analytics"],
        icons=["database", "journal-check", "bar-chart-fill"],  # Bootstrap icons
        menu_icon="compass",
        default_index=0,
        styles={
            "container": {"padding": "5px!"},
            "icon": {"font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "2px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff4b4b", "color": "white"},})


# ==================================================
# Analytics Module
# -=================================================

def run_query(query):
   return pd.read_sql(query, engine)

if menu == "Analytics":
    st.title("🌍 Earthquake Analytics Dashboard")

    # Select and run dynamic analytics function
    analysis = st.selectbox("Select Analysis",list(ANALYTICS.keys()))
    
    result = ANALYTICS[analysis]()
    st.dataframe(result, use_container_width=True)

    if analysis == "1. Top 10 Strongest Earthquakes":
      
        chart_df = result.sort_values(
            by="mag",
            ascending=True)

        fig = px.bar(
            chart_df,
            x="mag",
            y="Country",
            orientation="h",
            color="mag",
            text="mag",
            title="Top 10 Strongest Earthquakes",
            color_continuous_scale="Reds")

        st.plotly_chart(
            fig,
            use_container_width=True)

    
    #=============================================================
    # Line Chart: Year vs Type
    ##=========================================================
    st.subheader(" Earthquake seismic yearly summary with types ")
    yearly_type = (
        df.groupby(["year", "type"])
        .size()
        .reset_index(name="earthquake_count"))

    fig2 = px.line(
        yearly_type,
        x="year",
        y="earthquake_count",
        color="type",
        markers=True,
        title="Earthquake Trend by Year and Type")

    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Earthquake Count")

    st.plotly_chart(
        fig2,
        use_container_width=True )

elif menu == "Extracted Data":

    st.title("📄 Raw Data View")

    # ----------------------------------
    # Filters in One Line
    # ----------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_year = st.selectbox(
            "📅 Year",
            ["All"] + sorted(df["year"].dropna().unique().tolist())
        )

    with col2:
        selected_month = st.selectbox(
            "🗓️ Month",
            ["All"] + sorted(df["month_name"].dropna().unique().tolist())
        )

    with col3:
        rows_per_page = st.selectbox(
            "📄 Rows",
            [10, 25, 50, 100],
            index=1
        )

    # Apply Filters
    filtered_result = df.copy()

    if selected_year != "All":
        filtered_result = filtered_result[
            filtered_result["year"] == selected_year
        ]

    if selected_month != "All":
        filtered_result = filtered_result[
            filtered_result["month_name"] == selected_month
        ]

    total_rows = len(filtered_result)

    total_pages = max(
        1,
        (total_rows + rows_per_page - 1) // rows_per_page
    )

    with col4:
        page = st.number_input(
            "📖 Page",
            min_value=1,
            max_value=total_pages,
            value=1
        )

    # Pagination
    start_row = (page - 1) * rows_per_page
    end_row = start_row + rows_per_page


    page_data = filtered_result.iloc[
        start_row:end_row
    ]

    st.info(
        f"Showing {len(page_data)} records out of {total_rows}"
    )

    st.dataframe(
        page_data,
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"Page {page} of {total_pages}"
    )


elif menu == "Cleaning":
    st.title("🧹 Cleaned Data")
    cleaned_df = pd.read_csv("data/processed/global_table.csv")
    st.dataframe(cleaned_df,use_container_width=True)