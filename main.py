import sys
import os
from datetime import datetime
from utils import file_handler, data_processor, api_handler

def main():
    """Main execution function for the Sales Analytics System."""
    print("="*40)
    print("SALES ANALYTICS SYSTEM")
    print("="*40)

    try:
        # [1/10] Read and Parse sales data
        print("[1/10] Reading and parsing sales data...")
        raw_lines = file_handler.read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("× Failed to read sales data. Exiting.")
            return
        parsed_transactions = file_handler.parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # [2/10] Display filter options
        regions = sorted(list(set(t['Region'] for t in parsed_transactions if t['Region'])))
        amounts = [float(t['Quantity']) * float(t['UnitPrice']) for t in parsed_transactions]
        print(f"\nAvailable Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        # [3/10] User interaction for filters
        user_choice = input("\nDo you want to filter by region? (y/n): ").lower()
        selected_region = None
        if user_choice == 'y':
            selected_region = input(f"Enter region name: ")

        # [4/10] Validate and Filter
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = file_handler.validate_and_filter(
            parsed_transactions, region=selected_region
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # [5/10] Fetch and Map API data
        print("[5/10] Fetching product data from API...")
        api_products = api_handler.fetch_all_products()
        mapping = api_handler.create_product_mapping(api_products)

        # [6/10] Enrich sales data
        print("[6/10] Enriching sales data...")
        enriched_data = api_handler.enrich_sales_data(valid_transactions, mapping)
        
        matches = sum(1 for t in enriched_data if t.get('API_Match'))
        print(f"✓ Enrichment complete ({matches} matches)")

        # [7/10] Save enriched data
        print("[7/10] Saving enriched data...")
        api_handler.save_enriched_data(enriched_data, 'data/enriched_sales_data.txt')

        # [8/10] Generate comprehensive report
        # We prepare the summary dictionary expected by your new data_processor
        print("[8/10] Generating comprehensive report...")
        enrichment_metrics = {'count': matches}
        data_processor.generate_sales_report(valid_transactions, enriched_data)
        print("✓ Report saved to: output/sales_report.txt")

        # [9/10] Process Complete
        print("\n[10/10] Process Complete! Your 10-section report is ready.")
        print("="*40)

    except Exception as e:
        print(f"\nCRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    main()