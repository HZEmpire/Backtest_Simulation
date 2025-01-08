"""
backtest.py
-----------
This script defines the backtesting environment, simulates order executions,
and calculates performance metrics such as execution cost, slippage, and fill rate.
"""

import pandas as pd
import numpy as np

class Backtester:
    """
    A simple backtesting framework that executes a given strategy on synthetic market data
    and calculates relevant performance metrics.
    """
    def __init__(self, market_data: pd.DataFrame, slippage_factor: float = 0.001):
        """
        :param market_data: DataFrame that must include columns: ['timestamp', 'price', 'volume']
        :param slippage_factor: Proportion of the current price used to simulate slippage cost.
        """
        self.market_data = market_data.copy()
        self.slippage_factor = slippage_factor

        # Initialize additional columns for storing execution info
        self.market_data['executed_quantity'] = 0.0
        self.market_data['executed_price'] = np.nan
        self.market_data['expected_price'] = np.nan

    def run(self, df_orders: pd.DataFrame) -> pd.DataFrame:
        """
        Execute orders in a simplified manner:
        - The 'expected_price' is considered the current 'price' in the data.
        - The 'executed_price' includes a slippage factor above/below the price.
        - If there's enough volume, the order is fully filled at that price; otherwise partial.
        
        :param df_orders: DataFrame with 'order_quantity' for each row.
        :return: DataFrame with additional columns for execution details.
        """
        # Assume a buy scenario, so slippage means paying slightly more than the current price.
        for idx, row in df_orders.iterrows():
            order_qty = row['order_quantity']
            
            if order_qty > 0:
                # Simplify fill logic: fill the entire order if market volume is sufficient
                market_volume = self.market_data.at[idx, 'volume']
                possible_fill = min(order_qty, market_volume)

                # Record the expected and executed prices
                self.market_data.at[idx, 'expected_price'] = self.market_data.at[idx, 'price']
                # Apply slippage: executed_price = price * (1 + slippage_factor)
                executed_p = self.market_data.at[idx, 'price'] * (1 + self.slippage_factor)
                self.market_data.at[idx, 'executed_price'] = executed_p

                self.market_data.at[idx, 'executed_quantity'] = possible_fill

        return self.market_data

    def calculate_metrics(self, benchmark_type: str = 'VWAP') -> dict:
        """
        Calculate relevant performance metrics including:
        1. Execution Cost (comparing executed price to a benchmark price)
        2. Slippage (difference between expected price and executed price)
        3. Fill Rate (total filled quantity / total ordered quantity)
        
        :param benchmark_type: 'VWAP' or 'avg_price' to set the benchmark for execution cost.
        :return: A dictionary of metric results.
        """
        executed_rows = self.market_data.dropna(subset=['executed_price'])
        executed_rows = executed_rows[executed_rows['executed_quantity'] > 0]

        if executed_rows.empty:
            return {
                'execution_cost': None,
                'slippage': None,
                'fill_rate': 0.0
            }
        
        total_executed_quantity = executed_rows['executed_quantity'].sum()
        
        # Calculate fill rate
        total_order_quantity = self.market_data['order_quantity'].sum()
        fill_rate = total_executed_quantity / total_order_quantity if total_order_quantity > 0 else 0.0

        # Prepare benchmark
        if benchmark_type.upper() == 'VWAP':
            # Weighted by actual volume in the entire data
            vwap = (self.market_data['price'] * self.market_data['volume']).sum() / self.market_data['volume'].sum()
            benchmark_price = vwap
        else:
            # Use average price as a simpler approach
            benchmark_price = self.market_data['price'].mean()

        # Execution cost: difference between avg executed price and benchmark
        exec_value = (executed_rows['executed_price'] * executed_rows['executed_quantity']).sum()
        avg_exec_price = exec_value / total_executed_quantity
        execution_cost = avg_exec_price - benchmark_price

        # Slippage: difference between expected and executed price
        expected_value = (executed_rows['expected_price'] * executed_rows['executed_quantity']).sum()
        avg_expected_price = expected_value / total_executed_quantity
        slippage = avg_exec_price - avg_expected_price
        
        metrics = {
            'execution_cost': execution_cost,
            'slippage': slippage,
            'fill_rate': fill_rate
        }
        return metrics
