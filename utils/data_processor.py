import os
from collections import defaultdict
from datetime import datetime

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    total_rev = calculate_total_revenue(transactions)
    stats = defaultdict(lambda: {'total_sales': 0.0, 'transaction_count': 0})
    for t in transactions:
        reg = t['Region']
        stats[reg]['total_sales'] += (t['Quantity'] * t['UnitPrice'])
        stats[reg]['transaction_count'] += 1
    for reg in stats:
        stats[reg]['percentage'] = round((stats[reg]['total_sales'] / total_rev) * 100, 2)
    return dict(sorted(stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    prod_stats = defaultdict(lambda: {'qty': 0, 'rev': 0.0})
    for t in transactions:
        name = t['ProductName']
        prod_stats[name]['qty'] += t['Quantity']
        prod_stats[name]['rev'] += (t['Quantity'] * t['UnitPrice'])
    sorted_prods = sorted(prod_stats.items(), key=lambda x: x[1]['qty'], reverse=True)
    return [(name, data['qty'], data['rev']) for name, data in sorted_prods[:n]]

def customer_analysis(transactions):
    cust_stats = defaultdict(lambda: {'total_spent': 0.0, 'purchase_count': 0, 'products': set()})
    for t in transactions:
        cid = t['CustomerID']
        cust_stats[cid]['total_spent'] += (t['Quantity'] * t['UnitPrice'])
        cust_stats[cid]['purchase_count'] += 1
        cust_stats[cid]['products'].add(t['ProductName'])
    final_stats = {}
    for cid, data in cust_stats.items():
        final_stats[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': data['total_spent'] / data['purchase_count'],
            'products_bought': list(data['products'])
        }
    return dict(sorted(final_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))

def daily_sales_trend(transactions):
    trend = defaultdict(lambda: {'revenue': 0.0, 'transaction_count': 0, 'customers': set()})
    for t in transactions:
        d = t['Date']
        trend[d]['revenue'] += (t['Quantity'] * t['UnitPrice'])
        trend[d]['transaction_count'] += 1
        trend[d]['customers'].add(t['CustomerID'])
    sorted_trend = {}
    for d in sorted(trend.keys()):
        sorted_trend[d] = {
            'revenue': trend[d]['revenue'],
            'transaction_count': trend[d]['transaction_count'],
            'unique_customers': len(trend[d]['customers'])
        }
    return sorted_trend

def generate_sales_report(transactions, enrichment_summary, api_mapping, output_file='output/sales_report.txt'):
    total_rev = calculate_total_revenue(transactions)
    avg_order = total_rev / len(transactions) if transactions else 0
    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*44 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("="*44 + "\n\n")

        f.write("OVERALL SUMMARY\n" + "-"*44 + "\n")
        f.write(f"Total Revenue:        ₹{total_rev:,.2f}\n")
        f.write(f"Total Transactions:   {len(transactions)}\n")
        f.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n" + "-"*44 + "\n")
        f.write(f"{'Region':<10} {'Sales':<15} {'% Total':<12} {'Count':<5}\n")
        for reg, data in region_wise_sales(transactions).items():
            f.write(f"{reg:<10} ₹{data['total_sales']:<14,.0f} {data['percentage']:<11}% {data['transaction_count']:<5}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n" + "-"*44 + "\n")
        f.write(f"{'Rank':<5} {'Product Name':<22} {'Qty':<5} {'Revenue':<12}\n")
        for i, (name, qty, rev) in enumerate(top_selling_products(transactions), 1):
            f.write(f"{i:<5} {name:<22} {qty:<5} ₹{rev:,.0f}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n" + "-"*44 + "\n")
        f.write(f"Total products enriched: {enrichment_summary['count']}\n")
        f.write(f"Success rate:            {(enrichment_summary['count']/len(transactions)*100):.1f}%\n")