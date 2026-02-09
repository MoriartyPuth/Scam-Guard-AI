import pandas as pd
import numpy as np

def generate_live_data(n=100):
    np.random.seed(42)
    data = {
        'tx_id': range(1000, 1000+n),
        'sender': np.random.randint(100, 160, n),
        'receiver': np.random.randint(200, 260, n),
        'amount': np.random.uniform(50, 10000, n),
        'time_gap_seconds': np.random.randint(1, 10000, n),
        'is_scam': np.random.choice([0, 1], size=n, p=[0.9, 0.1])
    }
    df = pd.DataFrame(data)
    
    # Inject a known Laundering Cycle for the demo
    # 999 -> 888 -> 777 -> 999
    cycle_data = [
        [5000, 999, 888, 5000, 10, 1],
        [5001, 888, 777, 4900, 12, 1],
        [5002, 777, 999, 4850, 8, 1]
    ]
    df_cycle = pd.DataFrame(cycle_data, columns=['tx_id', 'sender', 'receiver', 'amount', 'time_gap_seconds', 'is_scam'])
    return pd.concat([df, df_cycle], ignore_index=True)