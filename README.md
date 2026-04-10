# AlphaPulse: Portfolio Risk Analytics Dashboard

> A portfolio analytics project that combines Python-based risk modeling with Tableau dashboards to study returns, volatility, diversification, correlation, Monte Carlo forecasting, and Value at Risk (VaR).

---

## Project Tiles

| Tile | Details |
| --- | --- |
| `📌 Project Title` | **AlphaPulse: Portfolio Risk Analytics Dashboard** |
| `🎯 Focus Area` | Portfolio analytics, financial risk measurement, and dashboard storytelling |
| `👥 End Goal` | Help users understand portfolio behavior, concentration risk, and downside exposure through clean data outputs and interactive visuals |
| `📊 Output Style` | CSV analytics outputs + Tableau dashboards + dashboard preview images |
| `🚧 Project State` | Completed, with the analytics pipeline, outputs, and dashboards finalized |

---

## `🧭 Project Overview`

AlphaPulse is a financial analytics project built to evaluate how a multi-asset portfolio behaves over time. The project pulls historical market data, cleans it, calculates daily log returns, measures rolling volatility, studies asset correlation, estimates portfolio risk, and simulates future outcomes using Monte Carlo methods.

The final outputs are turned into Tableau dashboards so the analysis is not only technically correct, but also easy to present and interpret. This makes the project useful both as an analytics workflow and as a business-facing dashboard portfolio piece.

---

## `❗ Problem Statement`

Investors and analysts often struggle with three common questions:

1. How is the portfolio performing on a risk-adjusted basis?
2. Which assets are driving diversification or concentration risk?
3. What could happen to the portfolio under uncertainty over the next year?

Raw price data alone cannot answer these questions clearly. Without a structured pipeline, it becomes difficult to convert market data into meaningful, presentation-ready risk insights.

---

## `✅ Solution Approach`

AlphaPulse solves this by creating an end-to-end portfolio risk analysis workflow:

1. Fetch historical adjusted close prices using Python.
2. Clean and standardize the dataset for reliable analysis.
3. Compute daily log returns, covariance, correlation, and rolling volatility.
4. Generate portfolio-level summary metrics and downside risk measures.
5. Run Monte Carlo simulations to forecast possible terminal portfolio values.
6. Export results into structured CSV files for dashboarding.
7. Visualize the story in Tableau dashboards for executive and analytical use.

---

## `🗓️ Week-Wise Project Journey`

### `📅 Week 1: Data Collection and Cleaning`

- Selected portfolio assets and defined the analysis scope.
- Fetched historical adjusted close price data using `yfinance`.
- Built the raw data pipeline and saved the dataset in the `data/` folder.
- Cleaned missing values and standardized the price data for downstream analysis.

### `📅 Week 2: Return and Risk Analytics`

- Calculated daily log returns for all active assets.
- Built rolling 30-day volatility analysis for both assets and the portfolio.
- Generated covariance and correlation matrices to understand asset relationships.
- Created portfolio summary outputs to capture core performance and risk statistics.

### `📅 Week 3: Monte Carlo Simulation and VaR`

- Implemented a Monte Carlo engine for portfolio risk forecasting.
- Simulated `10,000` one-year portfolio paths using historical return behavior.
- Estimated terminal value distribution and calculated `95% VaR`.
- Exported simulation outputs for dashboard-ready analysis.

### `📅 Week 4: Dashboard Design and Storytelling`

- Packaged analytics outputs into Tableau-friendly datasets.
- Built three dashboards focused on diversification, executive summary, and Monte Carlo risk forecast.
- Added visual storytelling layers to make risk insights easier to interpret.
- Organized the project repository and documentation for GitHub presentation.

---

## `🧱 Project Structure`

