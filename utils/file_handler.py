import os

def read_sales_data(filename):
    """Reads sales data handling encoding and file errors [cite: 64-76]."""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                # Skip header and empty lines
                lines = [line.strip() for line in f.readlines()[1:] if line.strip()]
                return lines
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
            return []
    return []

def parse_transactions(raw_lines):
    """Parses raw lines into clean dictionaries [cite: 84-111]."""
    parsed_data = []
    for line in raw_lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue
        
        try:
            # Clean commas from ProductName and numeric fields [cite: 51, 52]
            product_name = parts[3].replace(',', '')
            quantity = int(parts[4].replace(',', ''))
            unit_price = float(parts[5].replace(',', ''))
            
            transaction = {
                'TransactionID': parts[0],
                'Date': parts[1],
                'ProductID': parts[2],
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': parts[6],
                'Region': parts[7]
            }
            parsed_data.append(transaction)
        except ValueError:
            continue
    return parsed_data

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """Applies validation rules and user filters [cite: 120-152]."""
    valid = []
    invalid_count = 0
    
    # Calculate global stats for user display [cite: 149-150]
    all_regions = sorted(list(set(t['Region'] for t in transactions if t['Region'])))
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    
    summary = {
        'total_input': len(transactions),
        'invalid': 0,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }

    for t in transactions:
        # Validation Rules [cite: 45-48, 141-147]
        is_valid = (
            t['TransactionID'].startswith('T') and
            t['ProductID'].startswith('P') and
            t['CustomerID'].startswith('C') and
            t['Quantity'] > 0 and
            t['UnitPrice'] > 0 and
            t['Region'] != ""
        )
        
        if not is_valid:
            invalid_count += 1
            continue
            
        # Filtering logic
        amount = t['Quantity'] * t['UnitPrice']
        if region and t['Region'] != region:
            summary['filtered_by_region'] += 1
            continue
        if min_amount and amount < min_amount:
            summary['filtered_by_amount'] += 1
            continue
        if max_amount and amount > max_amount:
            summary['filtered_by_amount'] += 1
            continue
            
        valid.append(t)
    
    summary['invalid'] = invalid_count
    summary['final_count'] = len(valid)
    return valid, invalid_count, summary