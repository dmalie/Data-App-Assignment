import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")


import streamlit as st
import pandas as pd
import plotly.express as px

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("Superstore_sales_utf8.csv")
    # Explicit type conversion
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
category = st.sidebar.selectbox("Select Category", df["Category"].unique())
sub_categories = df[df["Category"] == category]["Sub_Category"].unique()
selected_sub_categories = st.sidebar.multiselect("Select Sub-Category", sub_categories, default=sub_categories)

# Filter data based on selections
filtered_data = df[
    (df["Category"] == category) &
    (df["Sub_Category"].isin(selected_sub_categories))
]

# Calculate metrics
total_sales = filtered_data["Sales"].sum()
total_profit = filtered_data["Profit"].sum()
selected_profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

# Calculate overall profit margin for delta comparison
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales else 0

# Calculate delta
profit_margin_delta = selected_profit_margin - overall_profit_margin

# Display metrics in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")
with col3:
    st.metric("Profit Margin", f"{selected_profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")

# Line chart with Plotly
st.write("### Sales Over Time for Selected Sub-Categories")
if not filtered_data.empty:
    sales_over_time = filtered_data.groupby("Order_Date")["Sales"].sum().reset_index()
    fig = px.line(sales_over_time, x="Order_Date", y="Sales", title="Sales Trend")
    st.plotly_chart(fig)
else:
    st.warning("No data available for the selected filters.")
