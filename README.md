# BITSOM_BA_DM2729294-Sales_Analytics_System
# Sales Analytics & Data Enrichment System 📊

A robust Python-based system designed to process raw sales transaction data, enrich it using external API metadata, and generate a comprehensive business intelligence report.

## 🚀 Project Overview
This system automates the lifecycle of sales data:
1.  **Data Ingestion**: Reads and validates raw transaction records from local storage.
2.  **API Enrichment**: Dynamically fetches product metadata (Category, Brand, Rating) from the **DummyJSON API**.
3.  **Advanced Analytics**: Performs regional performance mapping, customer spending analysis, and chronological sales trend tracking.
4.  **Reporting**: Generates a professionally formatted text report with 8 distinct analytical sections.

---

## 🛠️ Technical Implementation: Data Mapping Note
**Mapping Strategy: Modulo Logic**
In this system, I encountered Product IDs (P101-P110) that exceed the standard range of the DummyJSON API. To ensure 100% data enrichment success, I implemented a **Modulo Mapping Logic**. 
* **Mechanism**: The numeric portion of the Product ID is extracted and divided by the total number of API products, using the remainder to select a match.
* **Example**: Product `P107` maps to API Index `7`. This ensures that every transaction—such as a **USB Cable**—is successfully enriched with descriptive metadata (e.g., brand and rating) for complete pipeline testing.

---

## 📊 Project Output Preview
The system generates a detailed `sales_report.txt` in the `output/` folder. Below is a snapshot of the generated analysis:

```text
============================================
           SALES ANALYTICS REPORT
============================================

REGION-WISE PERFORMANCE (Sorted by Sales)
--------------------------------------------
Region     Sales           % of Total   Transactions
North      ₹1,321,605      37.46%       21
South      ₹889,332        25.21%       13
...

TOP 5 PRODUCTS (By Revenue)
--------------------------------------------
Rank   Product Name        Qty    Revenue
1      Monitor             30     ₹493,759
2      Laptop              15     ₹350,000
...

📂 Repository Structure
    -   main.py: The central hub orchestrating the data flow.

    -   utils/: Core logic modules (file_handler.py, api_handler.py, data_processor.py).

    -   data/: Contains raw source files and the final enriched dataset.

    -   output/: Location of the final generated sales report.

    -   requirements.txt: Project dependencies (requests==2.31.0).


⚙️ How to Run
** Clone the repository:
git clone git clone [https://github.com/Prady0301/BITSOM_BA_DM2729294-Sales_Analytics_System.git](https://github.com/Prady0301/BITSOM_BA_DM2729294-Sales_Analytics_System.git)

** Install Dependencies:
pip install -r requirements.txt

** Execute the System:
python3 main.py

