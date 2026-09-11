from pathlib import Path
from typing import Dict

import pandas as pd


class DataLoadError(Exception):
    """Raised when the project cannot load the required datasets."""


REQUIRED_FILES = {
    "ads": "ads.csv",
    "ad_events": "ad_events.csv",
    "campaigns": "campaigns.csv",
    "users": "users.csv",
}


def load_csv(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise DataLoadError(f"Dataset not found: {file_path}")

    try:
        return pd.read_csv(file_path)
    except Exception as exc:
        raise DataLoadError(
            f"Could not read dataset '{file_path}': {exc}"
        ) from exc


def load_datasets(data_directory: str = "data") -> Dict[str, pd.DataFrame]:
    data_path = Path(data_directory)

    datasets = {}

    for name, filename in REQUIRED_FILES.items():
        datasets[name] = load_csv(data_path / filename)

    return datasets


def validate_dataset_columns(
    datasets: Dict[str, pd.DataFrame]
) -> None:

    required_columns = {
        "ads": {
            "ad_id",
            "campaign_id",
            "ad_platform",
            "ad_type",
            "target_gender",
            "target_age_group",
            "target_interests",
        },
        "ad_events": {
            "event_id",
            "ad_id",
            "user_id",
            "timestamp",
            "day_of_week",
            "time_of_day",
            "event_type",
        },
        "campaigns": {
            "campaign_id",
            "name",
            "start_date",
            "end_date",
            "duration_days",
            "total_budget",
        },
        "users": {
            "user_id",
            "user_gender",
            "user_age",
            "age_group",
            "country",
            "location",
            "interests",
        },
    }

    for dataset_name, required in required_columns.items():

        if dataset_name not in datasets:
            raise DataLoadError(
                f"Missing dataset: {dataset_name}"
            )

        actual = set(datasets[dataset_name].columns)
        missing = required - actual

        if missing:
            raise DataLoadError(
                f"{dataset_name}.csv is missing columns: "
                f"{sorted(missing)}"
            )


def print_dataset_summary(
    datasets: Dict[str, pd.DataFrame]
) -> None:
    print("\nDataset Summary")
    print("=" * 60)

    for name, dataframe in datasets.items():

        print(f"\n{name}")
        print("-" * 60)
        print(f"Rows: {len(dataframe):,}")
        print(f"Columns: {len(dataframe.columns)}")
        print(
            f"Duplicate rows: "
            f"{dataframe.duplicated().sum():,}"
        )
        print(
            f"Missing values: "
            f"{dataframe.isna().sum().sum():,}"
        )