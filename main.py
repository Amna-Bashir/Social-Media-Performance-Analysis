from pathlib import Path
import sys

from data_loader import (
    DataLoadError,
    load_datasets,
    print_dataset_summary,
    validate_dataset_columns,
)

from preprocessing import (
    DataValidationError,
    add_derived_features,
    build_combined_dataset,
    clean_datasets,
)

from analysis import (
    print_key_findings,
    run_analysis,
)

from visualization import (
    create_all_visualizations,
)


OUTPUT_DIRECTORY = Path("outputs")


def export_results(analyses: dict) -> None:
    """
    Export analysis DataFrames to CSV files.
    """

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    export_mapping = {
        "event_metrics": "event_metrics.csv",
        "ad_performance": "ad_performance.csv",
        "ad_type_performance": "ad_type_performance.csv",
        "platform_performance": "platform_performance.csv",
        "campaign_performance": "campaign_performance.csv",
        "targeting_alignment": "targeting_alignment.csv",
        "targeting_performance": "targeting_performance.csv",
        "time_performance": "time_performance.csv",
        "interest_performance": "interest_performance.csv",
        "event_stage_summary": "event_stage_summary.csv",
    }

    for analysis_name, filename in export_mapping.items():

        dataframe = analyses[analysis_name]

        dataframe.to_csv(
            OUTPUT_DIRECTORY / filename,
            index=False,
        )


def main() -> None:
    """Run the complete analysis application."""

    print("=" * 70)
    print("SOCIAL MEDIA ADVERTISEMENT PERFORMANCE ANALYSIS")
    print("=" * 70)

    try:

        print("\n[1/6] Loading datasets...")

        datasets = load_datasets("data")

        validate_dataset_columns(datasets)

        print_dataset_summary(datasets)

        print("\n[2/6] Cleaning datasets...")

        datasets = clean_datasets(datasets)

        print("Cleaning completed successfully.")

        print("\n[3/6] Building relational dataset...")

        full_df = build_combined_dataset(
            datasets
        )

        print(
            f"Combined dataset: "
            f"{len(full_df):,} event records"
        )

        print("\n[4/6] Creating derived features...")

        full_df = add_derived_features(
            full_df
        )

        print(
            "Created engagement and targeting "
            "alignment features."
        )

        print("\n[5/6] Running performance analysis...")

        analyses = run_analysis(
            full_df,
            datasets["campaigns"],
        )

        export_results(analyses)

        print_key_findings(analyses)

        print("\n[6/6] Creating visualizations...")

        create_all_visualizations(
            analyses,
            OUTPUT_DIRECTORY,
        )

        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)

        print(
            f"\nResults saved to: "
            f"{OUTPUT_DIRECTORY.resolve()}"
        )

    except (
        DataLoadError,
        DataValidationError,
        FileNotFoundError,
        KeyError,
        ValueError,
    ) as exc:

        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )

        sys.exit(1)


if __name__ == "__main__":
    main()