from typing import Dict

import pandas as pd


class DataValidationError(Exception):
    """Raised when dataset validation fails."""


def clean_datasets(
    datasets: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:
    cleaned = {}

    for name, dataframe in datasets.items():

        df = dataframe.copy()

        df = df.drop_duplicates()

        string_columns = df.select_dtypes(
            include=["object"]
        ).columns

        for column in string_columns:
            df[column] = df[column].apply(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

        cleaned[name] = df

    cleaned["ad_events"]["timestamp"] = pd.to_datetime(
        cleaned["ad_events"]["timestamp"],
        errors="coerce"
    )

    cleaned["campaigns"]["start_date"] = pd.to_datetime(
        cleaned["campaigns"]["start_date"],
        errors="coerce"
    )

    cleaned["campaigns"]["end_date"] = pd.to_datetime(
        cleaned["campaigns"]["end_date"],
        errors="coerce"
    )

    validate_cleaned_data(cleaned)

    return cleaned


def validate_cleaned_data(
    datasets: Dict[str, pd.DataFrame]
) -> None:
    if datasets["ad_events"]["timestamp"].isna().any():
        raise DataValidationError(
            "Invalid timestamps found in ad_events."
        )

    if datasets["campaigns"][
        ["start_date", "end_date"]
    ].isna().any().any():
        raise DataValidationError(
            "Invalid campaign dates found."
        )

    for name, dataframe in datasets.items():

        if dataframe.empty:
            raise DataValidationError(
                f"{name} contains no rows after cleaning."
            )


def build_combined_dataset(
    datasets: Dict[str, pd.DataFrame]
) -> pd.DataFrame:

    ads = datasets["ads"]
    events = datasets["ad_events"]
    campaigns = datasets["campaigns"]
    users = datasets["users"]

    events_with_ads = events.merge(
        ads,
        on="ad_id",
        how="left",
        validate="many_to_one"
    )

    events_with_campaigns = events_with_ads.merge(
        campaigns,
        on="campaign_id",
        how="left",
        validate="many_to_one"
    )

    full_df = events_with_campaigns.merge(
        users,
        on="user_id",
        how="left",
        validate="many_to_one"
    )

    required_columns = [
        "ad_platform",
        "ad_type",
        "campaign_id",
        "user_id",
        "event_type",
        "target_age_group",
        "target_gender",
        "target_interests",
        "age_group",
        "user_gender",
        "interests",
    ]

    missing = full_df[required_columns].isna().sum()

    if missing.any():
        invalid_columns = missing[missing > 0].to_dict()

        raise DataValidationError(
            "Missing values introduced during dataset merge: "
            f"{invalid_columns}"
        )

    return full_df


def add_derived_features(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    df = dataframe.copy()

    engagement_events = {
        "Click",
        "Comment",
        "Like",
        "Share",
        "Purchase",
    }

    df["is_engagement"] = (
        df["event_type"].isin(engagement_events)
    )

    df["is_impression"] = (
        df["event_type"] == "Impression"
    )

    df["is_click"] = (
        df["event_type"] == "Click"
    )

    df["is_purchase"] = (
        df["event_type"] == "Purchase"
    )

    df["age_match"] = (
        (df["target_age_group"] == "All")
        | (
            df["target_age_group"]
            == df["age_group"]
        )
    )

    df["gender_match"] = (
        (df["target_gender"] == "All")
        | (
            df["target_gender"]
            == df["user_gender"]
        )
    )

    df["interest_match"] = df.apply(
        _calculate_interest_match,
        axis=1
    )

    df["targeting_match"] = (
        df["age_match"]
        & df["gender_match"]
        & df["interest_match"]
    )

    return df


def _calculate_interest_match(row: pd.Series) -> bool:
    target_interests = {
        interest.strip().lower()
        for interest in str(
            row["target_interests"]
        ).split(",")
        if interest.strip()
    }

    user_interests = {
        interest.strip().lower()
        for interest in str(
            row["interests"]
        ).split(",")
        if interest.strip()
    }

    return bool(
        target_interests.intersection(user_interests)
    )