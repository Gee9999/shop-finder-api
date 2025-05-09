import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
from io import BytesIO

st.set_page_config(page_title="Shop Finder", layout="centered")

st.title("🛍️ Real-Time Shop Finder")
st.markdown("Get real-time leads from DuckDuckGo based on category and location.")

# --- Inputs ---
categories_input = st.text_area("Enter product categories (one per line)", height=100)
location = st.text_input("Enter location (e.g. Cape Town)")
num_results = st.slider("Max results per search", min_value=1, max_value=20, value=10)

keyword_variants = ["supplier", "wholesaler", "distributor", "store", "shop"]

if st.button("🔍 Find Leads"):
    if not categories_input or not location:
        st.warning("Please enter both categories and a location.")
    else:
        categories = [line.strip() for line in categories_input.splitlines() if line.strip()]
        all_data = []
        seen_urls = set()

        with st.spinner("Searching..."):
            with DDGS() as ddgs:
                for cat in categories:
                    for variant in keyword_variants:
                        query = f"{cat} {variant} in {location}"
                        results = ddgs.text(query, region='wt-wt', safesearch='Off', max_results=num_results)
                        for r in results:
                            url = r.get("href")
                            if url and url not in seen_urls:
                                seen_urls.add(url)
                                all_data.append({
                                    "name": r.get("title"),
                                    "url": url,
                                    "snippet": r.get("body"),
                                    "category": cat,
                                    "location": location
                                })

        if all_data:
            df = pd.DataFrame(all_data)
            st.success(f"✅ Found {len(df)} unique leads.")
            st.dataframe(df)

            # Excel download
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            st.download_button("📥 Download Excel", buffer, file_name="shop_finder_leads.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.info("No results found. Try other keywords or locations.")
