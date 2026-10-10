import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("/Users/mosaddekamallick/Downloads/Cars93_missing.csv")

# ==============================================================================
# Task 1: Read CSV file and transfer it into DataFrame
# ==============================================================================
print("=" * 60)
print("TASK 1: Read CSV file and transfer it into DataFrame")
print("=" * 60)
print(f"Loaded DataFrame shape: {df.shape}")
print(df.head(3))

# ==============================================================================
# Task 2: Transfer object Series into index column of the dataframe
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 2: Transfer object Series into index column of the dataframe")
print("=" * 60)

df_indexed = df.set_index("Make")
print("New Index preview:")
print(df_indexed.index[:5])

# ==============================================================================
# Task 3: Change the data in the column of DataFrame according to some condition
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 3: Change the data in the column of DataFrame according to some condition")
print("=" * 60)

df_cond = df.copy()
df_cond.loc[df_cond["Price"] > 30, "Price"] = df_cond["Price"] * 0.90
print("Sample rows where Price was > 30 (now updated with 10% discount):")
print(df_cond.loc[df["Price"] > 30, ["Model", "Price"]].head(4))


# ==============================================================================
# Task 4: Get names of the DataFrame columns and sum of losted values DF
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 4: Get names of the DataFrame columns and sum of losted values DF")
print("=" * 60)
col_names = df.columns.tolist()
missing_by_col = df.isnull().sum()
total_lost = df.isnull().sum().sum()

print("Column Names:")
print(col_names)
print("\nMissing values per column:")
print(missing_by_col)
print(f"\nTotal lost/missing values in entire DataFrame: {total_lost}")


# ==============================================================================
# Task 5: Ex-change 2 columns, use function for it. Sort coulumn by name
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 5: Ex-change 2 columns, use function for it. Sort coulumn by name")
print("=" * 60)


def exchange_columns(data, col1, col2):
    """Swap positions of two columns in a DataFrame."""
    cols = list(data.columns)
    idx1, idx2 = cols.index(col1), cols.index(col2)
    cols[idx1], cols[idx2] = cols[idx2], cols[idx1]
    return data[cols]


# Exchange 'Manufacturer' and 'Model'
df_swapped = exchange_columns(df, "Manufacturer", "Model")
print("First 4 columns after swapping 'Manufacturer' and 'Model':")
print(df_swapped.columns[:4].tolist())

# Sort DataFrame columns alphabetically by name
df_sorted_cols = df.sort_index(axis=1)
print("\nColumns sorted alphabetically by name:")
print(df_sorted_cols.columns.tolist())


# ==============================================================================
# Task 6: Delete upper and lowe 5% in object DataFrame
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 6: Delete upper and lowe 5% in object DataFrame")
print("=" * 60)
# Trim outer 5% tails based on numeric 'Price'
lower_5 = df["Price"].quantile(0.05)
upper_5 = df["Price"].quantile(0.95)

df_trimmed = df[(df["Price"] >= lower_5) & (df["Price"] <= upper_5)]
print(f"5th percentile cutoff:  {lower_5:.2f}")
print(f"95th percentile cutoff: {upper_5:.2f}")
print(f"Rows before trimming: {len(df)} | Rows after trimming: {len(df_trimmed)}")

# ==============================================================================
# Task 7: Replay ( Apply) missed values in the Column with average values.
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 7: Replay ( Apply) missed values in the Column with average values.")
print("=" * 60)
df_imputed = df.copy()
mean_price = df_imputed["Price"].mean()
df_imputed["Price"] = df_imputed["Price"].fillna(mean_price)

print(f"Mean 'Price': {mean_price:.2f}")
print(
    f"Missing values remaining in 'Price': {df_imputed['Price'].isnull().sum()}"
)

# ==============================================================================
# Task 8: Create two data frames using the two Dicts, Merge two data frames, and append the second data frame as a new column to the first data frame.
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 8: Create two data frames using the two Dicts, Merge two data frames, and append the second data frame as a new column to the first data frame.")
print("=" * 60)
dict1 = {
    "CarID": [101, 102, 103],
    "Owner": ["Alice", "Bob", "Charlie"],
}
dict2 = {
    "CarID": [101, 102, 103],
    "City": ["Dortmund", "Berlin", "Munich"],
}

df1 = pd.DataFrame(dict1)
df2 = pd.DataFrame(dict2)

merged_df = pd.merge(df1, df2, on="CarID")
print("Merged DataFrame:")
print(merged_df)

df1["City"] = df2["City"]
print("\nFirst DataFrame with second DataFrame appended as a new column:")
print(df1)

# ==============================================================================
# Task 9: For any column create histogram
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 9: For any column create histogram")
print("=" * 60)
plt.figure(figsize=(7, 4.5))
plt.hist(df["Price"].dropna(), bins=15, color="#5dade2", edgecolor="black")
plt.title("Histogram of Car Prices (Cars93)")
plt.xlabel("Price ($1000s)")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# ==============================================================================
# Task 10: Create Correlation Matrix for any column
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 10: Create Correlation Matrix for any column")
print("=" * 60)
cols_for_corr = ["Price", "EngineSize", "Horsepower", "MPG.city", "Weight"]
corr_matrix = df[cols_for_corr].corr()
print("Correlation Matrix:")
print(corr_matrix)

plt.figure(figsize=(6, 5))
sns.heatmap(
    corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1
)
plt.title("Correlation Matrix Heatmap")
plt.tight_layout()
plt.show()
