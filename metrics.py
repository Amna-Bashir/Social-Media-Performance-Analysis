from typing import Iterable

import numpy as np
import pandas as pd


def safe_divide(
    numerator: pd.Series,
    denominator: pd.Series
) -> pd.Series:
    """
    Safely divide two pandas Series.

    Returns zero when the denominator is zero.
    """

    return pd.Series(
        np.divide(
            numerator,
            denominator,
            out=np.zeros(len(numerator), dtype=float),
            where=denominator != 0,
        ),
        index=numerator.index,
    )


def calculate_event_metrics(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate overall event performance metrics.
    """

    impressions = (
        dataframe["is_impression"]
        .sum()
    )

    clicks = (
        dataframe["is_click"]
        .sum()
    )

    purchases = (
        dataframe["is_purchase"]
        .sum()
    )

    engagements = (
        dataframe["is_engagement"]
        .sum()
    )

    return pd.DataFrame(
        {
            "metric": [
                "Total Events",
                "Impressions",
                "Engagement Events",
                "Clicks",
                "Purchases",
                "Engagement Rate (%)",
                "Click Rate (%)",
                "Purchase Rate (%)",
            ],
            "value": [
                len(dataframe),
                impressions,
                engagements,
                clicks,
                purchases,
                (
                    engagements / impressions * 100
                    if impressions
                    else 0
                ),
                (
                    clicks / impressions * 100
                    if impressions
                    else 0
                ),
                (
                    purchases / impressions * 100
                    if impressions
                    else 0
                ),
            ],
        }
    )


def calculate_ad_performance(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate performance metrics for each advertisement.
    """

    grouped = dataframe.groupby(
        [
            "ad_id",
            "ad_platform",
            "ad_type",
            "campaign_id",
            "target_gender",
            "target_age_group",
        ]
    )

    result = grouped.agg(
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
    ).reset_index()

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result.sort_values(
        "engagement_rate",
        ascending=False
    )


def calculate_ad_type_performance(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Compare advertisement types using performance metrics.
    """

    result = dataframe.groupby(
        "ad_type"
    ).agg(
        number_of_ads=("ad_id", "nunique"),
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
    ).reset_index()

    result["events_per_ad"] = safe_divide(
        result["total_events"],
        result["number_of_ads"],
    )

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result.sort_values(
        "engagement_rate",
        ascending=False
    )


def calculate_platform_performance(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Compare Facebook and Instagram using rate-based metrics.
    """

    result = dataframe.groupby(
        "ad_platform"
    ).agg(
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
        unique_ads=("ad_id", "nunique"),
    ).reset_index()

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result.sort_values(
        "engagement_rate",
        ascending=False
    )


def calculate_campaign_performance(
    dataframe: pd.DataFrame,
    campaigns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate campaign efficiency using budget and duration.

    Metrics include:
    - Events per day
    - Events per $1,000
    - Engagements per $1,000
    - Engagement rate
    """

    campaign_events = dataframe.groupby(
        "campaign_id"
    ).agg(
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
    ).reset_index()

    result = campaigns.merge(
        campaign_events,
        on="campaign_id",
        how="left",
    )

    metric_columns = [
        "total_events",
        "impressions",
        "engagements",
        "clicks",
        "purchases",
    ]

    result[metric_columns] = (
        result[metric_columns]
        .fillna(0)
    )

    result["events_per_day"] = safe_divide(
        result["total_events"],
        result["duration_days"],
    )

    result["events_per_1000_dollars"] = (
        safe_divide(
            result["total_events"],
            result["total_budget"],
        ) * 1000
    )

    result["engagements_per_1000_dollars"] = (
        safe_divide(
            result["engagements"],
            result["total_budget"],
        ) * 1000
    )

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result.sort_values(
        "events_per_1000_dollars",
        ascending=False
    )


def calculate_targeting_alignment(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Measure how closely interacting users match ad targeting.

    A user is considered fully aligned when their:
    - age group matches,
    - gender matches,
    - interests overlap with the target interests.
    """

    result = dataframe.groupby(
        "ad_platform"
    ).agg(
        total_events=("event_id", "count"),
        age_match_rate=("age_match", "mean"),
        gender_match_rate=("gender_match", "mean"),
        interest_match_rate=("interest_match", "mean"),
        full_targeting_match_rate=(
            "targeting_match",
            "mean",
        ),
    ).reset_index()

    rate_columns = [
        "age_match_rate",
        "gender_match_rate",
        "interest_match_rate",
        "full_targeting_match_rate",
    ]

    for column in rate_columns:
        result[column] *= 100

    return result.sort_values(
        "full_targeting_match_rate",
        ascending=False
    )


def calculate_targeting_performance(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Compare engagement between users who match targeting
    and users who do not.
    """

    result = dataframe.groupby(
        "targeting_match"
    ).agg(
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
    ).reset_index()

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result


def calculate_time_performance(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate engagement metrics by time of day.
    """

    result = dataframe.groupby(
        "time_of_day"
    ).agg(
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
    ).reset_index()

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result.sort_values(
        "engagement_rate",
        ascending=False
    )


def calculate_interest_performance(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate performance metrics for user interest categories.
    """

    interest_df = dataframe[
        [
            "event_id",
            "interests",
            "is_impression",
            "is_engagement",
            "is_click",
            "is_purchase",
        ]
    ].copy()

    interest_df["interest"] = (
        interest_df["interests"]
        .str.split(",")
    )

    interest_df = interest_df.explode(
        "interest"
    )

    interest_df["interest"] = (
        interest_df["interest"]
        .str.strip()
        .str.lower()
    )

    result = interest_df.groupby(
        "interest"
    ).agg(
        total_events=("event_id", "count"),
        impressions=("is_impression", "sum"),
        engagements=("is_engagement", "sum"),
        clicks=("is_click", "sum"),
        purchases=("is_purchase", "sum"),
    ).reset_index()

    result["engagement_rate"] = (
        safe_divide(
            result["engagements"],
            result["impressions"],
        ) * 100
    )

    result["click_rate"] = (
        safe_divide(
            result["clicks"],
            result["impressions"],
        ) * 100
    )

    result["purchase_rate"] = (
        safe_divide(
            result["purchases"],
            result["impressions"],
        ) * 100
    )

    return result.sort_values(
        "engagement_rate",
        ascending=False
    )


def calculate_event_stage_summary(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Summarize event stages relative to impressions.

    This is an event distribution analysis rather than
    a user-level conversion funnel.
    """

    event_types = [
        "Impression",
        "Click",
        "Like",
        "Comment",
        "Share",
        "Purchase",
    ]

    counts = (
        dataframe["event_type"]
        .value_counts()
        .reindex(
            event_types,
            fill_value=0
        )
    )

    impressions = counts["Impression"]

    result = pd.DataFrame(
        {
            "event_type": counts.index,
            "event_count": counts.values,
        }
    )

    result["percent_of_impressions"] = (
        result["event_count"]
        / impressions
        * 100
        if impressions
        else 0
    )

    return result