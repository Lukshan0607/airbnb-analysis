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
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# ── Paths ──────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
PLOTS_DIR   = os.path.join(REPORTS_DIR, 'plots')
OUTPUT_PATH = os.path.join(REPORTS_DIR, 'Bangkok_Airbnb_Analysis_Report.pdf')

# ── Colors ─────────────────────────────────────────────────
BLUE      = colors.HexColor('#1976d2')
DARK_BLUE = colors.HexColor('#0d47a1')
LIGHT_BLUE= colors.HexColor('#e3f2fd')
RED       = colors.HexColor('#d32f2f')
GRAY      = colors.HexColor('#616161')
LIGHT_GRAY= colors.HexColor('#f5f5f5')
WHITE     = colors.white

# ── Styles ─────────────────────────────────────────────────
styles = getSampleStyleSheet()

title_style = ParagraphStyle('CustomTitle',
    fontSize=28, fontName='Helvetica-Bold',
    textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=10)

subtitle_style = ParagraphStyle('CustomSubtitle',
    fontSize=14, fontName='Helvetica',
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=20)

h1_style = ParagraphStyle('H1',
    fontSize=18, fontName='Helvetica-Bold',
    textColor=DARK_BLUE, spaceBefore=20, spaceAfter=10,
    borderPad=5)

h2_style = ParagraphStyle('H2',
    fontSize=13, fontName='Helvetica-Bold',
    textColor=BLUE, spaceBefore=15, spaceAfter=8)

h3_style = ParagraphStyle('H3',
    fontSize=11, fontName='Helvetica-Bold',
    textColor=DARK_BLUE, spaceBefore=10, spaceAfter=6)

body_style = ParagraphStyle('Body',
    fontSize=10, fontName='Helvetica',
    textColor=colors.black, spaceAfter=8,
    alignment=TA_JUSTIFY, leading=14)

bullet_style = ParagraphStyle('Bullet',
    fontSize=10, fontName='Helvetica',
    textColor=colors.black, spaceAfter=4,
    leftIndent=20, leading=14)

caption_style = ParagraphStyle('Caption',
    fontSize=9, fontName='Helvetica-Oblique',
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)

highlight_style = ParagraphStyle('Highlight',
    fontSize=10, fontName='Helvetica',
    textColor=DARK_BLUE, spaceAfter=8,
    backColor=LIGHT_BLUE, borderPad=8,
    alignment=TA_JUSTIFY, leading=14)

