# Week 1 Logistics Analytics — Late Delivery Risk

## Project objective
A strategic planning and data exploration project for logistics analytics. The project uses the public **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS** dataset to study delivery performance and design a leakage-aware late-delivery risk workflow.

## Data source
Constante, Fabian; Silva, Fernando; Pereira, António (2019), *DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS*, Mendeley Data, Version 5, DOI: 10.17632/8gx2fvg2k6.5.

Download the CSV from:
https://data.mendeley.com/datasets/8gx2fvg2k6/5

## Workflow
1. Data validation and grain check
2. Missing-value and duplicate checks
3. KPI calculation
4. Exploratory analysis
5. Leakage-aware feature engineering
6. Logistic-regression baseline
7. K-Means clustering illustration
8. Constrained allocation optimization illustration
9. Evaluation and documentation

## Important leakage rule
Do not use post-delivery variables such as actual shipping duration or delivery status as predictors of whether an order will be late. Those variables reveal the outcome.

## Run
```bash
pip install -r requirements.txt
python code/week1_logistics_analysis.py
```

Place the downloaded CSV at:
`data/DataCoSupplyChainDataset.csv`

## Files
- `docs/Week1_Logistics_Strategic_Planning_Report.docx`
- `code/week1_logistics_analysis.py`
- `data/README.md`
- `requirements.txt`

## Limitations
The Week 1 script is a planning/baseline implementation. It does not claim model performance until the public dataset is actually downloaded and processed. Optimization values in the example are illustrative and must be replaced with measured operational costs, risk estimates, demand, and capacities before real decision use.
