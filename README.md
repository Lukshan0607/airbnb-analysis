# Bangkok Airbnb Market Intelligence
### Expernetic Data Engineer Intern - Technical Assignment
**Candidate:** Lukshan Sadeepa  
**Dataset:** Inside Airbnb - Bangkok, Thailand (September 2025)

## Project Overview
A comprehensive data engineering and analytics project analyzing Bangkok's 
Airbnb short-term rental market using the Inside Airbnb public dataset. 
The project covers data ingestion, cleaning, enrichment, dimensional modeling, 
exploratory analysis, statistical testing and machine learning.

## Project Structure

    airbnb-analysis/
    ├── data/
    │   └── bangkok/
    │       ├── listings.csv
    │       ├── calendar.csv
    │       ├── reviews.csv
    │       ├── neighbourhoods.csv
    │       ├── airbnb_bangkok.duckdb
    │       └── cleaned/
    ├── notebooks/
    │   ├── 01_dataset_familiarization.ipynb
    │   ├── 02_data_engineering.ipynb
    │   ├── 03_eda.ipynb
    │   ├── 04_statistical_analysis.ipynb
    │   └── 05_data_science.ipynb
    ├── src/
    │   ├── ingest.py
    │   ├── pipeline.py
    │   └── generate_report.py
    └── reports/
        ├── Bangkok_Airbnb_Analysis_Report.pdf
        ├── plots/
        └── pipeline.log

## Sections Completed

| Section | Topic | Status |
|---------|-------|--------|
| 02 | Dataset Familiarization | Complete |
| 03.1 | Data Ingestion and Profiling | Complete |
| 03.2 | Data Cleaning and Standardization | Complete |
| 03.3 | Data Enrichment and Joining | Complete |
| 03.4 | Data Modeling (Star Schema) | Complete |
| 03.5 | Pipeline Design and Automation | Complete |
| 04 | Exploratory Data Analysis | Complete |
| 05 | Statistical Analysis | Complete |
| 06 | Data Science and ML | Complete |

## Key Findings

- 28,806 listings across 50 Bangkok neighbourhoods
- Vadhana is Bangkok's top Airbnb market (4,305 listings, THB 1.45B revenue)
- Peak season July-September (40-43% occupancy) vs low season February-March (23-24%)
- Top 10% of hosts control 56% of all listings
- Superhosts achieve higher occupancy (31.6% vs 25.4%) despite charging less
- XGBoost price model achieves R2=0.61 and MAE=THB 580
- COVID-19 caused severe demand crash in 2020-2021 with record recovery in 2024

## Setup Instructions

**1. Clone the repository**

    git clone https://github.com/Lukshan0607/airbnb-analysis.git
    cd airbnb-analysis

**2. Create virtual environment**

    python -m venv venv
    venv\Scripts\activate

**3. Install dependencies**

    pip install pandas numpy matplotlib seaborn plotly jupyter
    pip install scipy statsmodels scikit-learn duckdb reportlab requests
    pip install xgboost lightgbm shap

**4. Download data**

Download Bangkok dataset from https://insideairbnb.com/get-the-data/ and place all files in the data/ folder.

**5. Run the full pipeline**

    python src/pipeline.py

**6. Generate the report**

    python src/generate_report.py

**7. Explore notebooks**

    jupyter notebook

Open notebooks in order: 01 then 02 then 03 then 04 then 05

## Review Order for Evaluators

1. reports/Bangkok_Airbnb_Analysis_Report.pdf - Start here
2. src/pipeline.py - Main automated pipeline
3. notebooks/01_dataset_familiarization.ipynb - Section 02
4. notebooks/02_data_engineering.ipynb - Section 03
5. notebooks/03_eda.ipynb - Section 04
6. notebooks/04_statistical_analysis.ipynb - Section 05
7. notebooks/05_data_science.ipynb - Section 06

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.14 |
| Data Processing | pandas, numpy |
| Database | DuckDB (star schema) |
| Visualization | matplotlib, seaborn |
| Statistics | scipy, statsmodels |
| ML | scikit-learn, XGBoost, LightGBM, SHAP |
| Pipeline | Custom Python modules |
| Report | ReportLab PDF |
| Version Control | Git, GitHub |

## AI Usage Disclosure

Claude Sonnet 4.6 (Anthropic) was used for code scaffolding, debugging assistance, 
and report structure guidance. All outputs were verified, tested, and interpreted 
independently. Full disclosure in report Appendix A.