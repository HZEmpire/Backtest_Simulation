"""
strategy.py
-----------
This script holds the basic TWAP strategy logic for order slicing.
"""

import pandas as pd

class TWAPStrategy:
    """
    A simple Time-Weighted Average Price (TWAP) strategy implementation.
    
    The strategy divides the total order size equally over the entire time window.
    """
    def __init__(self, total_order_quantity: float, start_index: int, end_index: int):
        """
        :param total_order_quantity: Total quantity of the order to be executed.
        :param start_index: Data index (row) at which the strategy starts execution.
        :param end_index: Data index (row) at which the strategy finishes execution.
        """
        self.total_order_quantity = total_order_quantity
        self.start_index = start_index
        self.end_index = end_index
        
    def generate_orders(self, market_data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate order schedule based on TWAP principle. Each time slice gets an equal share.
        
        :param market_data: DataFrame that includes at least an index or a timestamp for referencing.
        :return: DataFrame with an 'order_quantity' column indicating how many units are traded at each index.
        """
        n_slices = (self.end_index - self.start_index) + 1
        qty_per_slice = self.total_order_quantity / n_slices if n_slices > 0 else 0
        
        # Create a copy to store the order quantity
        df_orders = market_data.copy()
        df_orders['order_quantity'] = 0.0
        
        # Assign equal quantity to each time slice between start_index and end_index
        for idx in range(self.start_index, self.end_index + 1):
            df_orders.at[idx, 'order_quantity'] = qty_per_slice
        
        return df_orders
