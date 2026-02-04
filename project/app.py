"""Streamlit UI template for local-first feedback analytics.

Streamlit code is commented out so you can enable it when running locally.
"""

from __future__ import annotations

# The Streamlit UI is intentionally commented out. Uncomment when ready to run
# locally with Streamlit installed.
#
# import io
# from pathlib import Path
#
# import pandas as pd
# import streamlit as st
#
# from logic import AnalysisConfig, analyze_series
# from utils import detect_feedback_column
# from visualization import (
#     plot_distribution,
#     plot_grouped_distribution,
#     plot_negative_deep_dive,
#     plot_score_vs_sentiment,
# )
#
# st.set_page_config(page_title="Feedback Analytics", layout="wide")
#
# style_path = Path(__file__).with_name("styles.css")
# if style_path.exists():
#     st.markdown(f"<style>{style_path.read_text()}</style>", unsafe_allow_html=True)
#
# st.markdown(
#     """
#     <div class="app-header">
#       <h1>Local-First Feedback Analytics</h1>
#       <p>Private, offline-ready insights for weekly institutional feedback reviews.</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )
#
# st.markdown(
#     """
#     <div class="section-card">
#       <h3>Get Started</h3>
#       <p>Upload a CSV or XLSX file, confirm the feedback column, then run Quick or AI analysis.</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )
#
# uploaded_file = st.file_uploader("Upload feedback file", type=["csv", "xlsx"])
#
# if uploaded_file:
#     if uploaded_file.name.endswith(".csv"):
#         df = pd.read_csv(uploaded_file)
#     else:
#         df = pd.read_excel(uploaded_file)
#
#     st.subheader("Column Mapping")
#     detected_column = detect_feedback_column(df)
#     feedback_column = st.selectbox(
#         "Select feedback column",
#         options=df.columns,
#         index=list(df.columns).index(detected_column) if detected_column else 0,
#     )
#
#     st.sidebar.header("Analysis Mode")
#     quick_mode = st.sidebar.checkbox("Quick Analysis (Default)", value=True)
#     ai_mode = st.sidebar.checkbox("AI Deep Analysis", value=False)
#
#     mode = "quick"
#     model = "llama3.2"
#     if ai_mode and not quick_mode:
#         mode = "ai"
#         model = st.sidebar.selectbox("Select local model", ["llama3.2", "llama3.1"])
#     elif ai_mode and quick_mode:
#         st.sidebar.info("Quick mode is active. Disable Quick Analysis to use AI mode.")
#
#     st.sidebar.header("Aggregation")
#     aggregation_candidates = [
#         col
#         for col in df.columns
#         if col.lower()
#         in {"state", "district", "institute", "institution type", "institution_type"}
#     ]
#     aggregation_options = ["Overall"] + aggregation_candidates
#     aggregation = st.sidebar.selectbox("Group by", aggregation_options)
#
#     if st.button("Run Analysis"):
#         progress = st.progress(0)
#         config = AnalysisConfig(mode=mode, model=model)
#         results = analyze_series(df[feedback_column], config)
#         progress.progress(70)
#         result_df = pd.DataFrame(results)
#         enriched = pd.concat([df.reset_index(drop=True), result_df], axis=1)
#         progress.progress(100)
#
#         st.subheader("Results Overview")
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.pyplot(plot_distribution(enriched, "sentiment", "Sentiment Distribution"))
#         with col2:
#             st.pyplot(plot_distribution(enriched, "emotion", "Emotion Distribution"))
#         with col3:
#             st.pyplot(plot_distribution(enriched, "intent", "Intent Distribution"))
#
#         st.subheader("Deep Dives")
#         st.pyplot(plot_negative_deep_dive(enriched))
#         st.pyplot(plot_score_vs_sentiment(enriched))
#
#         if aggregation != "Overall":
#             st.subheader(f"Grouped View by {aggregation}")
#             st.pyplot(
#                 plot_grouped_distribution(
#                     enriched, aggregation, "sentiment", f"Sentiment by {aggregation}"
#                 )
#             )
#
#         st.subheader("Download Enriched Dataset")
#         buffer = io.StringIO()
#         enriched.to_csv(buffer, index=False)
#         st.download_button(
#             "Download CSV",
#             buffer.getvalue(),
#             file_name="feedback_enriched.csv",
#             mime="text/csv",
#         )
# else:
#     st.info("Upload a CSV or XLSX file to begin analysis.")
