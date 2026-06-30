"""
Final Report Generator - Bangkok Airbnb Analysis
Expernetic Data Engineer Assignment
Author: Lukshan Sadeepa
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# ── Paths ──────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
PLOTS_DIR   = os.path.join(REPORTS_DIR, 'plots')
OUTPUT_PATH = os.path.join(REPORTS_DIR, 'Bangkok_Airbnb_Analysis_Report.pdf')

# ── Colors ─────────────────────────────────────────────────
BLUE       = colors.HexColor('#1976d2')
DARK_BLUE  = colors.HexColor('#0d47a1')
LIGHT_BLUE = colors.HexColor('#e3f2fd')
GRAY       = colors.HexColor('#616161')
LIGHT_GRAY = colors.HexColor('#f5f5f5')
WHITE      = colors.white

# ── Page width available (A4 - margins) ───────────────────
PAGE_W = 17*cm  # 21cm - 2cm*2 margins

# ── Styles ─────────────────────────────────────────────────
styles = getSampleStyleSheet()

title_style = ParagraphStyle('CustomTitle',
    fontSize=26, fontName='Helvetica-Bold',
    textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=10)

subtitle_style = ParagraphStyle('CustomSubtitle',
    fontSize=13, fontName='Helvetica',
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=20)

h1_style = ParagraphStyle('H1',
    fontSize=16, fontName='Helvetica-Bold',
    textColor=DARK_BLUE, spaceBefore=20, spaceAfter=10)

h2_style = ParagraphStyle('H2',
    fontSize=12, fontName='Helvetica-Bold',
    textColor=BLUE, spaceBefore=12, spaceAfter=6)

body_style = ParagraphStyle('Body',
    fontSize=9.5, fontName='Helvetica',
    textColor=colors.black, spaceAfter=8,
    alignment=TA_JUSTIFY, leading=14)

bullet_style = ParagraphStyle('Bullet',
    fontSize=9.5, fontName='Helvetica',
    textColor=colors.black, spaceAfter=4,
    leftIndent=15, leading=13)

caption_style = ParagraphStyle('Caption',
    fontSize=8.5, fontName='Helvetica-Oblique',
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=8)

highlight_style = ParagraphStyle('Highlight',
    fontSize=9.5, fontName='Helvetica',
    textColor=DARK_BLUE, spaceAfter=8,
    backColor=LIGHT_BLUE, borderPad=6,
    alignment=TA_JUSTIFY, leading=13)

# ── Helper functions ───────────────────────────────────────
def section_header(text, number):
    return [
        HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=4),
        Paragraph(f"{number}. {text}", h1_style),
        HRFlowable(width="100%", thickness=0.5, color=LIGHT_BLUE, spaceAfter=8),
    ]

def subsection_header(text):
    return Paragraph(text, h2_style)

def body(text):
    return Paragraph(text, body_style)

def bullet(text):
    return Paragraph(f"• {text}", bullet_style)

def highlight(text):
    return Paragraph(text, highlight_style)

def spacer(h=0.3):
    return Spacer(1, h*cm)

def add_image(filename, width=PAGE_W, caption=None):
    path = os.path.join(PLOTS_DIR, filename)
    items = []
    if os.path.exists(path):
        items.append(Image(path, width=width, height=width*0.5))
        if caption:
            items.append(Paragraph(caption, caption_style))
    return items

def make_table(data, col_widths=None, header_color=BLUE):
    t = Table(data, colWidths=col_widths)
    style = TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), header_color),
        ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,0), 9),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,1), (-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.4, colors.grey),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('WORDWRAP',      (0,0), (-1,-1), 1),
    ])
    t.setStyle(style)
    return t

# ══════════════════════════════════════════════════════════
# BUILD REPORT
# ══════════════════════════════════════════════════════════
def build_report():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    story = []

    # ── COVER PAGE ─────────────────────────────────────────
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Bangkok Airbnb Market Intelligence", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Data Engineering and Analytics Report", subtitle_style))
    story.append(Spacer(1, 0.5*cm))

    cover_data = [
        ['Prepared for',  'Expernetic (Pvt) Ltd'],
        ['Prepared by',   'Lukshan Sadeepa Karunarathna'],
        ['Role',          'Data Engineer Intern Candidate'],
        ['Dataset',       'Inside Airbnb - Bangkok, Thailand'],
        ['Data Period',   'Scraped September 2025'],
        ['Report Date',   'June 2026'],
    ]
    story.append(make_table(cover_data, col_widths=[5*cm, 12*cm]))
    story.append(Spacer(1, 1*cm))
    story.append(highlight(
        "This report presents a comprehensive analysis of the Bangkok Airbnb "
        "short-term rental market using publicly available Inside Airbnb data. "
        "It covers data engineering, exploratory analysis, statistical testing, "
        "machine learning, and actionable business recommendations."
    ))
    story.append(PageBreak())

    # ── 1. EXECUTIVE SUMMARY ───────────────────────────────
    story += section_header("Executive Summary", 1)
    story.append(body(
        "This report delivers a comprehensive market intelligence analysis of Bangkok's "
        "Airbnb ecosystem using the Inside Airbnb public dataset (September 2025 scrape). "
        "The dataset encompasses 28,806 active listings, 583,333 guest reviews, and over "
        "10.5 million calendar availability records across 50 Bangkok neighbourhoods."
    ))
    story.append(subsection_header("Key Findings"))
    findings = [
        "Bangkok's Airbnb market has 28,806 listings managed by 8,874 unique hosts across 50 neighbourhoods.",
        "Vadhana is Bangkok's dominant neighbourhood with 4,305 listings generating an estimated THB 1.45 billion in annual revenue.",
        "Entire home listings (65.4%) dominate, commanding a median price of THB 1,479 vs THB 1,080 for private rooms.",
        "Strong seasonality: peak occupancy of 43% in September vs 23% low in March — a 20-point seasonal swing.",
        "Market concentration is high: top 10% of hosts control 56% of all listings.",
        "Superhosts achieve higher occupancy (31.6% vs 25.4%) and ratings (4.91 vs 4.75) despite lower prices.",
        "XGBoost price prediction model achieves R2=0.61 and MAE=THB 580 — 61% of price variance explained.",
        "Value for money is the weakest review dimension (4.647/5) suggesting pricing pressure from guests.",
        "COVID-19 caused a severe demand crash in 2020-2021 with strong recovery in 2023-2024.",
    ]
    for f in findings:
        story.append(bullet(f))

    story.append(subsection_header("Top Business Recommendations"))
    recs = [
        "Target the THB 1,000-2,500 price range where demand is highest.",
        "Implement dynamic pricing: raise rates 20-30% during July-September peak season.",
        "Achieving Superhost status drives occupancy more effectively than price reductions.",
        "Investors should target Vadhana, Khlong Toei, and Bang Rak for highest revenue potential.",
    ]
    for r in recs:
        story.append(bullet(r))
    story.append(PageBreak())

    # ── 2. OBJECTIVES & SCOPE ──────────────────────────────
    story += section_header("Objectives and Scope", 2)
    story.append(body(
        "The primary objective is to transform raw Inside Airbnb data into actionable "
        "market intelligence for a hypothetical Airbnb market intelligence consultancy. "
        "The analysis targets product managers, revenue strategists, and operations leads."
    ))
    story.append(subsection_header("City Selected: Bangkok, Thailand"))
    story.append(body(
        "Bangkok was selected due to its large dataset size (28,806 listings), diverse "
        "property mix, rich review history dating to 2011, and regional relevance as one "
        "of Southeast Asia's most dynamic short-term rental markets."
    ))
    story.append(subsection_header("Sections Completed"))
    scope_data = [
        ['Section', 'Topic', 'Status', 'Priority'],
        ['02', 'Dataset Familiarization', 'Complete', 'Mandatory'],
        ['03', 'Data Engineering', 'Complete', 'Recommended'],
        ['04', 'Exploratory Data Analysis', 'Complete', 'Recommended'],
        ['05', 'Statistical Analysis', 'Complete', 'Recommended'],
        ['06', 'Data Science and ML', 'Complete', 'Optional'],
        ['07', 'AI and LLM', 'Not completed', 'Optional'],
        ['08', 'Open Innovation', 'Not completed', 'Optional'],
    ]
    story.append(make_table(scope_data,
        col_widths=[2*cm, 7*cm, 4*cm, 4*cm]))
    story.append(spacer())
    story.append(highlight(
        "Prioritization rationale: Sections 02-06 were completed with depth and rigor. "
        "Quality over quantity — each section includes clean code, documented decisions, "
        "and business interpretations consistent with the assignment philosophy."
    ))
    story.append(PageBreak())

    # ── 3. DATASET OVERVIEW ────────────────────────────────
    story += section_header("Dataset Overview", 3)
    story.append(subsection_header("Data Source"))
    story.append(body(
        "All data sourced from Inside Airbnb (insideairbnb.com), an independent public "
        "dataset providing detailed Airbnb listing information. Bangkok data was scraped "
        "September 26-28, 2025."
    ))
    story.append(subsection_header("Files Used"))
    files_data = [
        ['File', 'Rows', 'Cols', 'Description'],
        ['listings.csv', '28,806', '79', 'Core listing data: pricing, host, location'],
        ['calendar.csv', '10,514,202', '7', 'Daily availability for 365 days per listing'],
        ['reviews.csv', '583,333', '6', 'Guest review text and metadata'],
        ['neighbourhoods.csv', '50', '2', 'Bangkok neighbourhood names'],
        ['neighbourhoods.geojson', 'N/A', 'N/A', 'Neighbourhood boundary polygons'],
    ]
    story.append(make_table(files_data,
        col_widths=[4.5*cm, 2.5*cm, 1.5*cm, 8.5*cm]))
    story.append(spacer())

    story.append(subsection_header("Key Relationships"))
    story.append(body(
        "listings.id is the primary key. calendar.listing_id achieves 100% match "
        "(all 28,806 listings have calendar entries). reviews.listing_id matches 18,716 "
        "listings (65%) — 35% are new or inactive with no review history."
    ))

    story.append(subsection_header("Dataset Limitations"))
    limitations = [
        "Snapshot data only — scraped Sep 26-28, 2025; does not reflect real-time changes.",
        "Calendar price columns are 100% null — revenue estimation relies on listing price.",
        "19% of listings (5,533) have missing price data.",
        "35% of listings (10,090) have no reviews — new or inactive listings.",
        "neighbourhood_group field is 100% null for Bangkok.",
        "Some minimum_nights values exceed 365 days — likely long-term rentals.",
        "4 listings have longitude values outside Bangkok expected range (Nong Chok border).",
    ]
    for l in limitations:
        story.append(bullet(l))
    story.append(PageBreak())

    # ── 4. METHODOLOGY ─────────────────────────────────────
    story += section_header("Methodology", 4)
    story.append(body(
        "The analytical approach follows a structured data engineering workflow: "
        "ingestion, profiling, cleaning, enrichment, modeling, and analysis. "
        "Python was selected as the primary language for its rich ecosystem."
    ))
    method_data = [
        ['Phase', 'Tools Used', 'Rationale'],
        ['Ingestion', 'Python, requests, gzip', 'Repeatable pipeline with logging'],
        ['Profiling', 'pandas, custom functions', 'Systematic quality assessment'],
        ['Cleaning', 'pandas, numpy', 'Standard data standardization'],
        ['Enrichment', 'pandas merge/groupby', 'Feature engineering for analysis'],
        ['Modeling', 'DuckDB, SQL', 'Lightweight analytical database'],
        ['EDA', 'matplotlib, seaborn', 'Publication-quality visualizations'],
        ['Statistics', 'scipy, statsmodels', 'Rigorous hypothesis testing'],
        ['ML', 'scikit-learn, XGBoost, SHAP', 'Price prediction and explainability'],
    ]
    story.append(make_table(method_data,
        col_widths=[3.5*cm, 5.5*cm, 8*cm]))
    story.append(PageBreak())

    # ── 5. ENGINEERING APPROACH ────────────────────────────
    story += section_header("Engineering Approach", 5)
    story.append(subsection_header("Pipeline Architecture"))
    story.append(body(
        "A modular automated pipeline (src/pipeline.py) runs five stages: ingest, load, "
        "clean, enrich, and load-to-DuckDB. It completes end-to-end in 25 seconds and "
        "is configurable for any Inside Airbnb city with minimal code changes."
    ))

    story.append(subsection_header("Star Schema Design"))
    schema_data = [
        ['Table', 'Type', 'Rows', 'Key Columns'],
        ['fact_listings', 'Fact', '28,806',
         'listing_id, host_id, neighbourhood_id, price_numeric'],
        ['dim_host', 'Dimension', '8,874',
         'host_id, superhost, tenure_years'],
        ['dim_neighbourhood', 'Dimension', '50',
         'neighbourhood_id, median_price, occupancy'],
        ['dim_property', 'Dimension', '85',
         'property_type_id, room_type, category'],
        ['dim_date', 'Dimension', '367',
         'date_id, year, month, is_weekend'],
    ]
    story.append(make_table(schema_data,
        col_widths=[3.5*cm, 3*cm, 2*cm, 8.5*cm]))
    story.append(spacer())

    story.append(subsection_header("Engineering Decision Log"))
    decisions = [
        "DuckDB over PostgreSQL: Zero-configuration setup, excellent analytical query performance, no server requirement.",
        "pandas over PySpark: Dataset fits in memory (112MB); calendar (1.5GB) handled via DuckDB to avoid MemoryError.",
        "Sentinel value -1 for missing review scores: Preserves distinction between no reviews yet and rated zero.",
        "neighbourhood_cleansed over neighbourhood: 0 nulls vs 67% nulls — clear reliability choice.",
        "IQR method for outlier detection: Robust to non-normal distributions. Flagged not removed.",
    ]
    for d in decisions:
        story.append(bullet(d))
    story.append(PageBreak())

    # ── 6. EDA FINDINGS ────────────────────────────────────
    story += section_header("EDA Findings", 6)

    story.append(subsection_header("6.1 Price Distribution"))
    story += add_image('fig01_price_distribution.png',
        caption='Figure 1: Price distribution and room type comparison')
    story.append(body(
        "Bangkok prices are strongly right-skewed. Median THB 1,358 vs mean THB 1,825 "
        "indicates luxury listings pulling the average up. Entire homes command median "
        "THB 1,479 while shared rooms cluster at median THB 360."
    ))

    story.append(subsection_header("6.2 Neighbourhood Pricing"))
    story += add_image('fig02_neighbourhood_pricing.png',
        caption='Figure 2: Neighbourhood pricing and occupancy analysis')
    story.append(body(
        "Parthum Wan commands the highest median price. High listing count does not equal "
        "high occupancy — Vadhana has most listings but moderate occupancy. Mid-price "
        "neighbourhoods consistently achieve higher occupancy rates."
    ))
    story.append(PageBreak())

    story.append(subsection_header("6.3 Seasonal Trends"))
    story += add_image('fig03_seasonal_trends.png',
        caption='Figure 3: Monthly occupancy rates and annual review volume')
    story.append(body(
        "Peak occupancy July-September (40-43%), low season February-March (23-24%). "
        "Strong pre-COVID growth (2015-2019), severe crash in 2020-2021, record recovery "
        "in 2024. The 2025 partial year shows continued strong demand."
    ))
    story.append(PageBreak())

    story.append(subsection_header("6.4 Host Analysis"))
    story += add_image('fig04_host_analysis.png',
        caption='Figure 4: Host portfolio distribution and market concentration')
    story.append(body(
        "Majority of hosts manage a single listing but top 10% control 56% of all "
        "listings. Superhosts charge less but achieve higher occupancy and ratings. "
        "Hosts with 5-10 years tenure achieve the highest occupancy rates."
    ))
    story.append(PageBreak())

    story.append(subsection_header("6.5 Review Analysis"))
    story += add_image('fig05_review_analysis.png',
        caption='Figure 5: Review scores and sub-dimension analysis')
    story.append(body(
        "Review scores are heavily left-skewed (mean 4.69, median 4.85) — potential "
        "rating inflation. Communication highest (4.781), Value lowest (4.647). "
        "High review count listings cluster in THB 500-3,000 range."
    ))
    story.append(PageBreak())

    # ── 7. STATISTICAL FINDINGS ────────────────────────────
    story += section_header("Statistical Findings", 7)
    story.append(subsection_header("7.1 Hypothesis Testing Results"))
    hyp_data = [
        ['Hypothesis', 'Test', 'p-value', 'Effect Size', 'Decision'],
        ['H1: Entire home > Private room price',
         'Mann-Whitney U', '<0.001', "Cohen's d=0.34", 'REJECT H0'],
        ['H2: Superhost > Regular ratings',
         'Mann-Whitney U', '<0.001', 'RBC=0.31', 'REJECT H0'],
        ['H3: Review count affects price',
         'Mann-Whitney U', '0.013', 'RBC=0.02 (Tiny)', 'REJECT H0*'],
        ['H4: Neighbourhood prices differ',
         'Kruskal-Wallis', '<0.001', 'Eta2=0.10', 'REJECT H0'],
        ['H5: Weekend vs weekday differ',
         'Chi-Square', '<0.001', "Cramer's V=0.003", 'REJECT H0*'],
    ]
    story.append(make_table(hyp_data,
        col_widths=[5*cm, 3*cm, 1.8*cm, 3.2*cm, 2.5*cm]))
    story.append(spacer())
    story.append(highlight(
        "* H3 and H5 are statistically significant but practically insignificant. "
        "H3 shows only THB 17 price difference. H5 shows only 0.3% occupancy difference "
        "(31.2% vs 31.5%) — Bangkok demand does not follow a weekend pattern."
    ))

    story.append(subsection_header("7.2 OLS Regression - Price Drivers"))
    story += add_image('fig07_regression.png',
        caption='Figure 7: OLS regression coefficients and residual plot')
    reg_data_table = [
        ['Feature', 'Coefficient', 'p-value', 'Interpretation'],
        ['bedrooms', '+THB 341', '<0.001', 'Each extra bedroom adds THB 341/night'],
        ['accommodates', '+THB 247', '<0.001', 'Each extra guest adds THB 247/night'],
        ['is_entire_home', '+THB 729', '<0.001', 'Entire home premium over shared room'],
        ['is_private_room', '+THB 457', '<0.001', 'Private room premium over shared room'],
        ['is_superhost', '+THB 28', '0.125', 'NOT significant after controlling others'],
        ['host_tenure_years', '-THB 8', '0.001', 'Older hosts price slightly lower'],
        ['minimum_nights', '-THB 1.3', '<0.001', 'Longer minimum stays = lower price'],
    ]
    story.append(make_table(reg_data_table,
        col_widths=[4*cm, 2.5*cm, 2*cm, 8.5*cm]))
    story.append(spacer())
    story.append(body(
        "OLS model achieves R2=0.399, explaining 40% of price variance. Property size "
        "variables dominate. Residual plot confirms heteroscedasticity — model performs "
        "better for budget listings than luxury."
    ))
    story.append(PageBreak())

    # ── 8. DATA SCIENCE EXPERIMENTS ───────────────────────
    story += section_header("Data Science Experiments", 8)
    story.append(subsection_header("8.1 Price Prediction Models"))
    ml_data = [
        ['Model', 'MAE', 'RMSE', 'R2', 'MAPE', 'CV R2'],
        ['Linear Regression', 'THB 744', 'THB 1,245', '0.442', '50.2%', '0.422'],
        ['Random Forest', 'THB 637', 'THB 1,085', '0.576', '41.1%', '0.562'],
        ['XGBoost', 'THB 580', 'THB 1,037', '0.613', '35.7%', '0.615'],
        ['LightGBM', 'THB 587', 'THB 1,042', '0.609', '35.9%', '0.612'],
    ]
    story.append(make_table(ml_data,
        col_widths=[3.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 2*cm]))
    story.append(spacer())
    story.append(body(
        "XGBoost achieves best performance with R2=0.613 and MAE=THB 580 — 61% of "
        "price variance explained, a significant improvement over OLS (40%). SHAP "
        "analysis confirms bedrooms and accommodates as dominant price drivers."
    ))
    story += add_image('fig08_price_prediction.png',
        caption='Figure 8: Model comparison, SHAP importance, actual vs predicted')
    story.append(PageBreak())

    story.append(subsection_header("8.2 Listing Segmentation (K-Means K=6)"))
    story.append(body(
        "K-Means clustering with K=6 (silhouette score=0.377) identifies six distinct "
        "listing segments: Large Group, High Demand, Popular Budget, Budget Standard, "
        "Underperforming, and Low Demand. Each segment has unique pricing and occupancy."
    ))
    story += add_image('fig09b_clusters.png',
        caption='Figure 9: Listing segments by price and occupancy')
    story.append(PageBreak())

    story.append(subsection_header("8.3 Model Generalization and Bias"))
    story.append(body(
        "XGBoost generalizes well across Bangkok's top neighbourhoods, achieving R2 > 0.7 "
        "in all tested areas. Sathon (R2=0.833) and Bang Rak (R2=0.832) perform best. "
        "All neighbourhoods achieve MAE below the overall THB 580 benchmark."
    ))
    story += add_image('fig10_model_bias.png',
        caption='Figure 10: Model R2 and MAE by neighbourhood')
    story.append(PageBreak())

    # ── 9. BUSINESS RECOMMENDATIONS ───────────────────────
    story += section_header("Business Recommendations", 9)
    recs_data = [
    ['Stakeholder', 'Recommendation', 'Evidence'],
    ['New Hosts',
     'Price THB 1,000-2,500\nand pursue Superhost status',
     'Median THB 1,379;\nSuperhosts: 31.6% vs 25.4% occupancy'],
    ['Existing Hosts',
     'Dynamic pricing:\n+20-30% Jul-Sep,\ndiscounts Feb-Mar',
     'Sep 43.2% vs Mar 23.4%\n— 20 point seasonal swing'],
    ['Property Investors',
     'Target Vadhana,\nKhlong Toei, Bang Rak',
     'Vadhana generates\nTHB 1.45B annual revenue'],
    ['Platform Operators',
     'Investigate Value score gap\n(lowest dimension at 4.647)',
     'Guests rate value below\nall other dimensions'],
    ['Revenue Strategists',
     'Focus on entire home listings\n— 37% price premium confirmed',
     'Entire home THB 1,479\nvs private room THB 1,080'],
    ]
    story.append(make_table(recs_data,
        col_widths=[3*cm, 7*cm, 7*cm]))
    story.append(PageBreak())

    # ── 10. LIMITATIONS & CAVEATS ─────────────────────────
    story += section_header("Limitations and Caveats", 10)
    caveats = [
        "Revenue estimates are approximations: calendar price data is 100% null, so revenue = listing_price x booked_days.",
        "Occupancy proxy: booked days inferred from calendar unavailability conflates bookings with manual blocks.",
        "Review count as demand proxy may underestimate true demand for newer listings.",
        "Snapshot limitation: data reflects Sep 2025 only. Market dynamics may have shifted.",
        "Price outliers above THB 50,000/night (37 listings) flagged but retained — may distort means.",
        "OLS heteroscedasticity confirmed — coefficients unbiased but standard errors may be underestimated.",
    ]
    for c in caveats:
        story.append(bullet(c))
    story.append(PageBreak())

    # ── 11. FUTURE IMPROVEMENTS ───────────────────────────
    story += section_header("Future Improvements", 11)
    improvements = [
        "Log-transformed price model or neural network for luxury segment (THB 10,000+).",
        "NLP on 583,263 reviews: sentiment analysis and BERTopic topic modeling.",
        "Multi-city pipeline: extend to Singapore, Kuala Lumpur, Jakarta for regional comparison.",
        "Incremental processing using CDC to handle monthly Inside Airbnb updates.",
        "Streamlit interactive dashboard with live filters for non-technical stakeholders.",
        "GeoPandas and Folium geospatial maps for listing density and pricing gradients.",
        "Time-series demand forecasting using Prophet/SARIMA on review volume proxy.",
    ]
    for i in improvements:
        story.append(bullet(i))
    story.append(PageBreak())

    # ── 12. REFLECTION ────────────────────────────────────
    story += section_header("Reflection", 12)
    story.append(body(
        "This assignment was approached with deliberate focus on depth. Sections 02-06 "
        "form the essential foundation: understanding data, building reliable infrastructure, "
        "exploring patterns, validating findings statistically, and applying ML."
    ))
    story.append(body(
        "The most significant challenge was memory management with the 10.5 million row "
        "calendar dataset. Resolved by routing large aggregations through DuckDB rather "
        "than pandas — a practical production-grade decision demonstrating the value of "
        "the star schema architecture."
    ))
    story.append(body(
        "OLS regression was selected over gradient boosting for interpretability in "
        "statistical analysis — coefficients are more actionable for non-technical "
        "stakeholders than SHAP values alone. XGBoost was then applied in Section 06 "
        "to demonstrate improved predictive power (R2: 0.40 to 0.61)."
    ))
    story.append(PageBreak())

    # ── APPENDIX A: AI USAGE ──────────────────────────────
    story += section_header("Appendix A: AI Usage Disclosure", 'A')
    story.append(body(
        "In accordance with Expernetic's AI Tools Usage Policy (Section 10), "
        "the following discloses all AI tool usage during this assignment."
    ))
    ai_data = [
        ['Disclosure Item', 'Details'],
        ['AI Tools Used', 'Claude Sonnet 4.6 (Anthropic)'],
        ['AI-Assisted Sections',
         'Code scaffolding for pipeline.py and generate_report.py; '
         'chart styling; report structure guidance; debugging'],
        ['Prompts Used',
         'Step-by-step guidance prompts per section; '
         'debugging for memory errors and encoding issues'],
        ['Output Validation',
         'All code executed and outputs verified; '
         'statistical results independently interpreted'],
        ['Modifications Made',
         'Pipeline paths corrected for Windows; '
         'memory management improved using DuckDB; '
         'matplotlib API updated for newer version'],
        ['Critical Assessment',
         'AI suggestions for calendar loading in pandas rejected '
         'due to MemoryError; DuckDB adopted instead. '
         'Business insights and interpretations are original work.'],
    ]
    story.append(make_table(ai_data, col_widths=[4.5*cm, 12.5*cm]))

    # ── BUILD ──────────────────────────────────────────────
    doc.build(story)
    print(f"Report saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_report()