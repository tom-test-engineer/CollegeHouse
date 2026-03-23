import streamlit as st

st.title("🥎 Stevens Point 'Softball House' Investment Model")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Acquisition & Financing")
price = st.sidebar.number_input("Purchase Price ($)", value=320000, step=5000)
down_payment_pct = st.sidebar.slider("Down Payment (%)", 0, 100, 20)
interest_rate = st.sidebar.slider("Interest Rate (%)", 3.0, 10.0, 6.5)

st.sidebar.header("2. Revenue (The Teammates)")
num_rooms = st.sidebar.slider("Total Bedrooms", 3, 6, 5)
rent_per_room = st.sidebar.number_input("Monthly Rent per Player ($)", value=650)

st.sidebar.header("3. Monthly Expenses (OPEX)")
taxes_insurance = st.sidebar.number_input("Monthly Taxes/Insurance ($)", value=450)
maintenance_pct = st.sidebar.slider("Monthly Maintenance (% of Price)", 0.0, 2.0, 0.1)

# --- CALCULATIONS ---
loan_amount = price * (1 - (down_payment_pct / 100))
monthly_rate = (interest_rate / 100) / 12
n_payments = 30 * 12
mortgage_pi = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)

total_monthly_out = mortgage_pi + taxes_insurance + (price * (maintenance_pct / 100))
total_revenue = rent_per_room * (num_rooms - 1) # Daughter lives for free
net_cash_flow = total_revenue - total_monthly_out

# --- DASHBOARD OUTPUT ---
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Mortgage (P&I)", f"${mortgage_pi:,.2f}")
col2.metric("Total Monthly Revenue", f"${total_revenue:,.2f}")
col3.metric("Net Cash Flow", f"${net_cash_flow:,.2f}", delta_color="normal")

st.divider()

if net_cash_flow > 0:
    st.success(f"✅ Success! You are cash-flow positive by ${net_cash_flow:,.2f}/month while your daughter pays $0.")
else:
    st.warning(f"⚠️ Gap: You are short by ${abs(net_cash_flow):,.2f}/month to achieve total break-even.")

st.info(f"**Insight:** By not paying the average UWSP Room & Board (~$800/mo), you are effectively 'saving' an additional $9,600 per year.")
