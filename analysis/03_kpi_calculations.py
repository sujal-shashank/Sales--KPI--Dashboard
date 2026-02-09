import pandas as pd
import numpy as np

#KPIs Calculation

def calculate_kpis(df):
    print("Calculating KPIs...")

    kpis= {}
    kpis['Total_Revenue'] = df['Sales'].sum()
    kpis['Total_Profit'] = df['Profit'].sum()
    kpis['Total_Orders'] = df['Order ID'].nunique()
    kpis['Total_Customers'] = df['Customer ID'].nunique()
    kpis['Average_Order_Value'] = df.groupby('Order ID')['Sales'].sum().mean()
    kpis['Average_Profit_Per_Order'] = df.groupby('Order ID')['Profit'].sum().mean()
    kpis['Profit_Margin'] = (kpis['Total_Profit']/kpis['Total_Revenue']) *100
    kpis['Average_Discount'] = df['Discount'].mean()*100 
    kpis['Total_Quantity'] = df['Quantity'].sum()
    #ltv = Lifetime Value
    kpis['Customer_ltv'] = df.groupby('Customer ID')['Sales'].sum().mean()

    print("KPIs Calculation Completed!!")
    return kpis

def create_monthly_summary(df):
    monthly = df.groupby(['Year','Month','Month_Name']).agg({
        'Sales' : 'sum',
        'Profit' : 'sum',
        'Quantity' : 'sum',
        'Order ID' : 'nunique',
        'Customer ID' : 'nunique',
        'Discount' : 'mean'
    }).reset_index()

    monthly.columns = ['Year', 'Month_Number', 'Month_Name', 'Total_Sales', 
                       'Total_Profit', 'Total_Quantity', 'Total_Orders', 
                       'Unique_Customers', 'Avg_Discount']
    monthly['Profit_Margin'] = (monthly['Total_Profit'] / monthly['Total_Sales']) * 100
    monthly['Year_Month'] = monthly['Year'].astype(str) + '-' + monthly['Month_Number'].astype(str).str.zfill(2)
    return monthly.sort_values('Year_Month')

def create_category_summary(df):
    category = df.groupby('Category').agg({
        'Sales' : 'sum',
        'Profit' : 'sum',
        'Quantity': 'sum',
        'Order ID' : 'nunique'
    }).reset_index()

    category.columns  = ['Category', 'Total_Sales', 'Total_Profit', 
                        'Total_Quantity', 'Total_Orders']
    
    category['Profit_Margin'] = (category['Total_Profit'] / category['Total_Sales']) *100
    category['Avg_Order_Value'] = category['Total_Sales'] / category['Total_Orders']

    return category.sort_values('Total_Sales', ascending=False)

def create_product_summary(df):
    product = df.groupby(['Category' ,'Sub-Category']).agg({
        "Sales" : 'sum',
        'Profit': 'sum',
        'Quantity': 'sum' 
    }).reset_index()

    product.columns = ['Category','Sub-Category','Total_Sales',
                       'Total_Profit','Total_Quantity']

    product['Profit_Margin'] = (product['Total_Profit'] / product['Total_Sales'])*100

    return product.sort_values('Total_Sales', ascending=False)

def create_customer_summary(df):
    customer = df.groupby('Customer ID').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Segment': 'first',
        'Customer Name': 'first'
    }).reset_index()

    # Fixed: Added comma and 'Total_Orders' to match the 6 columns above
    customer.columns = [
        'Customer ID', 'Total_Sales', 'Total_Profit', 
        'Total_Orders', 'Segment', 'Customer_Name'
    ]

    customer['Value_Segment'] = pd.cut(
        customer['Total_Sales'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['Low', 'Medium', 'High', 'VIP']
    )

    # Fixed: Changed 'Total_Sales' to 'Total_Profit' (Profit Margin is Profit/Sales)
    # Also corrected variable name from monthly to customer
    customer['Profit_Margin'] = (customer['Total_Profit'] / customer['Total_Sales']) * 100
    customer['Profit_per_Order'] = customer['Total_Profit'] / customer['Total_Orders']

    return customer.sort_values('Total_Sales', ascending=False)

def create_regional_summary(df):
    regional = df.groupby(['Region', 'State']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    
    regional.columns = ['Region', 'State', 'Total_Sales', 'Total_Profit', 
                        'Total_Quantity', 'Total_Orders']
    
    regional['Profit_Margin'] = (regional['Total_Profit'] / regional['Total_Sales']) * 100
    
    return regional.sort_values('Total_Sales', ascending=False)







#Execution
if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_sales_data.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    #Calculating KPIs
    kpis = calculate_kpis(df)

    # print(kpis)
    print("\n" + "="*50)
    print("KEY PERFORMANCE INDICATOR:")
    print("="*50)
    for key, value in kpis.items():
        if 'revenue' in key or 'profit' in key or 'value' in key or 'ltv' in key:
            print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
        elif 'margin' in key or 'discount' in key:
            print(f"{key.replace('_', ' ').title()}: {value:.2f}%")
        else:
            print(f"{key.replace('_', ' ').title()}: {value:,.0f}")
    
    # Create summary tables
    print("\nCreating summary tables...")
    
    monthly_summary = create_monthly_summary(df)
    category_summary = create_category_summary(df)
    product_summary = create_product_summary(df)
    customer_summary = create_customer_summary(df)
    regional_summary = create_regional_summary(df)
    
    # Save to outputs folder
    monthly_summary.to_csv('../outputs/monthly_summary.csv', index=False)
    category_summary.to_csv('../outputs/category_summary.csv', index=False)
    product_summary.to_csv('../outputs/product_summary.csv', index=False)
    customer_summary.to_csv('../outputs/customer_summary.csv', index=False)
    regional_summary.to_csv('../outputs/regional_summary.csv', index=False)
    
    # Save KPIs
    kpi_df = pd.DataFrame([kpis])
    kpi_df.to_csv('../outputs/kpis.csv', index=False)
    
    print("\nAll summary tables saved to outputs/ folder!")
    print("\nFiles created:")
    print("- monthly_summary.csv")
    print("- category_summary.csv")
    print("- product_summary.csv")
    print("- customer_summary.csv")
    print("- regional_summary.csv")
    print("- kpis.csv")
