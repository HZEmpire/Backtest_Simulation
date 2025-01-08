# Strategy Backtesting Framework for Smart Order Routing (SOR)

Author: [Haozhou Xu](https://hzempire.github.io/)

This repository demonstrates a simplified backtesting framework for a Smart Order Router (SOR). The key components include:
- **data_generator.py**: Generates synthetic market data (price, volume, timestamps) and saves it to a CSV file.
- **strategy.py**: Implements a basic TWAP (Time-Weighted Average Price) strategy to slice orders over a specified time window.
- **backtest.py**: Defines a backtester class that simulates order execution and calculates performance metrics such as execution cost, slippage, and fill rate.
- **visualization.py**: Provides functions to visualize the price, volume, and executed quantities, and saves the plots.
- **main.py**: The main entry point that ties everything together.

## Folder Structure
```bash
├── data_generator.py 
├── strategy.py 
├── backtest.py 
├── visualization.py 
├── main.py 
├── result 
│ ├── synthetic_data.csv 
│ ├── executed_data.csv 
│ ├── price_over_time.png 
│ ├── volume_over_time.png 
│ └── executed_quantity.png 
├── requirements.txt
└── README.md
```


## Usage

1. Install the required Python packages via `pip install -r requirements.txt`.
2. Run `python main.py` to:
   - Generate synthetic data and save to `./result/synthetic_data.csv`.
   - Execute a TWAP strategy and produce `./result/executed_data.csv`.
   - Produce and save plots (`price_over_time.png`, `volume_over_time.png`, `executed_quantity.png`) in the `./result` folder.
   - Display execution metrics in the console.

## Key Files

1. **data_generator.py**  
   - `generate_synthetic_data()`: Creates a random walk for the price and Poisson-distributed volumes, saves them to a CSV.

2. **strategy.py**  
   - `TWAPStrategy`: Distributes a total order quantity equally over the specified time indices.

3. **backtest.py**  
   - `Backtester`: Simulates trades with a simplified fill mechanism and calculates execution metrics.

4. **visualization.py**  
   - `plot_and_save_results()`: Generates plots for price, volume, and executed quantities, saving them as PNG files.

5. **main.py**  
   - Orchestrates the entire workflow, from data generation to strategy execution and visualization.

## Extending the Framework

- **Multiple Strategies**: Add more strategy classes (e.g., VWAP, POV, or RL-based) in `strategy.py`.
- **Complex Execution Logic**: Enhance the fill simulation and partial fills in `Backtester`.
- **Additional Metrics**: Include metrics like price impact, realized PnL, or custom benchmarks.


