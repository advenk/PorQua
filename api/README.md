# Web API for Optimisation functions
This API exposes Mean-Variance Portfolio Optimization function using FastAPI. It takes a CSV file with historical asset returns and computes the optimal asset allocation based on a given risk preference.

## Running the API
```bash
$ uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Sample curl:
```bash
curl --location 'http://localhost:8000/optimize/mean-variance?risk_aversion=41.0&min_weight=0.0&max_weight=0.3' \
--header 'accept: application/json' \
--form 'returns_file=@"/PorQua/data/msci_country_indices.csv"'
```

Response:
```json
{
    "status": "success",
    "weights": {
        "AT": 1.2052032101828233e-06,
        "AU": 0.29997631914765566,
        "BE": 8.342955755104206e-07,
        "CA": 0.1765566685844061,
        "CH": 1.8889019242108776e-06,
        "DE": 1.5151366692638624e-06,
        "DK": 0.2999978474476036,
        "ES": 1.2570994632592817e-06,
        "FI": 1.270548825342419e-06,
        "FR": 2.402122946042828e-06,
        "GB": 2.4623253672508576e-06,
        "GR": 2.4028398152166093e-07,
        "HK": 0.004638581807864141,
        "IE": 5.995208591756385e-07,
        "IL": 2.456916653726685e-06,
        "IT": 7.969343021433206e-07,
        "JP": 2.1611099732570826e-06,
        "NL": 3.206998927771042e-06,
        "NO": 0.0726550838763146,
        "NZ": 0.14606365832851156,
        "PT": 7.250026191131217e-07,
        "SE": 4.190227174699037e-05,
        "SG": 1.3530975995070921e-05,
        "US": 3.338515860452832e-05
    },
    "statistics": {
        "expected_annual_return": 0.0968877653224932,
        "annual_volatility": 0.12430404808618441,
        "sharpe_ratio": 0.7794417544255475
    }
}
```