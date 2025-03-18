import matplotlib.pyplot as plt
import pandas as pd

header_rows = 12
file_link = "Oszi_data\\20250317_Inrush_Current_AC_Load.csv"

def load_data(file: str):
    df = pd.read_csv(file, skiprows=header_rows, names=['Timestamp1', 'Voltage 1', 'Voltage 2', 'Current', 'Timestamp2', 'MATH'])

    # Downsample by selecting every 1000th row
    df_downsampled = df.iloc[::1000]
    
    # Downsample by grouping and aggregating
    df_downsampled = df.groupby(pd.cut(df.index, 100000)).mean()
    
    return df_downsampled


def plot_data(data: pd.core.frame.DataFrame):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    data.plot(x = 'Timestamp1', y = 'Current', ax = ax1, label = 'Current', color = 'blue')
    data.plot(x = 'Timestamp1', y = 'MATH', ax = ax2, label = 'CH1 - CH2', color = 'red')
    ax1.set_xlabel('Time in us')
    ax1.set_ylabel('Current in A')
    ax2.set_ylabel('Voltage in V')
    plt.title('Inrush current plot')
    plt.legend()
    plt.show()


data = load_data(file_link)
plot_data(data)