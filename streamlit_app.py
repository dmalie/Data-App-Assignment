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
    df = pd.read_csv("Superstore_Sales_utf8.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    return df

df = load_data()

# Add title
st.title("Superstore Sales Analytics")

# (1) Category dropdown
selected_category = st.selectbox(
    "Select Category", 
    df["Category"].unique()
)

# (2) Sub-Category multiselect (within selected category)
available_subcats = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_subcats = st.multiselect(
    "Select Sub-Categories",
    options=available_subcats,
    default=available_subcats
)

# Filter data based on selections
filtered_df = df[
    (df["Category"] == selected_category) &
    (df["Sub_Category"].isin(selected_subcats))
]

# (4) Metrics columns
if not filtered_df.empty:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    
    # (5) Calculate overall profit margin for delta
    overall_total_sales = df["Sales"].sum()
    overall_total_profit = df["Profit"].sum()
    overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0
    margin_delta = profit_margin - overall_profit_margin
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric(
            "Profit Margin (%)", 
            f"{profit_margin:.1f}%", 
            delta=f"{margin_delta:.1f}%"
        )
else:
    st.warning("No data available for selected filters")

# (3) Line chart of sales over time
if not filtered_df.empty:
    st.subheader("Sales Over Time")
    time_series = filtered_df.groupby("Order_Date")["Sales"].sum().reset_index()
    fig = px.line(time_series, x="Order_Date", y="Sales")
    st.plotly_chart(fig)
