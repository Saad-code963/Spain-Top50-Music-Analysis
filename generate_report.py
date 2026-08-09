import pandas as pd


# Load data

lifecycle = pd.read_csv(
    "output/song_lifecycle.csv"
)

churn = pd.read_csv(
    "output/playlist_churn_analysis.csv"
)


# Calculate research insights

average_lifetime = round(
    lifecycle["total_days"].mean(),
    2
)


evergreen_count = lifecycle[
    lifecycle["content_maturity"] == "Evergreen"
].shape[0]


top_songs = (
    lifecycle
    .sort_values(
        by="total_days",
        ascending=False
    )
    .head(10)
)


average_churn = round(
    churn["churn_rate"].mean(),
    2
)


# Create report

report = f"""
CONTENT MATURITY, RELEASE LIFECYCLE
AND PLAYLIST ROTATION ANALYSIS
===================================


RESEARCH SUMMARY
----------------

Average Song Lifetime:
{average_lifetime} days


Evergreen Songs Count:
{evergreen_count}


Average Playlist Churn Rate:
{average_churn}%



TOP 10 LONGEST RUNNING SONGS
----------------------------

{top_songs[["song", "artist", "total_days"]].to_string(index=False)}



CONCLUSION
----------

This research analyzes the lifecycle behavior
of Spain Top 50 songs.

Songs with longer chart presence show stronger
audience retention and long-term popularity.

Playlist rotation analysis helps understand
how frequently songs enter and leave the chart.

The study identifies temporary trending songs
and evergreen songs that maintain popularity
for a longer period.

"""


# Save report

with open(
    "output/research_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(report)


print(
    "Research Report Generated Successfully"
)