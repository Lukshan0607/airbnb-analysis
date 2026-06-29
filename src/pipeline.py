"""
Full Automated Pipeline - Inside Airbnb
Expernetic Data Engineer Assignment
Author: Lukshan Sadeepa

Runs the complete pipeline:
  1. Ingest data
  2. Profile & validate
  3. Clean & standardize
  4. Enrich & join
  5. Load to DuckDB star schema
"""

import os
import logging
import pandas as pd
import numpy as np
import duckdb
import gzip
import shutil
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

# ── Logging ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(REPORTS_DIR, 'pipeline.log'), 
                          encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════
# STEP 1: INGEST
# ══════════════════════════════════════════════════════════
def ingest(city_name):
    log.info(f"[INGEST] Starting for {city_name}")
    city_dir = os.path.join(DATA_DIR, city_name)
    os.makedirs(city_dir, exist_ok=True)

    files = [
        'listings.csv.gz', 'calendar.csv.gz',
        'reviews.csv.gz', 'neighbourhoods.csv',
        'neighbourhoods.geojson'
    ]

    for filename in files:
        dest = os.path.join(city_dir, filename)
        src  = os.path.join(DATA_DIR, filename)

        if os.path.exists(dest):
            log.info(f"[INGEST] Already exists: {filename}")
            continue

        if os.path.exists(src):
            shutil.copy2(src, dest)
            log.info(f"[INGEST] Copied: {filename}")
        else:
            log.warning(f"[INGEST] File not found: {filename}")
            continue

        if filename.endswith('.gz'):
            out = dest[:-3]
            with gzip.open(dest, 'rb') as f_in:
                with open(out, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            log.info(f"[INGEST] Extracted: {os.path.basename(out)}")

    log.info(f"[INGEST] Complete for {city_name}")
    return city_dir

# ══════════════════════════════════════════════════════════
# STEP 2: LOAD RAW DATA
# ══════════════════════════════════════════════════════════
def load_raw(city_dir):
    log.info("[LOAD] Loading raw datasets")
    listings       = pd.read_csv(os.path.join(city_dir, 'listings.csv'))
    calendar       = pd.read_csv(os.path.join(city_dir, 'calendar.csv'))
    reviews        = pd.read_csv(os.path.join(city_dir, 'reviews.csv'))
    neighbourhoods = pd.read_csv(os.path.join(city_dir, 'neighbourhoods.csv'))
    log.info(f"[LOAD] listings={listings.shape} calendar={calendar.shape} "
             f"reviews={reviews.shape}")
    return listings, calendar, reviews, neighbourhoods

# ══════════════════════════════════════════════════════════
# STEP 3: CLEAN
# ══════════════════════════════════════════════════════════
def clean(listings, calendar, reviews):
    log.info("[CLEAN] Starting cleaning")

    lc = listings.copy()
    cc = calendar.copy()
    rc = reviews.copy()

    # Price
    lc['price_numeric'] = (
        lc['price'].str.replace('$', '', regex=False)
                   .str.replace(',', '', regex=False)
                   .astype(float)
    )
    lc['price_flag'] = 'ok'
    lc.loc[lc['price_numeric'] < 100,   'price_flag'] = 'suspiciously_low'
    lc.loc[lc['price_numeric'] > 50000, 'price_flag'] = 'suspiciously_high'
    lc.loc[lc['price_numeric'].isna(),  'price_flag'] = 'missing'

    # Dates
    for col in ['host_since', 'first_review', 'last_review', 'last_scraped']:
        lc[col] = pd.to_datetime(lc[col], errors='coerce')
    cc['date'] = pd.to_datetime(cc['date'], errors='coerce')
    rc['date'] = pd.to_datetime(rc['date'], errors='coerce')

    # Calendar boolean
    cc['is_available'] = cc['available'] == 't'

    # Property category
    def simplify(prop):
        if pd.isna(prop): return 'Unknown'
        prop = prop.lower()
        if 'villa' in prop:                          return 'Villa'
        if 'hotel' in prop or 'hostel' in prop:     return 'Hotel/Hostel'
        if 'condo' in prop or 'apartment' in prop:  return 'Apartment/Condo'
        if 'house' in prop or 'home' in prop:       return 'House'
        if 'entire' in prop or 'whole' in prop:     return 'Entire Place'
        if 'private' in prop:                        return 'Private Room'
        if 'shared' in prop:                         return 'Shared Room'
        return 'Other'
    lc['property_category'] = lc['property_type'].apply(simplify)

    # Missing values
    review_cols = [c for c in lc.columns if 'review_scores' in c]
    for col in review_cols:
        lc[col] = lc[col].fillna(-1)
    for col in ['beds', 'bedrooms']:
        lc[col] = lc[col].fillna(lc[col].median())
    lc['host_name']          = lc['host_name'].fillna('Unknown')
    lc['host_is_superhost']  = lc['host_is_superhost'].fillna('f')
    lc['host_response_rate'] = lc['host_response_rate'].fillna('Unknown')
    lc['host_response_time'] = lc['host_response_time'].fillna('Unknown')
    lc['neighbourhood_standard'] = lc['neighbourhood_cleansed'].str.strip().str.title()

    # Drop 100% null columns
    lc = lc.drop(columns=[
        'license', 'calendar_updated', 'neighbourhood_group_cleansed'
    ], errors='ignore')

    # Coordinates
    lc['latitude']  = lc['latitude'].round(5)
    lc['longitude'] = lc['longitude'].round(5)
    lc['coord_flag'] = 'ok'
    lc.loc[(lc['longitude'] < 100.3) | (lc['longitude'] > 100.9), 
           'coord_flag'] = 'invalid_longitude'

    # Reviews - drop null comments
    rc = rc.dropna(subset=['comments'])

    log.info(f"[CLEAN] Done. listings={lc.shape} calendar={cc.shape} reviews={rc.shape}")
    return lc, cc, rc

# ══════════════════════════════════════════════════════════
# STEP 4: ENRICH
# ══════════════════════════════════════════════════════════
def enrich(lc, cc, rc):
    log.info("[ENRICH] Starting enrichment")
    scrape_date = pd.Timestamp('2025-09-27')

    # Review aggregates
    review_agg = rc.groupby('listing_id').agg(
        total_reviews     = ('id', 'count'),
        first_review_date = ('date', 'min'),
        last_review_date  = ('date', 'max'),
        unique_reviewers  = ('reviewer_id', 'nunique')
    ).reset_index()

    # Calendar aggregates
    cal_agg = cc.groupby('listing_id').agg(
        total_days     = ('date', 'count'),
        available_days = ('is_available', 'sum')
    ).reset_index()
    cal_agg['booked_days']    = cal_agg['total_days'] - cal_agg['available_days']
    cal_agg['occupancy_rate'] = (
        cal_agg['booked_days'] / cal_agg['total_days'] * 100
    ).round(2)

    # Neighbourhood aggregates
    temp = lc.merge(cal_agg, left_on='id', right_on='listing_id', how='left')
    temp['price_numeric'] = (
        temp['price'].str.replace('$','',regex=False)
                     .str.replace(',','',regex=False)
                     .astype(float)
    )
    nb_agg = temp.groupby('neighbourhood_standard').agg(
        listing_count = ('id', 'count'),
        median_price  = ('price_numeric', 'median'),
        avg_occupancy = ('occupancy_rate', 'mean'),
        superhost_pct = ('host_is_superhost', lambda x: (x=='t').mean()*100)
    ).reset_index().round(2)

    # Merge all
    master = lc.copy()
    master = master.merge(review_agg, left_on='id', 
                         right_on='listing_id', how='left')
    master = master.merge(cal_agg,    left_on='id', 
                         right_on='listing_id', how='left', 
                         suffixes=('','_cal'))
    master = master.merge(nb_agg, on='neighbourhood_standard', how='left')

    # Fill nulls
    master['total_reviews']    = master['total_reviews'].fillna(0)
    master['unique_reviewers'] = master['unique_reviewers'].fillna(0)

    # Calculated fields
    master['estimated_annual_revenue'] = (
        master['price_numeric'] * master['booked_days']
    ).round(2)
    master['host_tenure_years'] = (
        (scrape_date - master['host_since']).dt.days / 365.25
    ).round(2)
    master['review_frequency_per_month'] = (
        master['total_reviews'] /
        ((scrape_date - master['first_review_date']).dt.days / 30.44)
    ).round(3)
    master['review_frequency_per_month'] = (
        master['review_frequency_per_month']
        .replace([float('inf'), float('-inf')], float('nan'))
    )
    master['price_per_bedroom']  = (
        master['price_numeric'] / master['bedrooms'].replace(0,1)
    ).round(2)
    master['is_commercial_host'] = (
        master['calculated_host_listings_count'] > 1
    )
    master['days_since_last_review'] = (
        scrape_date - master['last_review_date']
    ).dt.days

    log.info(f"[ENRICH] Master table shape: {master.shape}")
    return master, nb_agg

# ══════════════════════════════════════════════════════════
# STEP 5: LOAD TO DUCKDB
# ══════════════════════════════════════════════════════════
def load_to_duckdb(master, nb_agg, city_dir):
    log.info("[DUCKDB] Loading star schema")
    db_path = os.path.join(city_dir, 'airbnb_bangkok.duckdb')
    con = duckdb.connect(db_path)

    con.execute("""
        CREATE OR REPLACE TABLE dim_host AS
        SELECT DISTINCT host_id, host_name, host_is_superhost,
               host_tenure_years, host_response_rate, host_response_time,
               calculated_host_listings_count, is_commercial_host
        FROM master
    """)

    con.execute("""
        CREATE OR REPLACE TABLE dim_neighbourhood AS
        SELECT ROW_NUMBER() OVER (ORDER BY neighbourhood_standard) AS neighbourhood_id,
               neighbourhood_standard AS neighbourhood_name,
               listing_count, median_price, avg_occupancy, superhost_pct
        FROM nb_agg
    """)

    con.execute("""
        CREATE OR REPLACE TABLE dim_property AS
        SELECT ROW_NUMBER() OVER (ORDER BY room_type, property_type) AS property_type_id,
               room_type, property_type, property_category
        FROM (SELECT DISTINCT room_type, property_type, property_category
              FROM master WHERE property_type IS NOT NULL)
    """)

    con.execute("""
        CREATE OR REPLACE TABLE fact_listings AS
        SELECT m.id AS listing_id, m.host_id,
               dn.neighbourhood_id, dp.property_type_id,
               m.price_numeric, m.price_flag, m.occupancy_rate,
               m.booked_days, m.available_days, m.availability_365,
               m.estimated_annual_revenue, m.total_reviews,
               m.review_scores_rating, m.review_frequency_per_month,
               m.minimum_nights, m.accommodates, m.bedrooms,
               m.price_per_bedroom, m.host_tenure_years,
               m.is_commercial_host, m.coord_flag
        FROM master m
        LEFT JOIN dim_neighbourhood dn 
            ON m.neighbourhood_standard = dn.neighbourhood_name
        LEFT JOIN dim_property dp 
            ON m.property_type = dp.property_type
            AND m.room_type = dp.room_type
    """)

    tables = con.execute("SHOW TABLES").df()
    for t in tables['name']:
        count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        log.info(f"[DUCKDB] {t}: {count:,} rows")

    con.close()
    log.info(f"[DUCKDB] Saved to {db_path}")

# ══════════════════════════════════════════════════════════
# STEP 6: SAVE OUTPUTS
# ══════════════════════════════════════════════════════════
def save_outputs(master, nb_agg, city_dir):
    log.info("[SAVE] Saving cleaned outputs")
    clean_dir = os.path.join(city_dir, 'cleaned')
    os.makedirs(clean_dir, exist_ok=True)

    master.to_csv(os.path.join(clean_dir, 'listings_master.csv'),
                  index=False, encoding='utf-8')
    nb_agg.to_csv(os.path.join(clean_dir, 'neighbourhood_aggregates.csv'),
                  index=False, encoding='utf-8')

    # Save metadata
    metadata = {
        'city':                'bangkok',
        'pipeline_run':        datetime.now().isoformat(),
        'listings_rows':       len(master),
        'neighbourhood_count': len(nb_agg),
        'status':              'completed'
    }
    pd.DataFrame([metadata]).to_csv(
        os.path.join(REPORTS_DIR, 'pipeline_metadata.csv'),
        index=False, encoding='utf-8'
    )
    log.info("[SAVE] All outputs saved!")

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def run_pipeline(city_name="bangkok"):
    log.info(f"{'='*50}")
    log.info(f"PIPELINE START: {city_name.upper()}")
    log.info(f"{'='*50}")
    start = datetime.now()

    try:
        city_dir                 = ingest(city_name)
        listings, calendar, reviews, _ = load_raw(city_dir)
        lc, cc, rc               = clean(listings, calendar, reviews)
        master, nb_agg           = enrich(lc, cc, rc)
        save_outputs(master, nb_agg, city_dir)
        load_to_duckdb(master, nb_agg, city_dir)

        duration = (datetime.now() - start).seconds
        log.info(f"PIPELINE COMPLETE in {duration}s")

    except Exception as e:
        log.error(f"PIPELINE FAILED: {e}")
        raise

if __name__ == "__main__":
    run_pipeline("bangkok")