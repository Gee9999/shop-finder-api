import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
from io import BytesIO

st.set_page_config(page_title="Shop Finder", layout="centered")

st.title("🛍️ Real-Time Shop Finder")
st.markdown("Get real-time leads based on product category and location.")

# --- Inputs ---
categories_input = st.text_area("Enter product categories (one per line)", height=100)
location = st.text_input("Enter location (e.g. Cape Town)")
num_results = st.slider("Number of results per category", min_value=1, max_value=20, value=5)

if st.button("🔍 Find Leads"):
    if not categories_input or not location:
        st.warning("Please enter both categories and a location.")
    else:
        categories = [line.strip() for line in categories_input.splitlines() if line.strip()]
        all_data = []

        with st.spinner("Searching..."):
            with DDGS() as ddgs:
                for cat in categories:
                    search_term = f"{cat} suppliers in {location}"
                    results = ddgs.text(search_term, region='wt-wt', safesearch='Off', max_results=num_results)
                    for r in results:
                        all_data.append({
                            "name": r.get("title"),
                            "url": r.get("href"),
                            "snippet": r.get("body"),
                            "category": cat,
                            "location": location
                        })

        if all_data:
            df = pd.DataFrame(all_data)
            st.success(f"✅ Found {len(df)} results.")
            st.dataframe(df)

            # Download button
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            st.download_button("📥 Download Excel", buffer, file_name="shop_finder_leads.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.info("No results found. Try different keywords or reduce the number of results.")
