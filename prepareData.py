import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
path = 'LabellingManual.csv'
df = pd.read_csv(path, encoding='utf-8', skipinitialspace=True)

# Display the first few rows to ensure the data is loaded correctly
print(df.head())


# Group by the Category column and get the count of each category
category_counts = df['Category'].value_counts()

# Plot the data using matplotlib
plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar')
plt.title('Category Distribution')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()