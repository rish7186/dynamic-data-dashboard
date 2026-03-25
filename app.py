import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Smart Dashboard", layout="wide")

st.title("🤖 Smart Data Dashboard")

# Upload file
file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # Detect column types
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    st.sidebar.header("⚙️ Customize")

    # Numeric column
    sales_col = st.sidebar.selectbox(
        "Numeric Column",
        numeric_cols,
        index=0 if numeric_cols else None,
        key="sales_col"
    )

    # Category column
    category_col = st.sidebar.selectbox(
        "Category Column",
        categorical_cols,
        index=0 if categorical_cols else None,
        key="category_col"
    )

    # Prevent same selection
    region_options = [col for col in categorical_cols if col != category_col]

    region_col = st.sidebar.selectbox(
        "Region Column",
        region_options,
        key="region_col"
    )

    # 🎛️ Filters
    st.sidebar.subheader("🔍 Filters")

    # Category filter
    if category_col:
        selected_category = st.sidebar.multiselect(
            f"Filter {category_col}",
            df[category_col].unique(),
            default=df[category_col].unique(),
            key="category_filter"
        )
        if selected_category:
            df = df[df[category_col].isin(selected_category)]

    # Region filter
    if region_col:
        selected_region = st.sidebar.multiselect(
            f"Filter {region_col}",
            df[region_col].unique(),
            default=df[region_col].unique(),
            key="region_filter"
        )
        if selected_region:
            df = df[df[region_col].isin(selected_region)]

    # 🚨 Handle empty data
    if df.empty:
        st.error("⚠️ No data available with selected filters. Try different options.")
        st.stop()

    # 📊 Metrics
    if sales_col:
        total = df[sales_col].sum()
        avg = df[sales_col].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total", f"{total:.2f}")
        col2.metric("📊 Average", f"{avg:.2f}")
        col3.metric("📦 Rows", len(df))

    # 📈 Charts
    if sales_col and category_col:
        st.subheader("📊 Category Analysis")
        fig1 = px.bar(df, x=category_col, y=sales_col, color=category_col)
        st.plotly_chart(fig1, use_container_width=True, key="chart1")

    if sales_col and region_col:
        st.subheader("🌍 Region Distribution")
        fig2 = px.pie(df, names=region_col, values=sales_col)
        st.plotly_chart(fig2, use_container_width=True, key="chart2")

    # 🏆 Top 5
    if sales_col and category_col:
        st.subheader("🏆 Top 5 Insights")
        top = df.groupby(category_col)[sales_col].sum().nlargest(5).reset_index()
        fig3 = px.bar(top, x=category_col, y=sales_col, color=category_col)
        st.plotly_chart(fig3, use_container_width=True, key="chart3")

    # 🧠 AI Insights
    if sales_col and category_col:
        st.subheader("🧠 AI Insights")

        grouped = df.groupby(category_col)[sales_col].sum()

        if not grouped.empty:
            top_cat = grouped.idxmax()
            low_cat = grouped.idxmin()

            st.success(f"🚀 Best performing category: **{top_cat}**")
            st.warning(f"⚠️ Lowest performing category: **{low_cat}**")
            st.info(f"📈 Total Value: **{total:.2f}**")

    # 📥 Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Data",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

else:
    st.info("👆 Upload a dataset to begin")