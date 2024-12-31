import time

def measure_performance(iterrows_func, alternative_func, df, num_runs=1):
    """
    Generic function to compare performance between an iterrows implementation
    and its alternative.

    Args:
        iterrows_func: Function that uses iterrows
        alternative_func: Function that uses an alternative to iterrows
        df: DataFrame to test with
        num_runs: Number of times to run each version
    """
    print(f"DataFrame shape: {df.shape}")

    # Test iterrows version
    print("\nTesting iterrows version...")
    iterrows_times = []
    for _ in range(num_runs):
        start_time = time.time()
        iterrows_func(df.copy())
        iterrows_times.append(time.time() - start_time)
    avg_iterrows_time = sum(iterrows_times) / len(iterrows_times)

    # Test alternative version
    print("\nTesting alternative version...")
    alt_times = []
    for _ in range(num_runs):
        start_time = time.time()
        alternative_func(df.copy())
        alt_times.append(time.time() - start_time)
    avg_alt_time = sum(alt_times) / len(alt_times)

    # Print results
    print(f"\nResults:")
    print(f"iterrows version average time: {avg_iterrows_time:.4f} seconds")
    print(f"Alternative version average time: {avg_alt_time:.4f} seconds")
    print(f"Speedup factor: {avg_iterrows_time/avg_alt_time:.2f}x")

# Example usage:
"""
def my_iterrows_version(df):
    # Your iterrows code here
    pass

def my_alternative_version(df):
    # Your alternative code here
    pass

# Test the functions
measure_performance(my_iterrows_version, my_alternative_version, your_dataframe)
"""

import pandas as pd
import numpy as np

# Create test data
n_rows = 1_000_000
game_types = ['Sports Betting']
df = pd.DataFrame({
    'game_type': np.random.choice(game_types, size=n_rows),
    'bet_amount': np.random.lognormal(mean=3, sigma=1, size=n_rows),
    'win_loss': np.random.choice([-1, 1], size=n_rows, p=[0.55, 0.45])
})
df['winnings'] = df['bet_amount'] * df['win_loss']

def iterrows_version(df):
  # Calculate statistics using iterrows
  game_stats = {}
  for _, row in df.iterrows():
      game_type = row['game_type']
      if game_type not in game_stats:
          game_stats[game_type] = {
              'total_bets': 0,
              'total_winnings': 0,
              'win_count': 0,
              'count': 0
          }

      game_stats[game_type]['total_bets'] += row['bet_amount']
      game_stats[game_type]['total_winnings'] += row['winnings']
      game_stats[game_type]['win_count'] += 1 if row['win_loss'] > 0 else 0
      game_stats[game_type]['count'] += 1

def alternative_version(df):
  # Calculate statistics using groupby
  stats = df.groupby('game_type').agg({
      'bet_amount': ['sum', 'mean'],
      'winnings': 'sum',
      'win_loss': lambda x: (x > 0).mean() * 100
  }).round(2)

measure_performance(iterrows_version, alternative_version, df)
