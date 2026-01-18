import sys
import os
from datetime import datetime
from utils import file_handler, data_processor, api_handler

def main():
    """Main execution function for the Sales Analytics System [cite: 464-466]."""
    print("="*40)
    print("SALES ANALYTICS SYSTEM")
    print("="*40)

    try:
        # [1/10] Read sales data file (handle encoding) [cite: 469, 492]
        print("[1/10] Reading sales data...")
        raw_lines = file_handler.read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("× Failed to read sales data. Exiting.")
            return
        print(f"✓ Successfully read {len(raw_lines)} lines")

        # [2/10] Parse and clean transactions [cite: 470, 494]
        print("[2/10] Parsing and cleaning data...")
        parsed_transactions = file_handler.parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # [3/10] Display filter options to user [cite: 471-473, 496-498]
        regions = sorted(list(set(t['Region'] for t in parsed_transactions if t['Region'])))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_transactions]
        min_range, max_range = min(amounts), max(amounts)
        
        print("\nFilter Options Available:")
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min_range:,.0f} - ₹{max_range:,.0f}")

        # [4/10] User interaction for filters [cite: 474-475, 499]
        user_choice = input("Do you want to filter data? (y/n): ").lower()
        selected_region = None
        if user_choice == 'y':
            selected_region = input(f"Enter region name ({', '.join(regions)}): ")

        # [5/10] Validate transactions [cite: 476-477, 500-501]
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = file_handler.validate_and_filter(
            parsed_transactions, region=selected_region
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # [6/10] Perform data analyses [cite: 478, 502-503]
        print("[5/10] Analyzing sales data...")
        # (Internal logic handled within report generation call)
        print("✓ Analysis complete")

        # [7/10] Fetch products from API [cite: 479, 504-505]
        print("[6/10] Fetching product data from API...")
        api_products = api_handler.fetch_all_products()
        mapping = api_handler.create_product_mapping(api_products)

        # [8/10] Enrich sales data with API info [cite: 480, 506-507]
        # Step 1: Enrich (Logic)
        print("[7/10] Enriching sales data...")
        enriched_data = api_handler.enrich_sales_data(valid_transactions, mapping)
        
        matches = sum(1 for t in enriched_data if t.get('API_Match'))
        success_rate = (matches / len(valid_transactions)) * 100 if valid_transactions else 0
        print(f"✓ Enriched {matches}/{len(valid_transactions)} transactions ({success_rate:.1f}%)")

        # [9/10] Save enriched data to file [cite: 481, 508-509]
        # Step 2: Save (File I/O)
        print("[8/10] Saving enriched data...")
        api_handler.save_enriched_data(enriched_data, 'data/enriched_sales_data.txt')
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [10/10] Generate comprehensive report [cite: 482, 510-511]
        print("[9/10] Generating report...")
        # Prepare small summary for the report generator
        failed_names = [t['ProductName'] for t in enriched_data if not t.get('API_Match')]
        enrichment_metrics = {'count': matches, 'failed_names': failed_names}
        
        data_processor.generate_sales_report(
            valid_transactions, 
            enrichment_metrics, 
            mapping, 
            'output/sales_report.txt'
        )
        print("✓ Report saved to: output/sales_report.txt")

        # [11/10] Print success message [cite: 483, 512]
        print("\n[10/10] Process Complete!")
        print("="*40)

    except Exception as e:
        # Error Handling: Display user-friendly messages [cite: 484-487]
        print(f"\nCRITICAL ERROR: {str(e)}")
        print("The program was unable to complete the process.")

if __name__ == "__main__":
    main()