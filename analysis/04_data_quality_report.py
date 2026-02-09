import pandas as pd 
import numpy as np
import os

def generate_quality_report(df):
    print("\n" + "="*60)
    print("DATA QUALITY REPORT")
    print("="*60)
    
    # 1. Dataset Overview
    print("\n1. DATASET OVERVIEW")
    print("-" * 60)
    print(f"Total Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum()/1024**2:.2f} MB")
    print(f"Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")

    # 2. Missing Values
    print("\n2. MISSING VALUES ANALYSIS")
    print("-" * 60)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Percentage': missing_pct.values
    })
    missing_df = missing_df[missing_df['Missing_Count'] > 0]
    
    if len(missing_df) > 0:
        print(missing_df.to_string(index=False))
    else:
        print("✓ No missing values found!")
    
    # 3. Duplicate Records
    print("\n3. DUPLICATE RECORDS")
    print("-" * 60)
    duplicates = df.duplicated().sum()
    dup_pct = (duplicates / len(df)) * 100
    print(f"Duplicate Rows: {duplicates:,} ({dup_pct:.2f}%)")
    
    # 4. Data Validity Checks
    print("\n4. DATA VALIDITY CHECKS")
    print("-" * 60)
    
    # Check for negative sales
    negative_sales = len(df[df['Sales'] < 0])
    print(f"Negative Sales Records: {negative_sales}")
    
    # Check for negative quantities
    negative_qty = len(df[df['Quantity'] < 0])
    print(f"Negative Quantity Records: {negative_qty}")
    
    # Check for unrealistic discounts
    high_discount = len(df[df['Discount'] > 1])
    print(f"Discounts > 100%: {high_discount}")
    
    # Check for future dates
    future_dates = len(df[df['Order Date'] > pd.Timestamp.now()])
    print(f"Future Order Dates: {future_dates}")
    
    # 5. Statistical Outliers
    print("\n5. STATISTICAL OUTLIERS (using IQR method)")
    print("-" * 60)
    
    for col in ['Sales', 'Profit', 'Quantity']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = len(df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)])
        outlier_pct = (outliers / len(df)) * 100
        print(f"{col} Outliers: {outliers:,} ({outlier_pct:.2f}%)")
    
    # 6. Data Accuracy Score
    print("\n6. OVERALL DATA ACCURACY")
    print("-" * 60)
    
    total_issues = negative_sales + negative_qty + high_discount + future_dates + duplicates
    accuracy = ((len(df) - total_issues) / len(df)) * 100
    
    print(f"Data Accuracy Score: {accuracy:.2f}%")
    
    if accuracy >= 98:
        print("✓ Excellent data quality!")
    elif accuracy >= 95:
        print("✓ Good data quality")
    else:
        print("⚠ Data quality needs improvement")
    
    # 7. Column Statistics
    print("\n7. NUMERICAL COLUMNS STATISTICS")
    print("-" * 60)
    print(df[['Sales', 'Profit', 'Quantity', 'Discount']].describe())
    
    return accuracy

# Execute
if __name__ == "__main__":
    # Debug: Print current directory
    print("Current working directory:", os.getcwd())
    
    # Try different file paths
    possible_paths = [
        '../data/cleaned_sales_data.csv',
        'data/cleaned_sales_data.csv',
        '../data/raw_sales_data.csv',
        'data/raw_sales_data.csv'
    ]
    
    df = None
    file_path = None
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found file at: {path}")
            file_path = path
            break
        else:
            print(f"✗ File not found at: {path}")
    
    if file_path is None:
        print("\n❌ ERROR: Could not find data file!")
        print("\nPlease check:")
        print("1. Have you run 02_data_cleaning.py?")
        print("2. Is the file in the 'data' folder?")
        print("3. Is the filename correct?")
        exit(1)
    
    try:
        print(f"\nLoading data from: {file_path}")
        df = pd.read_csv(file_path, encoding='latin-1')
        print(f"✓ Data loaded successfully! Shape: {df.shape}")
        
        # Convert Order Date
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
        else:
            print("⚠ Warning: 'Order Date' column not found")
            print("Available columns:", df.columns.tolist())
        
        # Generate report
        accuracy_score = generate_quality_report(df)
        
        # Save report
        output_dir = '../outputs' if os.path.exists('../outputs') else 'outputs'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        
        report_path = os.path.join(output_dir, 'data_quality_report.txt')
        with open(report_path, 'w') as f:
            f.write(f"Data Quality Report\n")
            f.write(f"Generated: {pd.Timestamp.now()}\n")
            f.write(f"Overall Accuracy: {accuracy_score:.2f}%\n")
        
        print(f"\n✓ Quality report saved to: {report_path}")
        
    except Exception as e:
        print(f"\n❌ ERROR occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()