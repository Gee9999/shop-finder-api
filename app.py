import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Shop Finder | Powered by Proto Trading", layout="centered")

# Logo and title using uploaded image
st.image("/mnt/data/ProtoLogoXS.png", width=140)
st.markdown("## Shop Finder  
**Powered by Proto Trading**", unsafe_allow_html=True)
st.markdown("---")

# --- Inputs ---
categories_input = st.text_area("📦 Product Categories (one per line)", height=100, help="e.g. beads, handbags, electronics")
country = st.selectbox("🌍 Country", sorted([
    "South Africa", "Kenya", "Nigeria", "Ghana", "Namibia", "Botswana", "Zimbabwe", "Uganda", "Tanzania", "Zambia", "Mozambique", "Egypt", "Ethiopia", "Morocco", "Rwanda"
]), help="Select a country in Africa")

city = st.text_input("🏙️ City (optional)", help="Optional: Cape Town, Nairobi, etc.")

extra_keywords = st.text_input("➕ Extra Keywords (optional)", help="Add more like 'importer, manufacturer'")
num_results = st.slider("🔁 Max results per search", 1, 20, 10)

keyword_variants = ["supplier", "wholesaler", "distributor", "store", "shop"]

if extra_keywords:
    keyword_variants += [kw.strip() for kw in extra_keywords.split(",") if kw.strip()]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

if st.button("🔍 Find Leads"):
    if not categories_input:
        st.warning("Please enter at least one product category.")
    else:
        categories = [line.strip() for line in categories_input.splitlines() if line.strip()]
        all_data = []
        seen_urls = set()

        location = f"{city}, {country}" if city else country

        with st.spinner("Searching the web..."):
            with DDGS(headers=headers) as ddgs:
                for cat in categories:
                    for variant in keyword_variants:
                        query = f"{cat} {variant} in {location}"
                        try:
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
                                        "location": location,
                                        "query": query
                                    })
                        except Exception as e:
                            st.error(f"❌ Error on query: {query}\n{str(e)}")

        if all_data:
            df = pd.DataFrame(all_data)
            st.success(f"✅ Found {len(df)} unique leads.")
            st.dataframe(df)

            # Excel download
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            filename = f"shop_finder_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            st.download_button("📥 Download Excel", buffer, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.info("No results found. Try other keywords or categories.")
