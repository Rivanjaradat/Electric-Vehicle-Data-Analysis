# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z2TOb9U-keHj0BJMUnt4czJuH5L3SVlj

Load a CSV file  into a DataFrame:
"""

import pandas as pd
# read the dataset using pandas
df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
#print first 5 line
df.head()

"""# Data Cleaning and Feature Engineering:

1. Document Missing Values: Check for missing values and document their frequency and
distribution across features.

To display the content of the data and type of features use the info() method in pandas. This method provides a concise summary of the DataFrame's structure, including column names, data types, and the count of non-null values.
"""

#Displaying Data Information and Checking NAN
df.info()

df.isnull().sum()

print(df.isnull().any(axis=1).sum())
print(100*df.isnull().any(axis=1).sum()/df.shape[0],'%')

"""# Handling Missing Data Through Dropping"""

# Record DataFrame shape before and after dropping rows
initial_shape = df.shape
df.dropna(inplace=True)
final_shape = df.shape

print("Initial shape:", initial_shape)
print("Final shape after dropping rows with missing values:", final_shape)

# Check impact on statistics
print(df.describe())

"""# Handling Missing Data Through Imputation"""

import pandas as pd
from sklearn.impute import SimpleImputer

# Load your dataset
data = pd.read_csv('Electric_Vehicle_Population_Data.csv')

# Check for missing values
print("Missing values before imputation:\n", data.isnull().sum())

# Define the column names
mean_columns = ['County', 'City', 'Postal Code', 'Electric Range', 'Base MSRP',
                'Legislative District', 'DOL Vehicle ID', 'Electric Utility', '2020 Census Tract']

# Loop through each column for mean imputation
for column in mean_columns:
    if column in data.columns:
        # Check if the column is numeric
        if pd.api.types.is_numeric_dtype(data[column]):
            # Mean Imputation
            mean_imputer = SimpleImputer(strategy='mean')
            data[column] = mean_imputer.fit_transform(data[[column]])
        else:
            print(f"Column '{column}' is not numeric and cannot be imputed with mean.")
    else:
        print(f"Column '{column}' does not exist in the DataFrame.")

# Check for missing values after imputation
print("Missing values after imputation:\n", data.isnull().sum())

# Display the updated dataframe
print(data.head())

"""# Feature Encoding

### encode the Electric Vehicle Type feature.
"""

# Import the necessary library for one-hot encoding
from sklearn.preprocessing import OneHotEncoder

# Create an instance of the OneHotEncoder with 'handle_unknown' set to 'ignore'
enc = OneHotEncoder(handle_unknown='ignore')

# Fit the encoder on the 'Electric Vehicle Type' column of the DataFrame
enc.fit(df[['Electric Vehicle Type']])

# Transform the 'Electric Vehicle Type' column into a one-hot encoded array and convert it to a dense array
df_Type = enc.transform(df[['Electric Vehicle Type']]).toarray()

# Create a copy of the original DataFrame to store the one-hot encoded data
df_ohenc = df.copy()

# Add the one-hot encoded columns to the new DataFrame using the encoder's categories
df_ohenc[enc.categories_[0]] = df_Type

# Display the first few rows of the new DataFrame
df_ohenc.head()

"""### encode the State feature."""

# Import the necessary library for one-hot encoding
from sklearn.preprocessing import OneHotEncoder

# Create an instance of the OneHotEncoder with 'handle_unknown' set to 'ignore'
enc = OneHotEncoder(handle_unknown='ignore')

# Fit the encoder on the 'State' column of the DataFrame
enc.fit(df[['State']])

# Transform the 'State' column into a one-hot encoded array and convert it to a dense array
df_Type = enc.transform(df[['State']]).toarray()

# Create a copy of the original DataFrame to store the one-hot encoded data
df_ohenc = df.copy()

# Add the one-hot encoded columns to the new DataFrame using the encoder's categories
df_ohenc[enc.categories_[0]] = df_Type

# Display the first few rows of the new DataFrame
df_ohenc.head()

"""
## Normalization"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler




numeric_features = df.select_dtypes(include=['float64', 'int64']).columns


scaler = MinMaxScaler()


df[numeric_features] = scaler.fit_transform(df[numeric_features])


print(df.head())

"""#Exploratory Data Analysis

5. Descriptive Statistics: Calculate summary statistics (mean, median, standard deviation) for
numerical features

* Central Tendency (Mean, Median)


