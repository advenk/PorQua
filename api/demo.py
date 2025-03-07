import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

def generate_sample_returns(n_assets=10, n_days=252):
    """Generate sample daily returns for demonstration"""
    np.random.seed(42)
    
    # Generate random returns with some correlation
    mean_returns = np.random.normal(0.0005, 0.0002, n_assets)
    cov_matrix = np.random.normal(0.0001, 0.00002, (n_assets, n_assets))
    cov_matrix = cov_matrix.dot(cov_matrix.T)  # Ensure positive semi-definite
    np.fill_diagonal(cov_matrix, 0.0004)
    
    returns = np.random.multivariate_normal(mean_returns, cov_matrix, n_days)
    
    # Create DataFrame with dates
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=x)) for x in range(n_days)]
    dates.reverse()
    
    assets = [f"Asset_{i+1}" for i in range(n_assets)]
    returns_df = pd.DataFrame(returns, index=dates, columns=assets)
    
    return returns_df

def main():
    # Generate sample returns data
    returns_df = generate_sample_returns()
    
    # Save to CSV
    csv_path = "sample_returns.csv"
    returns_df.to_csv(csv_path)
    print(f"Generated sample returns data and saved to {csv_path}")
    
    # Send optimization request to API
    url = "http://localhost:8000/optimize/mean-variance"
    files = {"returns_file": ("sample_returns.csv", open(csv_path, "rb"), "text/csv")}
    params = {
        "risk_aversion": 1.0,
        "min_weight": 0.0,
        "max_weight": 0.3  # Maximum 30% in any single asset
    }
    
    try:
        response = requests.post(url, files=files, params=params)
        response.raise_for_status()
        
        result = response.json()
        print("\nOptimization Results:")
        print("Status:", result["status"])
        print("\nOptimal Portfolio Weights:")
        weights = result["weights"]
        for asset, weight in weights.items():
            print(f"{asset}: {weight:.4f}")
            
        # Calculate some portfolio statistics
        weights_series = pd.Series(weights)
        portfolio_return = (returns_df * weights_series).sum(axis=1).mean() * 252  # Annualized
        portfolio_vol = (returns_df * weights_series).sum(axis=1).std() * np.sqrt(252)  # Annualized
        
        print("\nPortfolio Statistics:")
        print(f"Expected Annual Return: {portfolio_return:.2%}")
        print(f"Annual Volatility: {portfolio_vol:.2%}")
        print(f"Sharpe Ratio (assuming 0% risk-free rate): {portfolio_return/portfolio_vol:.2f}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to API: {e}")
    finally:
        # Clean up
        import os
        os.remove(csv_path)

if __name__ == "__main__":
    main()