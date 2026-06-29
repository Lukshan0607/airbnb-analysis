---

## Sections Completed

| Section | Topic | Status |
|---------|-------|--------|
| 02 | Dataset Familiarization | ✅ Complete |
| 03.1 | Data Ingestion & Profiling | ✅ Complete |
| 03.2 | Data Cleaning & Standardization | ✅ Complete |
| 03.3 | Data Enrichment & Joining | ✅ Complete |
| 03.4 | Data Modeling (Star Schema) | ✅ Complete |
| 03.5 | Pipeline Design & Automation | ✅ Complete |
| 04 | Exploratory Data Analysis | ✅ Complete |
| 05 | Statistical Analysis | ✅ Complete |

---

## Key Findings
- **28,806 listings** across 50 Bangkok neighbourhoods
- **Vadhana** is Bangkok's top Airbnb market (4,305 listings, ~THB 1.45B revenue)
- **Peak season**: July-September (40-43% occupancy) vs low season February-March (23-24%)
- **Top 10% of hosts** control 56% of all listings
- **Superhosts** achieve higher occupancy (31.6% vs 25.4%) despite charging less
- **Property size** (bedrooms, accommodates) is the strongest price driver (R²=0.40)
- **COVID-19** caused severe demand crash in 2020-2021; record recovery in 2024

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd airbnb-analysis
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn plotly jupyter 
pip install scipy statsmodels scikit-learn duckdb reportlab requests
```

### 4. Download data
Download Bangkok dataset from https://insideairbnb.com/get-the-data/  
Place all files in the `data/` folder.

### 5. Run the full pipeline
```bash
python src/pipeline.py
```

### 6. Generate the report
```bash
python src/generate_report.py
```

### 7. Explore notebooks
```bash
jupyter notebook
```
Open notebooks in order: 01 → 02 → 03 → 04

---

## Review Order for Evaluators
1. `reports/Bangkok_Airbnb_Analysis_Report.pdf` ← Start here
2. `src/pipeline.py` ← Main automated pipeline
3. `notebooks/01_dataset_familiarization.ipynb` ← Section 02
4. `notebooks/02_data_engineering.ipynb` ← Section 03
5. `notebooks/03_eda.ipynb` ← Section 04
6. `notebooks/04_statistical_analysis.ipynb` ← Section 05

---

## Tech Stack
| Category | Tools |
|----------|-------|
| Language | Python 3.14 |
| Data Processing | pandas, numpy |
| Database | DuckDB (star schema) |
| Visualization | matplotlib, seaborn |
| Statistics | scipy, statsmodels |
| Pipeline | Custom Python modules |
| Report | ReportLab PDF |
| Version Control | Git, GitHub |

---

## AI Usage Disclosure
Claude Sonnet 4.6 (Anthropic) was used for:
- Code scaffolding and debugging assistance
- Report structure guidance

All outputs were verified, tested, and interpreted independently.
Full disclosure in report Appendix A.