```text
AlphaPulse-Portfolio-Risk-Analytics/
|
|-- data/
|   |-- raw_data.csv
|   `-- cleaned_data.csv
|
|-- python/
|   |-- data_fetcher.py
|   |-- data_cleaner.py
|   |-- returns_calculator.py
|   |-- volatility.py
|   |-- correlation.py
|   |-- portfolio_metrics.py
|   |-- monte_carlo.py
|   `-- main.py
|
|-- output/
|   |-- daily_log_returns.csv
|   |-- covariance_matrix.csv
|   |-- correlation_matrix.csv
|   |-- correlation_heatmap_data.csv
|   |-- rolling_30d_volatility_assets.csv
|   |-- rolling_30d_volatility_portfolio.csv
|   |-- portfolio_summary.csv
|   |-- monte_carlo_terminal_distribution.csv
|   `-- var_95.csv
|
|-- dashboards/
|   |-- AlphaPulse - Portfolio Diversification Analysis.twbx
|   |-- AlphaPulse – Monte Carlo Risk Forecast.twbx
|   `-- AlphaPulse_Executive_Risk_Summary.twbx
|
|-- Executive Risk Summary.png
|-- Monte Carlo Situation.png
|-- Portfolio Diversification Map.png
|-- .gitignore
`-- README.md
```

---

## `▶️ How to Run This Project`

If someone wants to copy this repository and run the project locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/chiragchavda05-data/AlphaPulse-Portfolio-Risk-Analytics
```

2. Move into the project folder:

```bash
cd AlphaPulse-Portfolio-Risk-Analytics
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment:

```bash
.venv\Scripts\activate
```

5. Install the required libraries:

```bash
pip install pandas numpy yfinance
```

6. Run the full analytics pipeline:

```bash
python python/main.py
```

7. Check generated results inside:

- `data/`
- `output/`
- `dashboards/`

To explore the visual layer, open the Tableau dashboard files from the `dashboards/` folder.

---

## `🛠️ Tools and Technologies`

| Icon | Tool / Tech | Purpose |
| --- | --- | --- |
| `🐍` | Python | Core analytics and pipeline orchestration |
| `🧮` | NumPy | Numerical computations and simulation logic |
| `🐼` | Pandas | Data cleaning, transformation, and CSV export |
| `📈` | yfinance | Historical market data collection |
| `📊` | Tableau | Dashboard building and insight presentation |
| `🗂️` | CSV Files | Intermediate and final analytical outputs |
| `🧾` | Excel | Data review and supporting preparation |
| `💻` | VS Code | Development environment |
| `🔧` | Git & GitHub | Version control and project publishing |

---

## `🔍 Key Insights Generated`

- Portfolio performance can be evaluated beyond simple price movement by using daily log returns and summary metrics.
- Rolling volatility helps identify periods of rising or falling portfolio risk over time.
- Correlation analysis reveals whether assets are actually diversifying the portfolio or moving together.
- Monte Carlo simulation provides a probability-based view of future portfolio outcomes rather than a single-point forecast.
- `95% VaR` gives a practical estimate of downside exposure under adverse market conditions.
- Dashboard-based presentation makes technical risk metrics easier for non-technical stakeholders to understand.

---

## `🚀 How the Project Works`

The pipeline starts in `python/main.py`, which coordinates the complete workflow:

1. Fetch raw historical data.
2. Clean the dataset.
3. Calculate daily log returns.
4. Generate covariance, correlation, and portfolio summary metrics.
5. Run Monte Carlo simulations.
6. Compute `95% VaR`.
7. Export all outputs to the `output/` folder.
8. Use the exported data inside Tableau dashboards.

Run the project with:

```bash
python python/main.py
```

---

## `📌 Key Dashboard Deliverables`

| Icon | Dashboard | Focus |
| --- | --- | --- |
| `🧭` | Portfolio Diversification Analysis | Asset relationships, diversification view, and concentration understanding |
| `⚠️` | Monte Carlo Risk Forecast | Future distribution of portfolio value and downside scenarios |
| `📋` | Executive Risk Summary | High-level summary for quick stakeholder review |

---

## `📈 Project Status`

This project is now **completed** and ready for portfolio presentation, GitHub showcase, and local execution.

Completed deliverables:

- Core Python analytics pipeline
- Data cleaning and return calculations
- Volatility, covariance, and correlation analysis
- Monte Carlo simulation and `95% VaR`
- Tableau dashboards
- CSV export structure for visualization

The repository now contains the full workflow from market data collection to dashboard-ready outputs.

---

## `👤 Author`

| Tile | Details |
| --- | --- |
| `🧑 Name` | **Chirag Chavda** |
| `🏷️ Role` | Data Analytics / Portfolio Risk Analytics Project Builder |
| `📚 Project Type` | Finance + Python + Tableau Portfolio Project |
