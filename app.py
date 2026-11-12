
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Business KPI Dashboard", layout="wide")

df = pd.read_csv('customer_churn_sample (4).csv')
st.title("Business KPI Dashboard")
st.subheader("Customer Churn and Revenue Analysis")

st.sidebar.header("Dashboard Filters")

contracts = st.sidebar.multiselect(
    "Contract Type",
    df['ContractType'].unique(),
    default=list(df['ContractType'].unique())
)

payments = st.sidebar.multiselect(
    "Payment Method",
    df['PaymentMethod'].unique(),
    default=list(df['PaymentMethod'].unique())
)

min_t = int(df['TenureMonths'].min())
max_t = int(df['TenureMonths'].max())

tenure = st.sidebar.slider(
    "Tenure Months", min_t, max_t, (min_t, max_t)
)

data = df[
    (df['ContractType'].isin(contracts)) &
    (df['PaymentMethod'].isin(payments)) &
    (df['TenureMonths'].between(tenure[0], tenure[1]))
]

total = len(data)
churned = (data['Churn'] == 'Yes').sum()
retained = (data['Churn'] == 'No').sum()

churn_rate = churned / total * 100 if total else 0
retention_rate = retained / total * 100 if total else 0

risk = data.loc[data['Churn'] == 'Yes', 'MonthlyCharges'].sum()
avg_tenure = data['TenureMonths'].mean() if total else 0

st.subheader("Business KPIs")

a, b, c, d = st.columns(4)
a.metric("Total Customers", total)
b.metric("Churn Rate", f"{churn_rate:.2f}%")
c.metric("Retention Rate", f"{retention_rate:.2f}%")
d.metric("Revenue at Risk", f"{risk:.2f}")

st.metric("Average Tenure", f"{avg_tenure:.2f} months")

def show_bar(title, series):
    st.subheader(title)
    if len(series) == 0:
        st.info("No data for selected filters.")
        return

    maximum = max(series.values) if max(series.values) > 0 else 1

    for label, value in series.items():
        percent = value / maximum * 100
        st.write(f"**{label}** — {value:.2f}")
        st.markdown(
            f"""
            <div style="background:#eeeeee;border-radius:8px;height:22px;">
              <div style="background:#2878B5;width:{percent}%;
              height:22px;border-radius:8px;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )

show_bar(
    "Customer Churn Distribution",
    data['Churn'].value_counts()
)

show_bar(
    "Revenue by Subscription Type",
    data.groupby('SubscriptionType')['MonthlyCharges'].sum()
)

st.subheader("Churn by Contract Type")

contract = pd.crosstab(data['ContractType'], data['Churn'])
st.markdown(contract.to_html(index=False), unsafe_allow_html=True)

st.subheader("Customer Data")
st.markdown(data.to_html(index=False), unsafe_allow_html=True)
