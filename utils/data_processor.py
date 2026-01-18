import os
from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """Generates a comprehensive formatted text report in the exact required order."""
    
    # --- 1. PRE-CALCULATIONS & DATA AGGREGATION ---
    total_rev = sum(float(t['Quantity']) * float(t['UnitPrice']) for t in transactions)
    total_records = len(transactions)
    avg_order = total_rev / total_records if total_records > 0 else 0
    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # Region-wise Aggregation
    region_map = {}
    for t in transactions:
        r = t['Region']
        rev = float(t['Quantity']) * float(t['UnitPrice'])
        if r not in region_map:
            region_map[r] = {'sales': 0, 'count': 0}
        region_map[r]['sales'] += rev
        region_map[r]['count'] += 1
    # Sort by sales amount descending
    sorted_regions = sorted(region_map.items(), key=lambda x: x[1]['sales'], reverse=True)

    # Product Aggregation
    prod_map = {}
    for t in transactions:
        name = t['ProductName']
        rev = float(t['Quantity']) * float(t['UnitPrice'])
        qty = int(t['Quantity'])
        if name not in prod_map: prod_map[name] = {'qty': 0, 'rev': 0}
        prod_map[name]['qty'] += qty
        prod_map[name]['rev'] += rev
    # Sort by revenue descending
    top_prods = sorted(prod_map.items(), key=lambda x: x[1]['rev'], reverse=True)[:5]

    # Customer Aggregation
    cust_map = {}
    for t in transactions:
        cid = t['CustomerID']
        rev = float(t['Quantity']) * float(t['UnitPrice'])
        if cid not in cust_map: cust_map[cid] = {'spent': 0, 'orders': 0}
        cust_map[cid]['spent'] += rev
        cust_map[cid]['orders'] += 1
    # Sort by spending descending
    top_custs = sorted(cust_map.items(), key=lambda x: x[1]['spent'], reverse=True)[:5]

    # Daily Trend Aggregation
    daily_map = {}
    for t in transactions:
        d = t['Date']
        rev = float(t['Quantity']) * float(t['UnitPrice'])
        cid = t['CustomerID']
        if d not in daily_map: daily_map[d] = {'rev': 0, 'trans': 0, 'custs': set()}
        daily_map[d]['rev'] += rev
        daily_map[d]['trans'] += 1
        daily_map[d]['custs'].add(cid)
    sorted_days = sorted(daily_map.items()) # Chronological

    # --- 2. FILE WRITING (EXACT FORMATTING) ---
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        
        # SECTION 1: HEADER
        f.write("="*44 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"         Records Processed: {total_records}\n")
        f.write("="*44 + "\n\n")

        # SECTION 2: OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n" + "-"*44 + "\n")
        f.write(f"Total Revenue:        ₹{total_rev:,.2f}\n")
        f.write(f"Total Transactions:   {total_records}\n")
        f.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # SECTION 3: REGION-WISE PERFORMANCE (DESCENDING)
        f.write("REGION-WISE PERFORMANCE\n" + "-"*44 + "\n")
        f.write(f"{'Region':<10} {'Sales':<15} {'% Total':<12} {'Transactions'}\n")
        for reg, data in sorted_regions:
            perc = (data['sales'] / total_rev * 100) if total_rev > 0 else 0
            f.write(f"{reg:<10} ₹{data['sales']:<14,.0f} {perc:>6.2f}% {data['count']:>10}\n")
        f.write("\n")

        # SECTION 4: TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n" + "-"*44 + "\n")
        f.write(f"{'Rank':<6} {'Product Name':<18} {'Qty':<6} {'Revenue'}\n")
        for i, (name, data) in enumerate(top_prods, 1):
            f.write(f"{i:<6} {name:<18} {data['qty']:<6} ₹{data['rev']:,.2f}\n")
        f.write("\n")

        # SECTION 5: TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n" + "-"*44 + "\n")
        f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<12} {'Order Count'}\n")
        for i, (cid, data) in enumerate(top_custs, 1):
            f.write(f"{i:<6} {cid:<15} ₹{data['spent']:<11,.2f} {data['orders']:>5}\n")
        f.write("\n")

        # SECTION 6: DAILY SALES TREND
        f.write("DAILY SALES TREND\n" + "-"*44 + "\n")
        f.write(f"{'Date':<12} {'Revenue':<15} {'Trans':<8} {'Unique Cust'}\n")
        for d, data in sorted_days:
            f.write(f"{d:<12} ₹{data['rev']:<14,.0f} {data['trans']:<8} {len(data['custs']):>5}\n")
        f.write("\n")

        # SECTION 7: PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n" + "-"*44 + "\n")
        best_day = max(daily_map.items(), key=lambda x: x[1]['rev'])[0] if daily_map else "N/A"
        f.write(f"Best selling day: {best_day}\n")
        low_perf = [n for n, d in prod_map.items() if d['qty'] < 5]
        f.write(f"Low performing products: {', '.join(low_perf) if low_perf else 'None'}\n")
        f.write("\n")

        # SECTION 8: API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n" + "-"*44 + "\n")
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        success_rate = (enriched_count / total_records * 100) if total_records > 0 else 0
        failed_prods = list(set(t['ProductName'] for t in enriched_transactions if not t.get('API_Match')))
        
        f.write(f"Total products enriched: {enriched_count}\n")
        f.write(f"Success rate percentage: {success_rate:.1f}%\n")
        f.write(f"Failed products: {', '.join(failed_prods) if failed_prods else 'None'}\n")