# ── Helper functions ───────────────────────────────────────
def section_header(text, number):
    return [
        HRFlowable(width="100%", thickness=2, color=BLUE, spaceAfter=5),
        Paragraph(f"{number}. {text}", h1_style),
        HRFlowable(width="100%", thickness=0.5, color=LIGHT_BLUE, spaceAfter=10),
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

def add_image(filename, width=16*cm, caption=None):
    path = os.path.join(PLOTS_DIR, filename)
    items = []
    if os.path.exists(path):
        items.append(Image(path, width=width, height=width*0.55))
        if caption:
            items.append(Paragraph(caption, caption_style))
    return items

def make_table(data, col_widths=None, header_color=BLUE):
    t = Table(data, colWidths=col_widths)
    style = TableStyle([
        ('BACKGROUND',  (0,0), (-1,0), header_color),
        ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,0), 10),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,1), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING',  (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
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
    story.append(Paragraph("Data Engineering & Analytics Report", subtitle_style))
    story.append(Spacer(1, 0.5*cm))

    cover_data = [
        ['Prepared for',   'Expernetic (Pvt) Ltd'],
        ['Prepared by',    'Lukshan Sadeepa'],
        ['Role',           'Data Engineer Intern Candidate'],
        ['Dataset',        'Inside Airbnb - Bangkok, Thailand'],
        ['Data Period',    'Scraped September 2025'],
        ['Report Date',    'June 2026'],
    ]
    cover_table = make_table(cover_data, col_widths=[5*cm, 11*cm])
    story.append(cover_table)
    story.append(Spacer(1, 1*cm))
    story.append(highlight(
        "This report presents a comprehensive analysis of the Bangkok Airbnb "
        "short-term rental market using publicly available Inside Airbnb data. "
        "It covers data engineering, exploratory analysis, statistical testing, "
        "and actionable business recommendations."
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
        "Bangkok's Airbnb market is large and diverse with 28,806 listings managed by 8,874 unique hosts across 50 neighbourhoods.",
        "Vadhana is Bangkok's dominant Airbnb neighbourhood with 4,305 listings generating an estimated THB 1.45 billion in annual revenue.",
        "Entire home/apartment listings (65.4%) dominate the market, commanding a median price of THB 1,479 vs THB 1,080 for private rooms.",
        "Strong seasonality exists: peak occupancy of 43% in September vs 23% low in March — a 20-percentage-point seasonal swing.",
        "Market concentration is high: top 10% of hosts control 56% of all listings, indicating professionalization of the hosting market.",
        "Superhosts achieve higher occupancy (31.6% vs 25.4%) and ratings (4.91 vs 4.75) despite charging lower prices than regular hosts.",
        "Property size (accommodates, bedrooms) is the strongest price driver, explaining most of the 40% variance captured by OLS regression.",
        "Value for money is the weakest review dimension (4.647/5), suggesting pricing pressure from guests seeking better value.",
        "COVID-19 caused a severe demand crash in 2020-2021, but the market recovered strongly in 2023-2024 with review volumes reaching record highs.",
    ]
    for f in findings:
        story.append(bullet(f))

    story.append(subsection_header("Top Business Recommendations"))
    recs = [
        "Hosts should target the THB 1,000-2,500 price range where demand is highest.",
        "Dynamic pricing during July-September peak season (raise rates 20-30%) can significantly boost revenue.",
        "Achieving Superhost status drives occupancy more effectively than price reductions.",
        "Investors should target Vadhana, Khlong Toei, and Bang Rak for highest revenue potential.",
    ]
    for r in recs:
        story.append(bullet(r))
    story.append(PageBreak())

    # ── 2. OBJECTIVES & SCOPE ──────────────────────────────
    story += section_header("Objectives & Scope", 2)
    story.append(body(
        "The primary objective of this analysis is to transform raw Inside Airbnb data "
        "into actionable market intelligence for a hypothetical Airbnb market intelligence "
        "consultancy. The analysis targets product managers, revenue strategists, and "
        "operations leads seeking data-driven insights."
    ))
    story.append(subsection_header("City Selected: Bangkok, Thailand"))
    story.append(body(
        "Bangkok was selected as the primary analysis city due to its large dataset size "
        "(28,806 listings), diverse property mix, rich review history dating to 2011, and "
        "regional relevance. Bangkok represents one of Southeast Asia's most dynamic short-"
        "term rental markets, offering rich analytical opportunities."
    ))
    story.append(subsection_header("Sections Completed"))
    scope_data = [
        ['Section', 'Topic', 'Status', 'Priority'],
        ['02', 'Dataset Familiarization', 'Complete', 'Mandatory'],
        ['03', 'Data Engineering', 'Complete', 'Recommended'],
        ['04', 'Exploratory Data Analysis', 'Complete', 'Recommended'],
        ['05', 'Statistical Analysis', 'Complete', 'Recommended'],
        ['06', 'Data Science & ML', 'Not completed', 'Optional'],
        ['07', 'AI & LLM', 'Not completed', 'Optional'],
        ['08', 'Open Innovation', 'Not completed', 'Optional'],
    ]
    story.append(make_table(scope_data,
        col_widths=[2*cm, 6*cm, 4*cm, 4*cm]))
    story.append(spacer())
    story.append(highlight(
        "Prioritization rationale: Sections 02-05 were selected to demonstrate depth "
        "over breadth. Each section was completed thoroughly with clean code, documented "
        "decisions, and business interpretations — consistent with the assignment's "
        "stated philosophy that quality outweighs quantity."
    ))
    story.append(PageBreak())

    # ── 3. DATASET OVERVIEW ────────────────────────────────
    story += section_header("Dataset Overview", 3)
    story.append(subsection_header("Data Source"))
    story.append(body(
        "All data sourced exclusively from Inside Airbnb (insideairbnb.com), an "
        "independent, publicly available dataset providing detailed Airbnb listing "
        "information. The Bangkok dataset was scraped September 26-28, 2025."
    ))
    story.append(subsection_header("Files Used"))
    files_data = [
        ['File', 'Rows', 'Columns', 'Description'],
        ['listings.csv', '28,806', '79', 'Core listing data with pricing, host, location'],
        ['calendar.csv', '10,514,202', '7', 'Daily availability for 365 days per listing'],
        ['reviews.csv', '583,333', '6', 'Guest review text and metadata'],
        ['neighbourhoods.csv', '50', '2', 'Bangkok neighbourhood names'],
        ['neighbourhoods.geojson', 'N/A', 'N/A', 'Neighbourhood boundary polygons'],
    ]
    story.append(make_table(files_data,
        col_widths=[4*cm, 2.5*cm, 2.5*cm, 8*cm]))
    story.append(spacer())

    story.append(subsection_header("Key Relationships"))
    story.append(body(
        "listings.id is the primary key linking all datasets. calendar.listing_id "
        "achieves 100% match with listings (all 28,806 listings have calendar entries). "
        "reviews.listing_id matches 18,716 listings (65%) — the remaining 35% are new "
        "or inactive listings with no review history."
    ))

    story.append(subsection_header("Dataset Limitations"))
    limitations = [
        "Snapshot data only — scraped Sep 26-28, 2025; does not reflect real-time changes.",
        "Calendar price columns are 100% null — revenue estimation relies on listings price.",
        "19% of listings (5,533) have missing price data.",
        "35% of listings (10,090) have no reviews — new or inactive listings.",
        "neighbourhood_group field is 100% null for Bangkok.",
        "Some minimum_nights values exceed 365 days (likely long-term rentals, not short-term).",
        "4 listings have longitude values outside Bangkok's expected range (Nong Chok border area).",
    ]
    for l in limitations:
        story.append(bullet(l))
    story.append(PageBreak())

    # ── 4. METHODOLOGY ─────────────────────────────────────
    story += section_header("Methodology", 4)
    story.append(body(
        "The analytical approach follows a structured data engineering workflow: "
        "ingestion → profiling → cleaning → enrichment → modeling → analysis. "
        "Python was selected as the primary language for its rich ecosystem of "
        "data engineering and analytics libraries."
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
    ]
    story.append(make_table(method_data,
        col_widths=[3.5*cm, 5*cm, 8.5*cm]))
    story.append(PageBreak())

    # ── 5. ENGINEERING APPROACH ────────────────────────────
    story += section_header("Engineering Approach", 5)
    story.append(subsection_header("Pipeline Architecture"))
    story.append(body(
        "A modular, automated pipeline (src/pipeline.py) was implemented with five "
        "distinct stages: ingest, load, clean, enrich, and load-to-DuckDB. The pipeline "
        "completes end-to-end in approximately 25 seconds and is configurable for any "
        "Inside Airbnb city with minimal code changes."
    ))

    story.append(subsection_header("Star Schema Design"))
    schema_data = [
        ['Table', 'Type', 'Rows', 'Key Columns'],
        ['fact_listings', 'Fact', '28,806', 'listing_id, host_id, neighbourhood_id, price_numeric'],
        ['dim_host', 'Dimension', '8,874', 'host_id, superhost, tenure_years'],
        ['dim_neighbourhood', 'Dimension', '50', 'neighbourhood_id, median_price, occupancy'],
        ['dim_property', 'Dimension', '85', 'property_type_id, room_type, category'],
        ['dim_date', 'Dimension', '367', 'date_id, year, month, is_weekend'],
    ]
    story.append(make_table(schema_data,
        col_widths=[4*cm, 3*cm, 2*cm, 8*cm]))
    story.append(spacer())

    story.append(subsection_header("Engineering Decision Log"))
    decisions = [
        "DuckDB over PostgreSQL: Chosen for zero-configuration setup, excellent analytical query performance, and no server requirement — ideal for a local analytical workload.",
        "pandas over PySpark: Dataset fits in memory (112MB for listings); PySpark overhead not justified. Calendar (1.5GB) handled via DuckDB queries to avoid MemoryError.",
        "Sentinel value (-1) for missing review scores: Preserves the distinction between 'no reviews yet' and 'rated zero' — important for accurate filtering in analysis.",
        "neighbourhood_cleansed over neighbourhood: neighbourhood_cleansed has 0 nulls vs 67% nulls in neighbourhood field — clear choice for reliability.",
        "IQR method for outlier detection: Robust to non-normal distributions (price is heavily right-skewed). Flagged rather than removed to preserve data for analysis.",
    ]
    for d in decisions:
        story.append(bullet(d))
    story.append(PageBreak())

    # ── 6. EDA FINDINGS ───────────────────────────────────
    story += section_header("EDA Findings", 6)

    story.append(subsection_header("6.1 Price Distribution"))
    story += add_image('fig01_price_distribution.png',
        caption='Figure 1: Price distribution and room type comparison')
    story.append(body(
        "Bangkok listing prices are strongly right-skewed. The median price of THB 1,358 "
        "is significantly lower than the mean of THB 1,825, indicating a small number of "
        "luxury listings pulling the average up. Entire homes command the highest median "
        "price (THB 1,479), while shared rooms cluster tightly at the budget end (median THB 360)."
    ))
    story.append(spacer())

    story.append(subsection_header("6.2 Neighbourhood Pricing"))
    story += add_image('fig02_neighbourhood_pricing.png',
        caption='Figure 2: Neighbourhood pricing and occupancy analysis')
    story.append(body(
        "Parthum Wan commands the highest median price — Bangkok's CBD and luxury hotel "
        "district. The scatter plot reveals that high listing count does not equal high "
        "occupancy: Vadhana has the most listings but moderate occupancy, suggesting a "
        "competitive, volume-driven market. Mid-price neighbourhoods (green dots) "
        "consistently achieve higher occupancy rates."
    ))
    story.append(PageBreak())

    story.append(subsection_header("6.3 Seasonal Trends"))
    story += add_image('fig03_seasonal_trends.png',
        caption='Figure 3: Monthly occupancy rates and annual review volume')
    story.append(body(
        "Bangkok exhibits clear seasonality with peak occupancy in July-September (40-43%), "
        "coinciding with international summer travel. The annual review volume chart shows "
        "strong pre-COVID growth (2015-2019), a severe crash in 2020-2021, and a record "
        "recovery in 2024. The 2025 partial year shows continued strong demand."
    ))
    story.append(PageBreak())

    story.append(subsection_header("6.4 Host Analysis"))
    story += add_image('fig04_host_analysis.png',
        caption='Figure 4: Host portfolio distribution and market concentration')
    story.append(body(
        "The majority of hosts (5,565) manage a single listing, but the Lorenz curve "
        "reveals significant market concentration: the top 10% of hosts control 56% of "
        "all listings. Superhosts charge less but achieve higher occupancy and ratings. "
        "Host tenure shows that 5-10 year hosts achieve the highest occupancy rates."
    ))
    story.append(PageBreak())

    story.append(subsection_header("6.5 Review Analysis"))
    story += add_image('fig05_review_analysis.png',
        caption='Figure 5: Review scores and sub-dimension analysis')
    story.append(body(
        "Review scores are heavily left-skewed (mean 4.69, median 4.85), indicating "
        "potential rating inflation. Communication scores are highest (4.781) while "
        "Value scores are lowest (4.647) — guests feel some listings are overpriced "
        "relative to quality. High review count listings cluster in the THB 500-3,000 "
        "range, confirming mid-market listings drive the most consistent demand."
    ))
    story.append(PageBreak())

    # ── 7. STATISTICAL FINDINGS ────────────────────────────
    story += section_header("Statistical Findings", 7)
    story.append(subsection_header("7.1 Hypothesis Testing Results"))
    hyp_data = [
        ['Hypothesis', 'Test', 'p-value', 'Effect Size', 'Decision'],
        ['H1: Entire home > Private room price',
         'Mann-Whitney U', '<0.001', "Cohen's d=0.34 (Small)", 'REJECT H0'],
        ['H2: Superhost > Regular ratings',
         'Mann-Whitney U', '<0.001', 'RBC=-0.31', 'REJECT H0'],
        ['H3: Review count affects price',
         'Mann-Whitney U', '0.013', 'RBC=0.02 (Tiny)', 'REJECT H0*'],
        ['H4: Neighbourhood prices differ',
         'Kruskal-Wallis', '<0.001', 'Eta2=0.10 (Medium)', 'REJECT H0'],
        ['H5: Weekend vs weekday differ',
         'Chi-Square', '<0.001', "Cramer's V=0.003", 'REJECT H0*'],
    ]
    story.append(make_table(hyp_data,
        col_widths=[5*cm, 3.5*cm, 2*cm, 3.5*cm, 3*cm]))
    story.append(spacer())
    story.append(highlight(
        "* H3 and H5 are statistically significant but practically insignificant. "
        "H3 shows a THB 17 price difference between listing groups — negligible in "
        "business terms. H5 shows only 0.3% difference in weekend vs weekday occupancy "
        "(31.2% vs 31.5%) — Bangkok Airbnb demand does not follow a weekend pattern, "
        "unlike leisure-focused markets."
    ))

    story.append(subsection_header("7.2 OLS Regression - Price Drivers"))
    story += add_image('fig07_regression.png',
        caption='Figure 7: OLS regression coefficients and residual plot')
    reg_data_table = [
        ['Feature', 'Coefficient (THB)', 'p-value', 'Interpretation'],
        ['bedrooms', '+341', '<0.001', 'Each extra bedroom adds THB 341/night'],
        ['accommodates', '+247', '<0.001', 'Each extra guest capacity adds THB 247/night'],
        ['is_entire_home', '+729', '<0.001', 'Entire home premium over shared room'],
        ['is_private_room', '+457', '<0.001', 'Private room premium over shared room'],
        ['is_superhost', '+28', '0.125', 'NOT significant after controlling for other factors'],
        ['host_tenure_years', '-8', '0.001', 'Older hosts price slightly lower'],
        ['minimum_nights', '-1.3', '<0.001', 'Longer minimum stays = slightly lower price'],
    ]
    story.append(make_table(reg_data_table,
        col_widths=[4*cm, 3.5*cm, 2*cm, 7.5*cm]))
    story.append(spacer())
    story.append(body(
        "The OLS model achieves R2=0.399, explaining 40% of price variance. "
        "Property size variables (accommodates, bedrooms) are the dominant drivers. "
        "The residual plot reveals heteroscedasticity — model performance degrades for "
        "high-priced luxury listings. A log-transformed price model or gradient boosting "
        "approach would improve predictions for the luxury segment."
    ))
    story.append(PageBreak())

    # ── 8. BUSINESS RECOMMENDATIONS ───────────────────────
    story += section_header("Business Recommendations", 8)

    recs_data = [
        ['Stakeholder', 'Recommendation', 'Evidence'],
        ['New Hosts',
         'Price between THB 1,000-2,500 and pursue Superhost status',
         'Median price THB 1,379; Superhosts achieve 31.6% vs 25.4% occupancy'],
        ['Existing Hosts',
         'Implement dynamic pricing: +20-30% in Jul-Sep, discounts in Feb-Mar',
         'Sep occupancy 43.2% vs Mar 23.4% — 20pt seasonal swing'],
        ['Property Investors',
         'Target Vadhana, Khlong Toei, Bang Rak for highest revenue',
         'Vadhana generates THB 1.45B total estimated annual revenue'],
        ['Platform Operators',
         'Investigate Value score gap — lowest sub-dimension at 4.647',
         'Guests consistently rate value lower than other dimensions'],
        ['Revenue Strategists',
         'Focus on entire home/apt listings — 37% price premium confirmed',
         'Entire home median THB 1,479 vs private room THB 1,080 (p<0.001)'],
    ]
    story.append(make_table(recs_data,
        col_widths=[3.5*cm, 6.5*cm, 7*cm]))
    story.append(PageBreak())

    # ── 9. LIMITATIONS & CAVEATS ──────────────────────────
    story += section_header("Limitations & Caveats", 9)
    story.append(body(
        "Several important limitations should be considered when interpreting findings:"
    ))
    caveats = [
        "Revenue estimates are approximations: calendar price data is 100% null, so revenue = listings_price x booked_days. Actual revenue may differ if hosts offer discounts or surge pricing.",
        "Occupancy proxy: booked days are inferred from calendar availability (days marked unavailable). This conflates fully booked listings with hosts who block dates manually.",
        "Review count as demand proxy: guests who do not leave reviews are not captured, potentially underestimating true demand for newer listings.",
        "Snapshot limitation: data reflects a single point in time (Sep 2025). Market dynamics may have shifted since scraping.",
        "Price outliers: listings priced above THB 50,000/night (37 listings) were flagged but retained. These may distort mean-based statistics.",
        "OLS assumptions: The residual plot confirms heteroscedasticity, violating OLS assumptions. Coefficients remain unbiased but standard errors may be underestimated.",
    ]
    for c in caveats:
        story.append(bullet(c))
    story.append(PageBreak())

    # ── 10. FUTURE IMPROVEMENTS ───────────────────────────
    story += section_header("Future Improvements", 10)
    improvements = [
        "Price prediction model: Implement gradient boosting (XGBoost/LightGBM) with log-transformed price target to handle skewed distribution and capture non-linear relationships.",
        "NLP on reviews: Apply sentiment analysis and topic modeling (BERTopic) to 583,263 reviews to extract structured insights from unstructured text.",
        "Multi-city expansion: Extend pipeline to compare Bangkok with other Southeast Asian cities (Singapore, Kuala Lumpur, Jakarta) for regional market intelligence.",
        "Real-time pipeline: Implement incremental processing using change data capture (CDC) to handle monthly Inside Airbnb updates without full reprocessing.",
        "Interactive dashboard: Build a Streamlit dashboard with live filters for neighbourhood, room type, price range, and occupancy to serve non-technical stakeholders.",
        "Geospatial analysis: Use GeoPandas and Folium to create interactive maps of listing density, pricing gradients, and review score clusters across Bangkok.",
        "Demand forecasting: Build time-series models (Prophet, SARIMA) using review volume as demand proxy to forecast seasonal patterns.",
    ]
    for i in improvements:
        story.append(bullet(i))
    story.append(PageBreak())

    # ── 11. REFLECTION ────────────────────────────────────
    story += section_header("Reflection", 11)
    story.append(body(
        "This assignment was approached with a deliberate focus on depth over breadth. "
        "Sections 02-05 were selected because they form the essential foundation of any "
        "data engineering project: understanding the data, building reliable infrastructure, "
        "exploring patterns, and validating findings statistically."
    ))
    story.append(body(
        "The most significant challenge was memory management with the 10.5 million row "
        "calendar dataset. This was resolved by routing large aggregations through DuckDB "
        "rather than loading the full dataset into pandas — a practical production-grade "
        "decision that also demonstrated the value of the star schema architecture."
    ))
    story.append(body(
        "Key trade-offs made: OLS regression was selected over gradient boosting for "
        "interpretability — the assignment emphasized business storytelling, and regression "
        "coefficients are more actionable for non-technical stakeholders than SHAP values. "
        "Sections 06-08 (ML, AI, Open Innovation) were not completed due to time constraints "
        "but detailed future improvement plans are documented above."
    ))
    story.append(PageBreak())

    # ── APPENDIX: AI USAGE ────────────────────────────────
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
         'chart styling suggestions; report structure guidance'],
        ['Prompts Used',
         'Step-by-step guidance prompts for each section; '
         'debugging assistance for memory errors and encoding issues'],
        ['Output Validation',
         'All code was executed and outputs verified before inclusion; '
         'statistical results independently interpreted'],
        ['Modifications Made',
         'Pipeline paths corrected for Windows environment; '
         'memory management improved using DuckDB for large datasets; '
         'matplotlib API updated for newer version compatibility'],
        ['Critical Assessment',
         'AI suggestions for calendar data loading in pandas were rejected '
         'due to MemoryError; DuckDB approach adopted instead. '
         'Coefficient interpretation and business insights are original work.'],
    ]
    story.append(make_table(ai_data, col_widths=[5*cm, 12*cm]))

    # ── BUILD ──────────────────────────────────────────────
    doc.build(story)
    print(f"Report saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_report()