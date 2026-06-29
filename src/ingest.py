"""
Ingestion Pipeline - Inside Airbnb
Expernetic Data Engineer Assignment
Author: Lukshan Sadeepa
"""

import os
import gzip
import shutil
import logging
import requests
import pandas as pd
from datetime import datetime

# ── Base paths (works from any directory) ──────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# ── Ensure folders exist ───────────────────────────────────
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(REPORTS_DIR, 'pipeline.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ── City configuration ─────────────────────────────────────
CITIES = {
    "bangkok": {
        "base_url": "https://data.insideairbnb.com/thailand/central-thailand/bangkok/2025-09-27/data/",
        "files": [
            "listings.csv.gz",
            "calendar.csv.gz",
            "reviews.csv.gz",
            "neighbourhoods.csv",
            "neighbourhoods.geojson"
        ]
    }
}

# ── Download function ──────────────────────────────────────
def download_file(url, dest_path):
    """Download a file from url to dest_path with error handling."""
    try:
        log.info(f"Downloading: {url}")
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        log.info(f"Saved to: {dest_path}")
        return True
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to download {url}: {e}")
        return False

# ── Extract function ───────────────────────────────────────
def extract_gz(gz_path, out_path):
    """Extract a .gz file."""
    try:
        with gzip.open(gz_path, 'rb') as f_in:
            with open(out_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        log.info(f"Extracted: {out_path}")
        return True
    except Exception as e:
        log.error(f"Failed to extract {gz_path}: {e}")
        return False

# ── Metadata tracking ──────────────────────────────────────
def save_metadata(city, files_processed):
    """Track ingestion metadata."""
    metadata = {
        "city": city,
        "ingestion_timestamp": datetime.now().isoformat(),
        "files_processed": str(files_processed),
        "status": "completed"
    }
    df = pd.DataFrame([metadata])
    meta_path = os.path.join(REPORTS_DIR, "ingestion_metadata.csv")
    if os.path.exists(meta_path):
        existing = pd.read_csv(meta_path)
        df = pd.concat([existing, df], ignore_index=True)
    df.to_csv(meta_path, index=False, encoding='utf-8')
    log.info(f"Metadata saved for {city}")

# ── Main ingestion function ────────────────────────────────
def ingest_city(city_name):
    """Main pipeline: download and extract all files for a city."""
    if city_name not in CITIES:
        log.error(f"City '{city_name}' not found in configuration.")
        return

    config = CITIES[city_name]
    city_dir = os.path.join(DATA_DIR, city_name)
    os.makedirs(city_dir, exist_ok=True)

    log.info(f"Starting ingestion for: {city_name}")
    files_processed = []

    for filename in config["files"]:
        url = config["base_url"] + filename
        dest_path = os.path.join(city_dir, filename)

        # Check if file already exists in city folder
        if os.path.exists(dest_path):
            log.info(f"Already exists in city folder, skipping download: {filename}")
            files_processed.append(filename)

        # Check if file exists in root data folder (manually downloaded)
        elif os.path.exists(os.path.join(DATA_DIR, filename)):
            src = os.path.join(DATA_DIR, filename)
            shutil.copy2(src, dest_path)
            log.info(f"Copied from data folder: {filename}")
            files_processed.append(filename)

        # Try downloading
        else:
            log.warning(f"File not found locally, attempting download: {filename}")
            success = download_file(url, dest_path)
            if not success:
                log.error(f"Could not obtain file: {filename}")
                continue

        # Extract if .gz
        extracted_path = dest_path[:-3]
        if filename.endswith('.gz') and not os.path.exists(extracted_path):
            extract_gz(dest_path, extracted_path)

        files_processed.append(filename)

    save_metadata(city_name, files_processed)
    log.info(f"Ingestion complete for {city_name}!")
    log.info(f"Files available in: {city_dir}")
    return city_dir

# ── Run ────────────────────────────────────────────────────
if __name__ == "__main__":
    ingest_city("bangkok")