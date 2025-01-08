"""
main.py
-------
This script ties together the data generator, strategy, backtester, and visualization.
It runs a basic TWAP strategy on synthetic market data, saves results to CSV, 
then creates and saves visualizations.
"""

import pandas as pd
import os

from data_generator import generate_synthetic_data
from strategy import TWAPStrategy
from backtest import Backtester
from visualization import plot_and_save_results

def main():
    """
    Main function that orchestrates:
    1. Data generation (saved to CSV)
    2. Strategy instantiation (TWAP)
    3. Running backtest
    4. Saving backtest results to CSV
    5. Visualization and saving plots
    """
    # 1. Generate synthetic market data and save to CSV
    market_data = generate_synthetic_data(
        start_time="2025-01-01 09:30:00",
        periods=60,
        freq="1T",
        initial_price=100.0,
        price_volatility=1.0,
        volume_mean=500,
        random_seed=123,
        output_path="./result/synthetic_data.csv"
    )
    
    # 2. Create a TWAP strategy instance
    #    Let's assume we want to execute a total of 3000 units from index=10 to index=50
    twap_strategy = TWAPStrategy(
        total_order_quantity=3000.0,
        start_index=10,
        end_index=50
    )
    
    # 3. Generate the order schedule
    df_orders = twap_strategy.generate_orders(market_data)
    
    # 4. Run the backtest
    backtester = Backtester(df_orders, slippage_factor=0.001)
    executed_data = backtester.run(df_orders)
    
    # 5. Calculate performance metrics
    metrics = backtester.calculate_metrics(benchmark_type='VWAP')
    
    # 6. Save executed data to CSV
    os.makedirs("./result", exist_ok=True)
    executed_csv_path = "./result/executed_data.csv"
    executed_data.to_csv(executed_csv_path, index=False)
    
    # 7. Visualization
    plot_and_save_results(market_data, executed_data, metrics, output_dir="./result")
    
if __name__ == "__main__":
    main()
