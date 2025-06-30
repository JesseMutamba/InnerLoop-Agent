import streamlit as st
from main import fetch_headlines, cluster_headlines, summarize_cluster, TOPICS
from email_utils import send_email
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Inner Loop Trend Agent", layout="wide")
st.title("Inner Loop Daily Trend Brief")
st.caption("Your Gen-Z flavored, AI-powered pulse on what's trending.")

st.sidebar.header("Customize Your Brief")
num_clusters = st.sidebar.slider("Number of Trend Topics", 3, 8, 5)
selected_topics = st.sidebar.multiselect("Pick Focus Areas", TOPICS, default=TOPICS)

generate_btn = st.sidebar.button("Generate Trend Brief")

if generate_btn:
    with st.spinner("Fetching headlines and analyzing..."):
        headlines = []
        for topic in selected_topics:
            headlines += fetch_headlines(topic)

        clusters = cluster_headlines(headlines, n_clusters=num_clusters)

        summaries = []
        for i, (cluster_id, titles) in enumerate(clusters.items(), start=1):
            with st.expander(f"Topic {i}", expanded=False):
                st.markdown("**Top Headlines:**")
                for title in titles[:3]:
                    st.markdown(f"- {title}")

                summary = summarize_cluster(titles)
                summaries.append(f"Topic {i}: {summary}")

                st.markdown("**Summary:**")
                st.success(summary)
                st.code(summary, language="markdown")

    full_summary = "\n\n".join(summaries)
    st.divider()
    st.subheader("Email This Trend Brief")
    email_address = st.text_input("Your Email Address", value="your_email@gmail.com")
    send_btn = st.button("Send Me the Brief")

    if send_btn:
        send_email(
            subject="Inner Loop Daily Trend Brief",
            body=full_summary,
            to_email=email_address,
            from_email=os.getenv("GMAIL_USER"),
            app_password=os.getenv("GMAIL_APP_PASSWORD")
        )
        st.success("📨 Sent!")
