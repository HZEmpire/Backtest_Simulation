"""
data_generator.py
-----------------
This script generates synthetic market data for prices, volumes, and timestamps,
and saves the data to a CSV file.
"""

import pandas as pd
import numpy as np
import datetime
import os

def generate_synthetic_data(
    start_time: str = "2023-01-01 09:30:00",
    periods: int = 60,
    freq: str = "1T",
    initial_price: float = 100.0,
    price_volatility: float = 1.0,
    volume_mean: float = 1000.0,
    random_seed: int = 42,
    output_path: str = "./result/synthetic_data.csv"
) -> pd.DataFrame:
    """
    Generate synthetic time-series market data for a single trading day (or period).
    Then save the generated data to a CSV file at output_path.
    
    :param start_time: The starting timestamp string (YYYY-MM-DD HH:MM:SS).
    :param periods: Number of data points to generate.
    :param freq: Frequency between data points (e.g., '1T' for 1 minute).
    :param initial_price: Starting price for the random walk.
    :param price_volatility: Controls the standard deviation of price changes.
    :param volume_mean: Average trading volume (per time interval).
    :param random_seed: Seed for reproducible random results.
    :param output_path: File path to save the synthetic data in CSV format.
    :return: DataFrame with columns [timestamp, price, volume].
    """
    # Ensure the result folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    np.random.seed(random_seed)
    
    # Generate a range of timestamps
    timestamp_index = pd.date_range(start=start_time, periods=periods, freq=freq)
    
    # Create a simple random walk for price
    price_changes = np.random.normal(loc=0, scale=price_volatility, size=periods)
    prices = [initial_price]
    for change in price_changes:
        next_price = prices[-1] + change
        prices.append(max(1.0, next_price))  # Ensuring price stays above 0
    prices = prices[1:]  # Drop the initial seed value
    
    # Generate volumes around a mean with some random variation
    volumes = np.random.poisson(lam=volume_mean, size=periods)
    
    data = pd.DataFrame({
        "timestamp": timestamp_index,
        "price": prices,
        "volume": volumes
    })
    
    # Save generated data to CSV
    data.to_csv(output_path, index=False)
    
    return data
