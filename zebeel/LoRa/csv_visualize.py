

import pandas as pd
import matplotlib.pyplot as plt

def visualize_data(csv_file):
    df = pd.read_csv(csv_file)
    df['Mesafe (cm)'] = pd.to_numeric(df['Mesafe (cm)'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['Zaman Damgası'], df['Mesafe (cm)'], marker='o', label='Mesafe')
    plt.xlabel('Zaman Damgası')
    plt.ylabel('Mesafe (cm)')
    plt.title('Zaman ile Mesafe')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

visualize_data("data_log.csv")
