import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

# 1. SETUP PATHS
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'zomato.csv')

# 2. LOAD DATA
try:
    # Use 'latin-1' encoding as Zomato data often has special characters
    df = pd.read_csv(file_path, encoding='latin-1')
    print("Dataset Loaded Successfully!")
except FileNotFoundError:
    print(f"Error: Could not find 'zomato.csv' at {file_path}")
    sys.exit()

# 3. DATA CLEANING [cite: 102]
# Removing unnecessary columns and handling nulls
df = df.drop(['url', 'address', 'phone', 'menu_item'], axis=1)
df.dropna(inplace=True)

# Cleaning 'rate' (e.g., '4.1/5' -> 4.1)
def clean_rate(value):
    if isinstance(value, str):
        value = value.split('/')[0]
        try:
            return float(value)
        except:
            return None
    return value

df['rate'] = df['rate'].apply(clean_rate)
df.dropna(subset=['rate'], inplace=True)

# 4. ANALYSIS: LOCATION & DEMAND [cite: 104, 105]
# Top 10 locations with highest restaurant count
top_locations = df['location'].value_counts().head(10)

# 5. VISUALIZATION 
plt.figure(figsize=(15, 7))

# Subplot 1: Demand by Location
plt.subplot(1, 2, 1)
sns.barplot(x=top_locations.values, y=top_locations.index, palette='magma')
plt.title('Top 10 High-Demand Locations (Restaurant Count)')
plt.xlabel('Number of Restaurants')

# Subplot 2: Online Order vs. Rating
plt.subplot(1, 2, 2)
sns.boxplot(x='online_order', y='rate', data=df, palette='Set1')
plt.title('Ratings: Online vs. Offline Orders')

plt.tight_layout()
plt.show()

# 6. OPERATIONAL BOTTLENECK ANALYSIS 
# Comparing average cost for two vs rating
plt.figure(figsize=(10, 6))
sns.scatterplot(x='approx_cost(for two people)', y='rate', data=df, alpha=0.3)
plt.title('Cost vs. Rating Performance')
plt.show()