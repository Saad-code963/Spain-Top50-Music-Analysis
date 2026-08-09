import pandas as pd
import os


# ==============================
# LOAD DATA
# ==============================

def load_data():

    df = pd.read_csv("data/Atlantic_Spain.csv")

    return df



# ==============================
# MAIN ANALYSIS
# ==============================

if __name__ == "__main__":


    # Load Dataset
    df = load_data()


    # ==============================
    # DATA CLEANING
    # ==============================

    clean_df = df.drop_duplicates(
        subset=["date", "position"]
    ).copy()


    clean_df["date"] = pd.to_datetime(
        clean_df["date"],
        format="%d-%m-%Y"
    )


    os.makedirs("output", exist_ok=True)


    clean_df.to_csv(
        "output/clean_spain_top50.csv",
        index=False
    )


    print("Data Cleaning Completed")



    # ==============================
    # SONG LIFECYCLE ANALYSIS
    # ==============================


    song_group = clean_df.groupby(
        ["song", "artist"]
    )


    entry_date = song_group["date"].min()

    exit_date = song_group["date"].max()


    total_days = song_group["date"].nunique()


    peak_position = song_group["position"].min()



    # Find peak date

    peak_rows = clean_df.loc[
        clean_df.groupby(
            ["song","artist"]
        )["position"].idxmin()
    ]


    peak_rows["time_to_peak"] = (
        peak_rows["date"].values -
        entry_date.values
    ) / pd.Timedelta(days=1)



    lifecycle_df = pd.DataFrame({

        "entry_date": entry_date,

        "exit_date": exit_date,

        "total_days": total_days,

        "peak_position": peak_position

    })


    lifecycle_df["time_to_peak"] = (
        peak_rows["time_to_peak"].values
    )



    # ==============================
    # LIFECYCLE STAGE
    # ==============================


    lifecycle_df["stage"] = "Other"


    lifecycle_df.loc[
        lifecycle_df["total_days"] <= 7,
        "stage"
    ] = "New Entry"



    lifecycle_df.loc[
        lifecycle_df["peak_position"] <= 10,
        "stage"
    ] = "Peak Phase"



    lifecycle_df.loc[
        lifecycle_df["time_to_peak"] > 0,
        "stage"
    ] = "Growth Phase"



    lifecycle_df.loc[
        (lifecycle_df["peak_position"] > 10)
        &
        (lifecycle_df["peak_position"] <= 30),
        "stage"
    ] = "Mature Phase"



    # Save lifecycle

    lifecycle_df.to_csv(
        "output/song_lifecycle.csv"
    )


    print("Lifecycle Analysis Completed")



    # ==============================
    # PLAYLIST ROTATION / CHURN
    # ==============================


    daily_entries = (
        entry_date
        .value_counts()
        .sort_index()
    )


    daily_exits = (
        exit_date
        .value_counts()
        .sort_index()
    )



    churn_df = pd.DataFrame({

        "entries": daily_entries,

        "exits": daily_exits

    }).fillna(0)



    churn_df["churn_rate"] = (

        (churn_df["entries"] + churn_df["exits"])
        / 50

    ) * 100



    churn_df["playlist_status"] = "Stable"



    churn_df.loc[
        churn_df["churn_rate"] > 5,
        "playlist_status"
    ] = "Moderate"



    churn_df.loc[
        churn_df["churn_rate"] > 10,
        "playlist_status"
    ] = "Volatile"



    churn_df.to_csv(
        "output/playlist_churn_analysis.csv"
    )


    print("Playlist Rotation Analysis Completed")



    # ==============================
    # CONTENT MATURITY ANALYSIS
    # ==============================


    print("\nCONTENT MATURITY ANALYSIS")


    print(
        lifecycle_df["total_days"].describe()
    )


    # Percentile calculation

    p25 = lifecycle_df["total_days"].quantile(0.25)

    p50 = lifecycle_df["total_days"].quantile(0.50)

    p75 = lifecycle_df["total_days"].quantile(0.75)



    def maturity_stage(days):

        if days <= p25:

            return "Fresh Release"


        elif days <= p50:

            return "Growing"


        elif days <= p75:

            return "Mature Hit"


        else:

            return "Evergreen"



    lifecycle_df["content_maturity"] = (
        lifecycle_df["total_days"]
        .apply(maturity_stage)
    )



    print(
        lifecycle_df["content_maturity"]
        .value_counts()
    )



    # Final save with maturity

    lifecycle_df.to_csv(
        "output/song_lifecycle.csv"
    )


    print("\nFINAL ANALYSIS COMPLETED SUCCESSFULLY")

    