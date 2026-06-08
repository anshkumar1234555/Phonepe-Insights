import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ DATABASE CONNECTION ------------------
conn = sqlite3.connect(r"C:\Users\kumar\OneDrive\Desktop\phonepe project\phonepe.db")

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# ------------------ TITLE ------------------
st.title("📊 PhonePe Transaction Insights Dashboard")
st.markdown("Analyze digital payment trends across India")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Filters")
st.sidebar.write("Select Year and Quarter")

# ------------------ LOAD DATA ------------------
df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)

# ------------------ FILTERS ------------------
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(df["Quarter"].unique()))

filtered_df = df[(df["Year"] == year) & (df["Quarter"] == quarter)]

# ------------------ KPIs ------------------
total_amount = filtered_df["Amount"].sum()
total_count = filtered_df["Count"].sum()
avg_value = total_amount / total_count if total_count != 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Amount", f"₹ {total_amount:,.0f}")
col2.metric("📊 Total Transactions", int(total_count))
col3.metric("📈 Avg Transaction", f"₹ {avg_value:.2f}")

# ------------------ PREP DATA ------------------
type_df = filtered_df.groupby("Type").agg({
    "Amount": "sum",
    "Count": "sum"
}).reset_index()

# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Amount by Type")
    fig1, ax1 = plt.subplots()
    sns.barplot(x="Type", y="Amount", data=type_df, ax=ax1)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with col2:
    st.subheader("Transactions by Type")
    fig2, ax2 = plt.subplots()
    sns.barplot(x="Type", y="Count", data=type_df, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# ------------------ PIE CHART ------------------
st.subheader("Transaction Share by Type")

fig3, ax3 = plt.subplots()
ax3.pie(type_df["Amount"], labels=type_df["Type"], autopct='%1.1f%%')
st.pyplot(fig3)

# ------------------ YEARLY TREND ------------------
st.subheader("Yearly Growth")

year_df = df.groupby("Year")["Amount"].sum().reset_index()

fig4, ax4 = plt.subplots()
sns.lineplot(x="Year", y="Amount", data=year_df, marker="o", ax=ax4)

st.pyplot(fig4)

# ------------------ QUARTER TREND ------------------
st.subheader("Quarter-wise Transactions")

quarter_df = df.groupby("Quarter")["Amount"].sum().reset_index()

fig5, ax5 = plt.subplots()
sns.barplot(x="Quarter", y="Amount", data=quarter_df, ax=ax5)

st.pyplot(fig5)

# ------------------ INSIGHTS ------------------
st.subheader("📌 Key Insights")

st.write("""
- Digital transactions are increasing year by year.
- Peer-to-peer and merchant payments dominate usage.
- Certain quarters show higher activity due to seasonal trends.
- Average transaction value indicates user spending behavior.
""")

# ------------------ RAW DATA ------------------
st.subheader("Raw Data")
st.dataframe(filtered_df)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Developed for Internship Project 🚀")