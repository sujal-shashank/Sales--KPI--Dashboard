#Data Cleaning
import pandas as pd
import numpy as np

filepath = "../data/raw_sales_data.csv"

def clean_sales_data(filepath):
    print("Starting Cleaning Process")
    
    #Loading Data
    df = pd.read_csv(filepath , encoding='latin-1')
    initial_rows = len(df)
    print(f"Initial Rows: {initial_rows}")

    #Data Conversion
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')

    #Extract date features
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Month_Name'] = df['Order Date'].dt.month_name()
    df['Quarter'] = df['Order Date'].dt.quarter
    df['Day_of_Week'] = df['Order Date'].dt.day_name()
    df['Week_Number'] = df['Order Date'].dt.isocalendar().week

    #Removing Null and Duplicate Values
    df = df.dropna(subset=['Sales','Profit','Quantity'])
    df=df.drop_duplicates()

    #Creating Calculated Columns 
    df['Discount Amount'] = df['Sales']*df['Discount']
    df['Profit Margin'] = df['Profit'] / df['Sales']*100

    #Cleaning Negative Values
    df = df[df['Sales']>0]
    df = df[df['Quantity']>0]

    #Customer Segments
    df['Customer_Segment_Value'] = pd.cut(
        df.groupby('Customer ID')['Sales'].transform('sum'),
        bins=[0,1000,5000,10000, float('inf')],
        labels=['Low', 'Medium','High','VIP']
    )

    final_rows = len(df)
    removed_rows = initial_rows - final_rows

    print(f"Final rows: {final_rows}")
    print(f"Removed rows: {removed_rows}")
    print(f"Data accuracy: {(final_rows/initial_rows)*100:.2f}%")
    print("Data cleaning completed!")

    return df
#Execution
if __name__ == "__main__" :
    df_clean = clean_sales_data(filepath)
    #save clean data
    df_clean.to_csv('../cleaned_sales_data.csv' , index = False)
    print("\nCleaned data saved to: data/cleaned_sales_data.csv")
    
    # Display sample
    print("\n Sample of cleaned data:")
    print(df_clean.head())

