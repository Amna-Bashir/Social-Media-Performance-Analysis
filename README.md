# Dataset
The dataset offers a comprehensive, synthetic view into the performance of a social media advertising campaign.

The core of this dataset is a relational database modeled around four key entities:

Users: Detailed individual profiles, including age, gender, country, location, and interests. This allows for granular demographic analysis and segmentation.

Campaigns: High-level campaign data, including budget, duration, and a clear start/end date, providing the strategic context for all ad-related activities.

Ads: Specific creative assets tied to campaigns, complete with their own targeting parameters for age, gender, and interests. This is essential for evaluating targeting effectiveness.

Ad Events: The central transactional log, capturing every user interaction from a simple Impression to a final Purchase. This table is the key to understanding the full conversion funnel.


The dataset was obtained from Kaggle: Social Media Advertisement Performances - Cecily D


# Social Media Advertisement Performance Analysis

A modular Python application for analyzing social media advertisement
performance across ads, campaigns, platforms, and user audiences.

The project started as an exploratory pandas notebook and was
restructured into a reusable Python analysis pipeline. The final
version focuses on deriving performance metrics from event-level data,
evaluating campaign efficiency, and measuring how closely ad targeting
aligns with the users interacting with each advertisement.

## Features

- CSV data ingestion and validation
- Duplicate detection and removal
- Date and string preprocessing
- Relational dataset merging
- Event-level feature engineering
- Advertisement performance analysis
- Advertisement type comparison
- Platform performance comparison
- Campaign efficiency analysis
- Audience targeting alignment
- Time-of-day performance analysis
- Interest-level performance analysis
- Event-stage analysis
- CSV report generation
- Automated visualization generation
- Modular Python architecture
- Error handling and validation

## Project Structure

```text
social-media-ad-analysis/
│── data_loader.py
│── preprocessing.py
│── metrics.py
│── analysis.py
│── visualization.py
│── main.py
└── README.md
