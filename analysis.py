from typing import Dict

import pandas as pd

from metrics import (
    calculate_ad_performance,
    calculate_ad_type_performance,
    calculate_campaign_performance,
    calculate_event_metrics,
    calculate_event_stage_summary,
    calculate_interest_performance,
    calculate_platform_performance,
    calculate_targeting_alignment,
    calculate_targeting_performance,
    calculate_time_performance,
)


def run_analysis(
    full_df: pd.DataFrame,
    campaigns: pd.DataFrame,
) -> Dict[str, pd.DataFrame]:

    analyses = {}

    analyses["event_metrics"] = (
        calculate_event_metrics(full_df)
    )

    analyses["ad_performance"] = (
        calculate_ad_performance(full_df)
    )

    analyses["ad_type_performance"] = (
        calculate_ad_type_performance(full_df)
    )

    analyses["platform_performance"] = (
        calculate_platform_performance(full_df)
    )

    analyses["campaign_performance"] = (
        calculate_campaign_performance(
            full_df,
            campaigns,
        )
    )

    analyses["targeting_alignment"] = (
        calculate_targeting_alignment(full_df)
    )

    analyses["targeting_performance"] = (
        calculate_targeting_performance(full_df)
    )

    analyses["time_performance"] = (
        calculate_time_performance(full_df)
    )

    analyses["interest_performance"] = (
        calculate_interest_performance(full_df)
    )

    analyses["event_stage_summary"] = (
        calculate_event_stage_summary(full_df)
    )

    return analyses


def print_key_findings(
    analyses: Dict[str, pd.DataFrame]
) -> None:

    print("\n")
    print("=" * 70)
    print("KEY PERFORMANCE RESULTS")
    print("=" * 70)

    ad_types = analyses["ad_type_performance"]

    best_ad_type = ad_types.iloc[0]

    print(
        "\nBest ad type by engagement rate:"
    )
    print(
        f"  {best_ad_type['ad_type']}: "
        f"{best_ad_type['engagement_rate']:.2f}%"
    )

    platforms = analyses["platform_performance"]

    best_platform = platforms.iloc[0]

    print(
        "\nBest platform by engagement rate:"
    )
    print(
        f"  {best_platform['ad_platform']}: "
        f"{best_platform['engagement_rate']:.2f}%"
    )

    campaigns = analyses["campaign_performance"]

    best_campaign = campaigns.iloc[0]

    print(
        "\nMost efficient campaign by events per $1,000:"
    )
    print(
        f"  Campaign {int(best_campaign['campaign_id'])}: "
        f"{best_campaign['events_per_1000_dollars']:.2f}"
    )

    targeting = analyses["targeting_performance"]

    matched = targeting[
        targeting["targeting_match"] == True
    ]

    unmatched = targeting[
        targeting["targeting_match"] == False
    ]

    if not matched.empty and not unmatched.empty:

        print(
            "\nTargeting performance:"
        )

        print(
            f"  Matched engagement rate: "
            f"{matched.iloc[0]['engagement_rate']:.2f}%"
        )

        print(
            f"  Unmatched engagement rate: "
            f"{unmatched.iloc[0]['engagement_rate']:.2f}%"
        )