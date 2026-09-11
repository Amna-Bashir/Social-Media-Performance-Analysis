from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def _save_plot(
    output_directory: Path,
    filename: str,
) -> None:
    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    plt.tight_layout()

    plt.savefig(
        output_directory / filename,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def plot_ad_type_performance(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=dataframe,
        x="ad_type",
        y="engagement_rate",
    )

    plt.title(
        "Engagement Rate by Advertisement Type"
    )
    plt.xlabel("Advertisement Type")
    plt.ylabel("Engagement Rate (%)")

    _save_plot(
        output_directory,
        "ad_type_engagement_rate.png",
    )


def plot_platform_performance(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    plot_df = dataframe.melt(
        id_vars="ad_platform",
        value_vars=[
            "engagement_rate",
            "click_rate",
            "purchase_rate",
        ],
        var_name="metric",
        value_name="rate",
    )

    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=plot_df,
        x="ad_platform",
        y="rate",
        hue="metric",
    )

    plt.title(
        "Performance Rates by Advertising Platform"
    )
    plt.xlabel("Platform")
    plt.ylabel("Rate (%)")

    _save_plot(
        output_directory,
        "platform_performance.png",
    )


def plot_campaign_efficiency(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    top_campaigns = (
        dataframe
        .sort_values(
            "events_per_1000_dollars",
            ascending=False,
        )
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=top_campaigns,
        x="events_per_1000_dollars",
        y="name",
    )

    plt.title(
        "Top 10 Campaigns by Event Efficiency"
    )
    plt.xlabel("Events per $1,000")
    plt.ylabel("Campaign")

    _save_plot(
        output_directory,
        "campaign_efficiency.png",
    )


def plot_top_ads(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    top_ads = dataframe.head(10).copy()

    top_ads["ad_id"] = (
        "Ad " + top_ads["ad_id"].astype(str)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=top_ads,
        x="engagement_rate",
        y="ad_id",
        hue="ad_platform",
    )

    plt.title(
        "Top 10 Advertisements by Engagement Rate"
    )
    plt.xlabel("Engagement Rate (%)")
    plt.ylabel("Advertisement")

    _save_plot(
        output_directory,
        "top_ad_performance.png",
    )


def plot_targeting_alignment(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    plot_df = dataframe.melt(
        id_vars="ad_platform",
        value_vars=[
            "age_match_rate",
            "gender_match_rate",
            "interest_match_rate",
            "full_targeting_match_rate",
        ],
        var_name="match_type",
        value_name="rate",
    )

    plt.figure(figsize=(11, 6))

    sns.barplot(
        data=plot_df,
        x="ad_platform",
        y="rate",
        hue="match_type",
    )

    plt.title(
        "Audience Targeting Alignment"
    )
    plt.xlabel("Platform")
    plt.ylabel("Match Rate (%)")

    _save_plot(
        output_directory,
        "targeting_alignment.png",
    )


def plot_time_performance(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    plt.figure(figsize=(9, 5))

    sns.barplot(
        data=dataframe,
        x="time_of_day",
        y="engagement_rate",
    )

    plt.title(
        "Engagement Rate by Time of Day"
    )
    plt.xlabel("Time of Day")
    plt.ylabel("Engagement Rate (%)")

    _save_plot(
        output_directory,
        "time_engagement_rate.png",
    )


def plot_interest_performance(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    top_interests = dataframe.head(10)

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=top_interests,
        x="engagement_rate",
        y="interest",
    )

    plt.title(
        "Top Interests by Engagement Rate"
    )
    plt.xlabel("Engagement Rate (%)")
    plt.ylabel("Interest")

    _save_plot(
        output_directory,
        "interest_performance.png",
    )


def plot_event_stages(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> None:
    plt.figure(figsize=(10, 5))

    sns.barplot(
        data=dataframe,
        x="event_type",
        y="percent_of_impressions",
    )

    plt.title(
        "Event Types Relative to Impressions"
    )
    plt.xlabel("Event Type")
    plt.ylabel("Events per 100 Impressions")

    _save_plot(
        output_directory,
        "event_stage_distribution.png",
    )


def create_all_visualizations(
    analyses: Dict[str, pd.DataFrame],
    output_directory: str = "outputs",
) -> None:
    output_path = Path(output_directory)

    plot_ad_type_performance(
        analyses["ad_type_performance"],
        output_path,
    )

    plot_platform_performance(
        analyses["platform_performance"],
        output_path,
    )

    plot_campaign_efficiency(
        analyses["campaign_performance"],
        output_path,
    )

    plot_top_ads(
        analyses["ad_performance"],
        output_path,
    )

    plot_targeting_alignment(
        analyses["targeting_alignment"],
        output_path,
    )

    plot_time_performance(
        analyses["time_performance"],
        output_path,
    )

    plot_interest_performance(
        analyses["interest_performance"],
        output_path,
    )

    plot_event_stages(
        analyses["event_stage_summary"],
        output_path,
    )