

# BITSOM_BA_DM2729294-Sales_Analytics_System

# Sales Analytics System
An automated Python-based data pipeline that processes messy e-commerce sales records, validates transaction data, enriches records using the DummyJSON API, and generates a comprehensive business intelligence report.
## Technical Note: API Enrichment Mapping
The provided dataset contains ProductIDs in the range `P101` to `P110`[cite: 568]. However, the DummyJSON API (standard limit) returns products with IDs `1` to `100`[cite: 301, 311]. 

To demonstrate successful data enrichment as required by the assignment [cite: 367-368, 396]:
* The system extracts the numeric portion of the ID (e.g., 107).
* A modulo-based mapping logic (`id % total_api_products`) is used to link records to existing API metadata.
* This ensures that fields like `API_Category`, `API_Brand`, and `API_Rating` are correctly populated and saved to the final report, fulfilling the technical requirements for API integration[cite: 398, 536].

## Features
- **Encoding Handling**: Successfully reads files in `utf-8`, `latin-1`, or `cp1252`[cite: 61, 72].
- **Data Cleaning**: Automatically removes records with invalid IDs, negative prices, or zero quantities [cite: 44-48].
- **API Integration**: Enriches local sales data with real-time product categories, brands, and ratings from the DummyJSON API[cite: 23, 297].
- **Business Intelligence**: Generates a detailed text report including regional performance and sales trends[cite: 25, 403].

## Repository Structure
sales-analytics-system/
├── main.py              # Main execution flow [cite: 463]
├── requirements.txt     # External dependencies [cite: 17, 560]
├── data/                # Data storage [cite: 14]
│   ├── sales_data.txt   # Input dataset [cite: 15]
│   └── enriched_sales_data.txt # Generated report 
├── utils/               # Module folder [cite: 10]
│   ├── file_handler.py   # File I/O and cleaning [cite: 11]
│   ├── data_processor.py # Analytics logic [cite: 12]
│   └── api_handler.py    # API integration [cite: 13]
└── output/              # Generated reports [cite: 16]
