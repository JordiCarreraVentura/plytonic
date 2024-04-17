import datetime
import os

import pandas as pd


PATH_EXAMPLE = 'test.csv'

def make_example():

    if os.path.exists(PATH_EXAMPLE):
        return

    # Sample data
    data = {
        'Manufacturer': ['Toyota', 'Ford', 'Honda', 'Chevrolet', 'Nissan'],
        'Model': ['Corolla', 'F-150', 'Civic', 'Silverado', 'Altima'],
        'Year': [2020, 2019, 2021, 2018, 2022],
        'Sales_Date': [datetime.date(2022, 4, 1), datetime.date(2022, 3, 15), datetime.date(2022, 4, 5), datetime.date(2022, 2, 20), datetime.date(2022, 4, 10)],
        'Sales_Amount': [25000, 35000, 27000, 32000, 28000],
        'Fuel_Efficiency': [30.5, 22.3, 33.1, 21.8, 28.4]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Convert Sales_Date to datetime dtype
    df['Sales_Date'] = pd.to_datetime(df['Sales_Date'])

    # Display DataFrame
    df.to_csv(PATH_EXAMPLE)
