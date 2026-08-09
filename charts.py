import pandas as pd
import matplotlib.pyplot as plt

# Load churn analysis file
df = pd.read_csv("output/playlist_churn_analysis.csv")

# Check data
print(df.head())
print(df.columns)
print(df.head(10))

# Create figure
plt.figure(figsize=(12,5))

# Plot churn rate
plt.plot(
    df["date"],
    df["churn_rate"]
)

# Labels and title
plt.xlabel("Date")
plt.ylabel("Churn Rate (%)")
plt.title("Playlist Churn Rate Over Time")

# Show limited date labels
plt.xticks(
    ticks=range(0, len(df), 30),
    labels=df["date"][::30],
    rotation=45
)

# Ignore extreme spikes for better visualization
plt.ylim(0,50)

# Adjust layout
plt.tight_layout()

# Display graph
plt.show()
plt.tight_layout()
plt.show()


# ==========================================
# Chart 2 : Entry vs Exit Flow Chart
# ==========================================

plt.figure(figsize=(12,5))

plt.plot(
    df["date"],
    df["entries"],
    label="Entries"
)

plt.plot(
    df["date"],
    df["exits"],
    label="Exits"
)

plt.xlabel("Date")
plt.ylabel("Number of Songs")
plt.title("Daily Playlist Entry vs Exit")

plt.xticks(
    ticks=range(0, len(df), 30),
    labels=df["date"][::30],
    rotation=45
)

plt.legend()

plt.tight_layout()

plt.show()