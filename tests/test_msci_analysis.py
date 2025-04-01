import pandas as pd
import numpy as np
from src.data_loader import load_data_msci

def analyze_msci_data():
    try:
        msci_data = load_data_msci()
        
        if not msci_data or 'return_series' not in msci_data or 'bm_series' not in msci_data:
            raise ValueError("No data was loaded from the MSCI dataset or data is incomplete")
        
        country_returns = msci_data['return_series']
        world_returns = msci_data['bm_series']
        
        if not isinstance(country_returns, pd.DataFrame) or not isinstance(world_returns, pd.DataFrame):
            raise ValueError("MSCI data is not in the expected DataFrame format")
            
        print("Mean daily returns:")
        
        for country in country_returns.columns:
            mean_return = country_returns[country].mean() * 100 
            print(f"{country}: {mean_return:.2f}%")
        
        world_mean = world_returns.iloc[:, 0].mean() * 100
        print(f"World: {world_mean:.2f}%")
        
        returns_df = country_returns.copy()
        returns_df['World'] = world_returns.iloc[:, 0] 
        
        correlation_matrix = returns_df.corr()
        print("Correlation matrix: ")
        print(correlation_matrix.round(3))

        
        print("Number of daily records for each index: ")
        for country in country_returns.columns:
            print(f"{country}: {len(country_returns[country].dropna())} records")
        print(f"World: {len(world_returns.dropna())} records")
        
        world_index = returns_df['World']
        print("Correlations with world index:")
        for country in country_returns.columns:
            corr = returns_df[country].corr(world_index)
            print(f"{country}: {corr:.3f}")
            assert corr > 0, f"Warning: {country} has non-positive correlation with World index"
                
    except FileNotFoundError:
        print("MSCI file not found")
    except pd.errors.EmptyDataError:
        print("MSCI data file is empty.")
    except pd.errors.ParserError as e:
        print(f"Error parsing the data file: {str(e)}")

if __name__ == "__main__":
    try:
        analyze_msci_data()
        print("All validations passed successfully!")
    except AssertionError as e:
        print(f"Validation failed: {str(e)}")
    except ValueError as e:
        print(f"Data validation error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 