Calculating the mean, median, and mode for each numerical feature provides insights into the central tendency, helping understand where the data is centered.
"""

# Calculating mean, median, and mode
mean_values = df.mean(numeric_only=True)
median_values = df.median(numeric_only=True)


print("Mean values:\n", mean_values)
print("\nMedian values:\n", median_values)

"""* Variation (Variance and Standard Deviation)

Variance and standard deviation measure the spread of data. Higher values indicate more variability, while lower values suggest data points are closer to the mean.
"""

# Calculating variance and standard deviation
variance_values = df.var(numeric_only=True)
std_dev_values = df.std(numeric_only=True)

print("\nVariance values:\n", variance_values)
print("\nStandard deviation values:\n", std_dev_values)

"""* Visualization of Distribution for Descriptive Statistics"""

import seaborn as sns
import matplotlib.pyplot as plt

# Plot histograms for specific numerical columns with mean, median, and standard deviation
fig, axs = plt.subplots(figsize=(18, 5), ncols=3, nrows=2)

# Select the first 6 numerical columns for visualization (adjust as necessary)
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns[:6]

for i, col in enumerate(numerical_columns):
    sns.histplot(data=df, x=col, ax=axs[i//3, i%3], kde=True)
    axs[i//3, i%3].set_title(
        f"{col}:\nMean = {mean_values[col]:.2f}, Median = {median_values[col]:.2f}, Std Dev = {std_dev_values[col]:.2f}"
    )
    axs[i//3, i%3].set_xlim(df[col].min(), df[col].max())

plt.tight_layout()
plt.show()

"""----

6. Spatial Distribution: Visualize the spatial distribution of EVs across locations (e.g., maps).

In this section, we will visualize the spatial distribution of electric vehicles (EVs) registered across Washington State. Using Folium, we create an interactive map with clustered markers representing different vehicle brands, color-coded for easy identification.

* Import Libraries and Prepare Data

We start by importing necessary libraries and preparing the data. We convert the 'Location' column to string format, then extract longitude and latitude coordinates. Rows with missing coordinates are removed to ensure accuracy.
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Convert the 'Vehicle Location' column to string format
df['Location'] = df['Vehicle Location'].astype(str)

# Function to extract coordinates
def get_coordinates(location_str):
    try:
        longitude, latitude = location_str.split('(')[1].replace(')', '').split()
        return float(longitude), float(latitude)
    except:
        return None, None

# Apply the function to create 'Longitude' and 'Latitude' columns
df['Longitude'], df['Latitude'] = zip(*df['Location'].apply(get_coordinates))

# Remove rows with missing coordinates
df_with_coords = df.dropna(subset=['Longitude', 'Latitude'])

"""* Sample Data and Define Color Mapping

To keep the map responsive, we sample 1,000 entries. We then define a color mapping for popular EV brands to differentiate them visually on the map.
"""

# Sample 1,000 entries to enhance map responsiveness
sampled_data = df_with_coords.sample(n=1000, random_state=42)

# Define color mapping for EV brands
brand_colors = {
    'Tesla': 'purple',
    'Nissan': 'blue',
    'Chevrolet': 'green',
    'BMW': 'red',
    'Audi': 'orange',
    'Other': 'gray'
}

"""* Create and Configure Map

We create a Folium map centered around Washington State. A cluster layer is added to handle dense areas and avoid clutter. Each EV is represented by a color-coded marker based on its brand.

"""

# Center map on Washington State
washington_center = [47.7511, -120.7401]  # Washington State coordinates
ev_distribution_map = folium.Map(location=washington_center, zoom_start=7)

# Add cluster layer
cluster_group = MarkerCluster().add_to(ev_distribution_map)

# Add color-coded markers for each EV, based on brand
for _, row in sampled_data.iterrows():
    brand = row['Make']
    # Use the brand color, defaulting to gray if the brand is not in the color mapping
    marker_color = brand_colors.get(brand, 'gray')

    # Add marker with popup info and color-coded icon
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=f"{row['Make']} {row['Model']} ({row['Model Year']})",
        icon=folium.Icon(color=marker_color)
    ).add_to(cluster_group)

"""* Display the Map

Below is the interactive map showing the distribution of EVs across Washington State. Each cluster represents an area with high EV registrations, and each marker is color-coded by brand.

"""

# Display the interactive map
ev_distribution_map
# Display the interactive map
ev_distribution_map

"""----

**7- Model Popularity:**
"""

#Code for Counting Model Frequency
model_counts = df['Model'].value_counts()


print("Frequency of each model:")
print(model_counts)

