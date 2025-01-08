"""
visualization.py
----------------
This script provides functions to visualize price, volume, and executed orders.
It also saves the resulting plots to the ./result folder.
"""

import matplotlib.pyplot as plt
import os

def plot_and_save_results(market_data, executed_data, metrics, output_dir="./result"):
    """
    Create visualizations of:
      1. Price over time
      2. Volume over time
      3. Executed quantity
    And save plots as PNG files in the specified output_dir.
    
    :param market_data: Original market DataFrame.
    :param executed_data: Market DataFrame with execution columns.
    :param metrics: Dict containing 'execution_cost', 'slippage', 'fill_rate'.
    :param output_dir: Folder where plots will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Plot price over time
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(market_data['timestamp'], market_data['price'], label='Price', color='blue')
    ax1.set_title('Price Over Time')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Price')
    ax1.legend()
    plt.tight_layout()
    plot1_path = os.path.join(output_dir, "price_over_time.png")
    plt.savefig(plot1_path)
    plt.show()

    # 2. Plot volume over time
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.bar(market_data['timestamp'], market_data['volume'], label='Volume', color='orange')
    ax2.set_title('Volume Over Time')
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('Volume')
    ax2.legend()
    plt.tight_layout()
    plot2_path = os.path.join(output_dir, "volume_over_time.png")
    plt.savefig(plot2_path)
    plt.show()

    # 3. Plot executed quantity vs. time
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.bar(executed_data['timestamp'], executed_data['executed_quantity'], label='Executed Qty', color='green')
    ax3.set_title('Executed Quantity Over Time')
    ax3.set_xlabel('Timestamp')
    ax3.set_ylabel('Executed Quantity')
    ax3.legend()
    plt.tight_layout()
    plot3_path = os.path.join(output_dir, "executed_quantity.png")
    plt.savefig(plot3_path)
    plt.show()
    
    # Print metrics for clarity (also could be saved in a text file if needed)
    print("=== Performance Metrics ===")
    print(f"Execution Cost: {metrics['execution_cost']}")
    print(f"Slippage: {metrics['slippage']}")
    print(f"Fill Rate: {metrics['fill_rate']:.2%}")
