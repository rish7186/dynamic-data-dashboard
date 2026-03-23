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

    # 🤖 Auto-select best columns
    sales_col = numeric_cols[0] if numeric_cols else None
    category_col = categorical_cols[0] if categorical_cols else None
    region_col = categorical_cols[1] if len(categorical_cols) > 1 else category_col

    st.sidebar.header("⚙️ Customize")

    sales_col = st.sidebar.selectbox("Numeric Column", numeric_cols, index=0 if numeric_cols else None)
    category_col = st.sidebar.selectbox("Category Column", categorical_cols, index=0 if categorical_cols else None)
    region_col = st.sidebar.selectbox("Region Column", categorical_cols, index=1 if len(categorical_cols) > 1 else 0)

    # 🎛️ Dynamic Filters
    st.sidebar.subheader("🔍 Filters")

    if category_col:
        selected_category = st.sidebar.multiselect(
            f"Filter {category_col}",
            df[category_col].unique(),
            default=df[category_col].unique()
        )
        df = df[df[category_col].isin(selected_category)]

    if region_col:
        selected_region = st.sidebar.multiselect(
            f"Filter {region_col}",
            df[region_col].unique(),
            default=df[region_col].unique()
        )
        df = df[df[region_col].isin(selected_region)]

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
        st.plotly_chart(fig1, use_container_width=True)

    if sales_col and region_col:
        st.subheader("🌍 Region Distribution")
        fig2 = px.pie(df, names=region_col, values=sales_col)
        st.plotly_chart(fig2, use_container_width=True)

    # 🏆 Top 5
    if sales_col and category_col:
        st.subheader("🏆 Top 5 Insights")
        top = df.groupby(category_col)[sales_col].sum().nlargest(5).reset_index()
        fig3 = px.bar(top, x=category_col, y=sales_col, color=category_col)
        st.plotly_chart(fig3, use_container_width=True)

    # 🧠 Smart Insights
    if sales_col and category_col:
        st.subheader("🧠 AI Insights")

        top_cat = df.groupby(category_col)[sales_col].sum().idxmax()
        low_cat = df.groupby(category_col)[sales_col].sum().idxmin()

        st.success(f"🚀 Best performing category: **{top_cat}**")
        st.warning(f"⚠️ Lowest performing category: **{low_cat}**")
        st.info(f"📈 Total Value: **{total:.2f}**")

    # 📥 Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data", csv, "filtered_data.csv", "text/csv")

else:
    st.info("👆 Upload a dataset to begin")