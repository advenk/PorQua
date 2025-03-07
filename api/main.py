from fastapi import FastAPI, UploadFile, Query, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from io import StringIO
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import PorQua components
from optimization import MeanVariance, OptimizationParameter, Constraints
from optimization_data import OptimizationData
from covariance import Covariance
from mean_estimation import MeanEstimator

app = FastAPI(title="PorQua API", description="Portfolio Optimization API")

@app.post("/optimize/mean-variance")
async def optimize_mean_variance(
    returns_file: UploadFile,
    risk_aversion: float = Query(1.0, description="Risk aversion parameter (λ)"),
    min_weight: float = Query(0.0, description="Minimum weight per asset"),
    max_weight: float = Query(1.0, description="Maximum weight per asset"),
    mean_estimation_method: str = Query("geometric", description="Method for estimating returns"),
    covariance_method: str = Query("pearson", description="Method for covariance estimation"),
    solver_name: str = Query("cvxopt", description="Solver to use for optimization")
):
    try:
        # Read and validate returns data
        content = await returns_file.read()
        returns_df = pd.read_csv(StringIO(content.decode()), index_col=0, parse_dates=True)
        
        if returns_df.empty:
            raise HTTPException(status_code=400, detail="Empty returns data")
        
        # Ensure returns are numeric
        returns_df = returns_df.astype(float)
        
        # Configure optimization components
        optimization_params = OptimizationParameter(
            risk_aversion=float(risk_aversion),
            solver_name=solver_name,
            verbose=True
        )
        
        # Initialize constraints with asset universe
        asset_universe = returns_df.columns.tolist()
        constraints = Constraints(selection=asset_universe)
        constraints.add_box(box_type="LongOnly", lower=float(min_weight), upper=float(max_weight))
        constraints.add_budget()  # Adds sum of weights = 1 constraint
        
        covariance = Covariance(method=covariance_method)
        mean_estimator = MeanEstimator(method=mean_estimation_method)
        
        # Initialize optimizer
        optimizer = MeanVariance(
            params=optimization_params,
            constraints=constraints,
            covariance=covariance,
            mean_estimator=mean_estimator
        )
        
        # Prepare optimization data
        opt_data = {'return_series': returns_df}
        
        # Set objective and solve
        optimizer.set_objective(opt_data)
        optimizer.solve()
        
        if not optimizer.results['status']:
            raise HTTPException(status_code=400, detail="Optimization failed to converge")
        
        # Calculate portfolio statistics
        weights = pd.Series(optimizer.results['weights'])
        portfolio_return = (returns_df * weights).sum(axis=1).mean() * 252  # Annualized
        portfolio_vol = (returns_df * weights).sum(axis=1).std() * np.sqrt(252)  # Annualized
        
        return JSONResponse({
            "status": "success",
            "weights": optimizer.results['weights'],
            "statistics": {
                "expected_annual_return": float(portfolio_return),
                "annual_volatility": float(portfolio_vol),
                "sharpe_ratio": float(portfolio_return/portfolio_vol) if portfolio_vol > 0 else None
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
