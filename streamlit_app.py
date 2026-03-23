import streamlit as st
import pandas as pd

# Initialize "Database" in session memory
if 'listings' not in st.session_state:
    st.session_state.listings = []

st.set_page_config(page_title="Softball House Model", layout="wide")
st.title("🥎 Stevens Point Investment & Comparison")

# --- APP TABS ---
tab1, tab2 = st.tabs(["Add/Model Listing", "Compare Saved Houses"])

with tab1:
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.header("Listing Details")
        name = st.text_input("House Nickname (e.g., 'Franklin St 5-Bed')")
        price = st.number_input("Purchase Price ($)", value=320000)
        num_players = st.slider("Number of Renting Teammates", 1, 6, 4)
        rent_rate = st.number_input("Monthly Rent per Player ($)", value=650)
        
    with col_b:
        st.header("Operating Costs")
        int_rate = st.slider("Mortgage Interest (%)", 4.0, 9.0, 6.5)
        tax_ins = st.number_input("Monthly Tax/Ins ($)", value=450)
        
        # Calculations
        loan = price * 0.8  # Assuming 20% down
        m_rate = (int_rate / 100) / 12
        mortgage = loan * (m_rate * (1 + m_rate)**360) / ((1 + m_rate)**360 - 1)
        
        monthly_exp = mortgage + tax_ins
        monthly_rev = num_players * rent_rate
        cash_flow = monthly_rev - monthly_exp
        
        # UWSP Room & Board Comparison (2026 Estimates)
        avoided_cost = 9280 / 12 # Monthly savings from daughter not being in dorms
        true_roi = cash_flow + avoided_cost

        st.metric("Net Cash Flow", f"${cash_flow:,.2f}")
        st.metric("Total Monthly Value (incl. Savings)", f"${true_roi:,.2f}")

    if st.button("💾 Save Listing to Compare"):
        listing_data = {
            "Name": name, "Price": price, "Players": num_players,
            "Rent": rent_rate, "Cash Flow": cash_flow, "Total ROI": true_roi
        }
        st.session_state.listings.append(listing_data)
        st.success(f"Saved {name}!")

with tab2:
    st.header("Side-by-Side Comparison")
    if len(st.session_state.listings) > 0:
        df = pd.DataFrame(st.session_state.listings)
        st.table(df)
        
        if st.button("Clear All Listings"):
            st.session_state.listings = []
            st.rerun()
    else:
        st.info("No listings saved yet. Use Tab 1 to add some while house hunting!")
