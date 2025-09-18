import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def show_visualizations(df: pd.DataFrame):
    st.header("📊 Financial Visualizations")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) == 0:
        st.warning("⚠️ No numeric columns available for visualization.")
        return

    col_choices = st.multiselect(
        "Select one or more columns to visualize",
        options=numeric_cols,
        default=[numeric_cols[0]]
    )

    if col_choices:
        st.subheader("📈 Trend Over Time")
        fig_line = px.line(
            df,
            y=col_choices,
            markers=True,
            title="Financial Trends",
            labels={"value": "Amount", "index": "Record"},
        )
        fig_line.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📊 Comparison of Metrics")
    fig_bar = px.bar(
        df,
        y=col_choices,
        barmode="group",
        title="Financial Distribution",
        labels={"value": "Amount", "index": "Record"},
    )
    fig_bar.update_traces(marker_line_width=1, opacity=0.8)
    fig_bar.update_layout(template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Correlation Heatmap ---
    if len(numeric_cols) > 1:
        st.subheader("🔗 Correlation Heatmap")
        corr = df[numeric_cols].corr()

        fig_heat = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="RdBu",
                zmin=-1, zmax=1,
                text=corr.round(2).values,
                texttemplate="%{text}",
                hoverongaps=False,
            )
        )
        fig_heat.update_layout(
            title="Correlation Between Financial Metrics",
            template="plotly_dark"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
