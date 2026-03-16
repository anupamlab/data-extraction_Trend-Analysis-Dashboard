import requests
import pandas as pd

# Indicators we want to collect
indicators = {
    "GDP": "NY.GDP.MKTP.CD",
    "Population": "SP.POP.TOTL",
    "Inflation": "FP.CPI.TOTL.ZG",
    "Unemployment": "SL.UEM.TOTL.ZS"
}

# Empty list to store all data
all_data = []


# Loop through each indicator
# ---------------------------------------
for indicator_name, indicator_code in indicators.items():

    # Build API URL
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}?format=json&per_page=20000"

    # Send request
    response = requests.get(url)

    # Convert response to JSON
    data = response.json()

    # Actual records are in index [1]
    records = data[1]

    # Extract useful fields
    for item in records:

        country = item["country"]["value"]
        year = item["date"]
        value = item["value"]

        # Ignore missing values
        if value is not None:

            all_data.append([
                country,
                year,
                indicator_name,
                value
            ])

# Convert to dataframe
# ---------------------------------------
df = pd.DataFrame(all_data, columns=[
    "Country",
    "Year",
    "Indicator",
    "Value"
])

# Save dataset
# ---------------------------------------
df.to_csv("world_economic_data.csv", index=False)

print("Dataset created successfully")
print("Total rows:", len(df))