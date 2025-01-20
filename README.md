# Customer Service Analysis & Recommendations
## Etraveli Group Analysis 2023-2024

This repository contains a comprehensive analysis of customer service data Etraveli Group bookings, including contact patterns, booking changes, and customer behavior analysis.

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:
python -m venv case_venv
source case_venv/bin/activate

3. Install the required packages:
pip install -r requirements.txt

4. Run the analysis:
python run_analysis.py

## Repository File Descriptions

### customer_service_analysis.py
Contains the `CustomerServiceAnalysis` class with methods for:
- Data preprocessing
- Contact analysis
- Time pattern analysis
- Route analysis
- Financial analysis
- Visualization generation

### run_analysis.py
Main script to execute the analysis, including:
- Argument parsing
- Analysis execution
- Results output
- Figure generation

## requirements.txt 
The following Python packages are required:
- numpy>=1.21.0
- pandas>=1.3.0
- matplotlib>=3.4.0
- seaborn>=0.11.0
- pyarrow>=5.0.0 (for parquet file support)

### analysis.ipynb
Jupyter notebook containing:
- Exploratory data analysis
- Testing visualizations
- Interactive analysis examples

## Output
The analysis generates several visualizations in the `analysis/figures/` directory
presentation of the analysis is in the `presentation.pdf` file


## Contact
Marzieh Saeedimasine - marzieh.saeedimasine@gmail.com
Project Link: https://github.com/marzieh-saeedimasine/MarziehSaeedimasine-20250120

## Acknowledgments
- Etraveli Group for providing the dataset
- Contributors and reviewers
