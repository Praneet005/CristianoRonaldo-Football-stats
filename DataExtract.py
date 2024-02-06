import pandas as pd

# Load the CSV file from the provided link
csv_url = "https://drive.google.com/uc?id=1fq0G48PlMpo1TZCwiSXozgGzrHN3nZN6"
df = pd.read_csv(csv_url)

# Extract Date, Club, Playing_Position, and Type columns
extracted_data = df[['Date', 'Club', 'Playing_Position', 'Type']]

# Display the extracted data
print(extracted_data)
