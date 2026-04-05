
# ============================================================
# 01: Market Basket Analysis — Streamlit Web Application
# ============================================================
# Association Rule Learning | FP-Growth Recommender
# Dataset: UCI Online Retail II (UK Only)
# ============================================================

import streamlit as st
import pandas as pd
import joblib
import os


# ============================================================
## 1.1 - Page Configuration
# ============================================================

st.set_page_config(
    page_title="Market Basket Recommender",
    page_icon="🛒",
    layout="centered"
)


# ============================================================
## 1.2 - Load Model
# ============================================================

# Load FP-Growth rules from saved pickle file
@st.cache_resource
def load_rules():
    model_path = os.path.join(os.path.dirname(__file__), 'Model', 'fpgrowth_rules.pkl')
    df_rules = joblib.load(model_path)
    return df_rules

df_fpgrowth_rules = load_rules()


# ============================================================
## 1.3 - Extract Unique Products
# ============================================================

# Pull all unique antecedent items for the dropdown | frozenset → flat list
all_products = sorted(set(
    item
    for itemset in df_fpgrowth_rules['antecedents']
    for item in itemset
))


# ============================================================
## 1.4 - Recommendation Function
# ============================================================

def get_recommendations(selected_product, df_rules, top_n=10):
    """
    Filter rules where selected_product is in antecedents.
    Return top N consequents sorted by lift then confidence.
    """
    # Filter rules containing selected product in antecedents
    mask = df_rules['antecedents'].apply(lambda x: selected_product in x)
    df_filtered = df_rules[mask].copy()

    if df_filtered.empty:
        return pd.DataFrame()

    # Explode consequents | one row per recommended item
    df_filtered['recommended_item'] = df_filtered['consequents'].apply(
        lambda x: ', '.join(list(x))
    )

    # Sort by lift descending, then confidence descending
    df_filtered = df_filtered.sort_values(
        by=['lift', 'confidence'],
        ascending=[False, False]
    ).head(top_n)

    # Select display columns only
    df_output = df_filtered[['recommended_item', 'confidence', 'lift', 'support']].reset_index(drop=True)
    df_output.index += 1  # | Start index from 1 for display

    # Round metric columns
    df_output['confidence'] = df_output['confidence'].round(4)
    df_output['lift']       = df_output['lift'].round(4)
    df_output['support']    = df_output['support'].round(4)

    return df_output


# ============================================================
## 1.5 - UI Layout
# ============================================================

# ---- Header ----
st.title("🛒 Market Basket Recommender")
st.markdown("**Association Rule Learning** — FP-Growth Model | UK Online Retail")
st.markdown("---")

# ---- Sidebar Info ----
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app uses **FP-Growth** association rules
    to recommend products frequently bought together.

    ---
    **Model Stats**
    - Rules: 398
    - Avg Confidence: 0.3941
    - Avg Lift: 12.6258
    - Max Lift: 57.0593

    ---
    **How to use**
    1. Select a product
    2. Choose how many recommendations
    3. Click **Get Recommendations**
    """)
    st.markdown("---")
    st.caption("Dataset: UCI Online Retail II (UK Only)")


# ---- Product Selector ----
st.subheader("🔍 Select a Product")

selected_product = st.selectbox(
    label="Choose a product to find recommendations for:",
    options=all_products,
    index=0
)

# ---- Top N Slider ----
top_n = st.slider(
    label="Number of recommendations to show:",
    min_value=1,
    max_value=20,
    value=10
)

st.markdown("---")


# ============================================================
## 1.6 - Recommendation Output
# ============================================================

# ---- Recommend Button ----
if st.button("🚀 Get Recommendations", use_container_width=True):

    df_recommendations = get_recommendations(selected_product, df_fpgrowth_rules, top_n)

    st.markdown("---")

    if df_recommendations.empty:
        st.warning(f"⚠️ No recommendations found for **{selected_product}**.")
        st.info("Try selecting a different product from the dropdown.")

    else:
        st.success(f"✅ Top {len(df_recommendations)} recommendation(s) for: **{selected_product}**")
        st.markdown("*Customers who bought this also bought ...*")
        st.markdown(" ")

        # ---- Metrics Row ----
        top = df_recommendations.iloc[0]
        col1, col2, col3 = st.columns(3)

        col1.metric(
            label="🏆 Top Recommended",
            value=top['recommended_item'][:30] + ("…" if len(top['recommended_item']) > 30 else "")
        )
        col2.metric(
            label="📊 Confidence",
            value=f"{top['confidence']:.2%}"
        )
        col3.metric(
            label="⬆️ Lift",
            value=f"{top['lift']:.2f}"
        )

        st.markdown(" ")

        # ---- Results Table ----
        st.dataframe(
            df_recommendations.rename(columns={
                'recommended_item' : '🛍️ Recommended Product',
                'confidence'       : '📊 Confidence',
                'lift'             : '⬆️ Lift',
                'support'          : '📈 Support'
            }),
            use_container_width=True
        )

        # ---- Confidence Bar Chart ----
        st.markdown("---")
        st.subheader("📊 Confidence Scores")
        chart_data = df_recommendations.set_index('recommended_item')['confidence']
        st.bar_chart(chart_data)

        # ---- Lift Bar Chart ----
        st.subheader("⬆️ Lift Scores")
        lift_data = df_recommendations.set_index('recommended_item')['lift']
        st.bar_chart(lift_data)


# ============================================================
## 1.7 - Footer
# ============================================================

st.markdown("---")
st.markdown("<center><sub>🎓 CMLE : Capstone Project &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; Silver Badge &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; Association Rule Learning &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 2026 &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; Udula Kodagoda®️</sub></center>", unsafe_allow_html=True)
