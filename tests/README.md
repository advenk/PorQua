# MSCI Index Analysis Tests

This directory contains test scripts for analyzing MSCI index data using PorQua's data loader.

## MSCI Data Analysis Script (`test_msci_analysis.py`)

This script performs a comprehensive analysis of MSCI index data, including:
- Calculation of mean daily returns for each index
- Generation of a correlation matrix between all indices
- Validation of the dataset, including record counts and correlation checks

### How to Run

From the project root directory, run:
```bash
python -m tests.test_msci_analysis
```

### Expected Output

The script will output:
1. Mean daily returns for each MSCI index (as percentages)
2. A correlation matrix showing relationships between all indices
3. Validation results including:
   - Number of daily records for each index
   - Correlations between country indices and the World index
   - Validation checks for positive correlations with the World index

### Requirements

The script requires:
- Python 3.x
- pandas
- numpy
- PorQua's data_loader module

All dependencies should be installed through the project's main requirements file. 