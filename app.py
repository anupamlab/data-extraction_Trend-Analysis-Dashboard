# -------------------------------------------------
# Import required libraries
# -------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# Dashboard Title
# -------------------------------------------------
st.title("Global Economic Data Dashboard")
st.caption("Economic trend analysis using World Bank dataset")

# -------------------------------------------------
# Load dataset
# -------------------------------------------------
data = pd.read_csv("world_economic_data.csv")

# Convert columns to numeric format
data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
data["Value"] = pd.to_numeric(data["Value"], errors="coerce")

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------
st.subheader("Dataset Preview")
st.write(data)

# Show total records
st.metric("Total Records", len(data))

# -------------------------------------------------
# Country Selection (with ALL option)
# -------------------------------------------------
st.subheader("Select Country")

countries = sorted(data["Country"].dropna().unique())

# Add ALL option
countries.insert(0, "ALL")

selected_country = st.selectbox(
    "Choose a country",
    countries
)

# -------------------------------------------------
# Indicator Selection
# -------------------------------------------------
st.subheader("Select Indicator")

indicators = data["Indicator"].dropna().unique()

selected_indicator = st.selectbox(
    "Choose indicator",
    indicators
)

# -------------------------------------------------
# Year Filter
# -------------------------------------------------
st.subheader("Select Year Range")

year_range = st.slider(
    "Choose year range",
    int(data["Year"].min()),
    int(data["Year"].max()),
    (2000, 2023)
)

# -------------------------------------------------
# Data Filtering
# -------------------------------------------------

# If ALL countries selected
if selected_country == "ALL":

    filtered_data = data[
        (data["Indicator"] == selected_indicator) &
        (data["Year"] >= year_range[0]) &
        (data["Year"] <= year_range[1])
    ]

# If specific country selected
else:

    filtered_data = data[
        (data["Country"] == selected_country) &
        (data["Indicator"] == selected_indicator) &
        (data["Year"] >= year_range[0]) &
        (data["Year"] <= year_range[1])
    ]

# Sort data by year
filtered_data = filtered_data.sort_values("Year")

# -------------------------------------------------
# Show Filtered Data
# -------------------------------------------------
st.subheader("Filtered Data")

st.write(filtered_data)

# -------------------------------------------------
# Trend Analysis Chart
# -------------------------------------------------
st.subheader("Trend Analysis")

fig, ax = plt.subplots()

# If ALL countries selected
if selected_country == "ALL":

    trend_data = filtered_data.groupby("Year")["Value"].mean()

    ax.plot(trend_data.index, trend_data.values)

    ax.set_title(f"Global Average {selected_indicator} Trend")

# If single country selected
else:

    ax.plot(filtered_data["Year"], filtered_data["Value"])

    ax.set_title(f"{selected_indicator} Trend for {selected_country}")

ax.set_xlabel("Year")
ax.set_ylabel(selected_indicator)

st.pyplot(fig)

# -------------------------------------------------
# Top Countries Analysis (Based on Year Filter)
# -------------------------------------------------
st.subheader("Top Countries Analysis")

# Use the last year from the slider
selected_year = year_range[1]

st.write("Latest Selected Year:", selected_year)

# Filter data for selected indicator and selected year
year_data = data[
    (data["Indicator"] == selected_indicator) &
    (data["Year"] == selected_year)
]

# Remove missing values
year_data = year_data.dropna(subset=["Value"])

# Check if data exists
if len(year_data) > 0:

    # Sort countries by value
    top_countries = year_data.sort_values(
        by="Value",
        ascending=False
    ).head(10)

    # Display result
    st.write(top_countries[["Country", "Value"]])

else:
    st.warning("No data available for this year.")