#Code for Plotting Model Popularity
import matplotlib.pyplot as plt


top_models = model_counts.head(10)


plt.figure(figsize=(10, 6))
top_models.plot(kind='bar', color='skyblue')
plt.title("Top EV Models by Frequency")
plt.xlabel("Model")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()

"""### 8-Investigate the relationship between every pair of numeric features"""

import pandas as pd
import numpy as np
# Select only numeric columns
df_numeric = df.select_dtypes(include=[np.number])

# Calculate the Pearson correlation matrix
corr = df_numeric.corr(method='pearson')

# Display the correlation matrix
print(corr)

"""Visualize Correlations with a Heatmap"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, vmin=-1, vmax=1)
plt.title('Correlation Heatmap of Numeric Features')
plt.show()

"""# Visualization:

9. Data Exploration Visualizations: Create various visualizations (e.g., histograms, scatter
plots, boxplots) to explore the relationships between features.
"""

import matplotlib.pyplot as plt
import seaborn as sns

"""

*   Histograms for Numerical Features


"""

# Plotting histograms for each numerical feature
df.hist(bins=20, figsize=(15,10))
plt.suptitle('Histograms of Numerical Features')
plt.show()

"""

---




*   Scatter Plot Matrix




"""

# Creating scatter plot matrix for numerical features
sns.pairplot(df.select_dtypes(include=['float64', 'int64']))
plt.suptitle('Scatter Plot Matrix of Numerical Features')
plt.show()

"""---
*  Box Plot to Identify Outliers
"""

# Boxplot for each numerical feature
plt.figure(figsize=(10, 6))
sns.boxplot(data=df.select_dtypes(include=['float64', 'int64']))
plt.xticks(rotation=90)
plt.title('Box Plot of Numerical Features')
plt.show()

"""10. Comparative Visualization: Compare the distribution of EVs across different locations
(cities, counties) using bar charts or stacked bar charts.

*  Bar Chart for Top 10 Cities by Number of EV Registrations
"""

# Top 10 cities with highest EV registrations
plt.figure(figsize=(15, 6))
df['City'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Cities with Highest EV Registrations')
plt.xlabel('City')
plt.ylabel('Number of EVs')
plt.show()

"""* Stacked Barfor Top 10 Counties by Number of EV Registrations

"""

# Get the top 10 counties by total EV count
top_counties = df['County'].value_counts().head(10).index
ev_by_top_counties = df[df['County'].isin(top_counties)].groupby(['County', 'Electric Vehicle Type']).size().unstack()

# Plot the stacked bar chart for only the top counties
ev_by_top_counties.plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Distribution of EV Types Across Top 10 Counties')
plt.xlabel('County')
plt.ylabel('Number of EVs')
plt.legend(title='EV Type')
plt.xticks(rotation=45)  # Rotate labels slightly for readability
plt.show()

"""# Additional Analysis:

11. Temporal Analysis (Optional): If the dataset includes data across multiple time points,
analyze the temporal trends in EV adoption rates and model popularity.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Temporal Analysis of EV Adoption Over Time
# Check if 'Model Year' column exists in the dataset
if 'Model Year' in df.columns:
    # Count the number of EVs by 'Model Year', sorted for trend analysis
    ev_by_year = df['Model Year'].value_counts().sort_index()

    # Plot the EV adoption trend over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=ev_by_year.index, y=ev_by_year.values, marker='o', color='dodgerblue')
    plt.title('EV Adoption Trend Over Time')
    plt.xlabel('Model Year')
    plt.ylabel('Number of EVs')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Step 2: Temporal Analysis of Top Model Popularity Over Time
    # Check if 'Model' column exists in the dataset
    if 'Model' in df.columns:
        # Group by 'Model Year' and 'Model' to analyze model popularity over time
        model_popularity = df.groupby(['Model Year', 'Model']).size().unstack(fill_value=0)

        # Identify the top 5 most popular models across all years
        top_models = model_popularity.sum().nlargest(5).index
        model_popularity_top = model_popularity[top_models]

        # Plot the popularity trend of the top 5 models over time
        plt.figure(figsize=(12, 6))
        for model in top_models:
            sns.lineplot(data=model_popularity_top[model], marker='o', label=model)

        plt.title('Top 5 EV Model Popularity Over Time')
        plt.xlabel('Model Year')
        plt.ylabel('Number of EVs')
        plt.legend(title='Model')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("The 'Model' column is not available for analyzing model popularity trends.")
else:
    print("The 'Model Year' column is not available for temporal analysis.")