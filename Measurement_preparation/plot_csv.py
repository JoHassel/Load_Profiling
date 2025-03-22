import matplotlib.pyplot as plt
import pandas as pd
import mpld3

header_rows = 12
file_link = "Measurement_preparation\\Oszi_data\\20250319_Constant_Bench_Grinder.csv"

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

    line1, = ax1.plot(data['Timestamp1'], data['Current'], label='Current', color='blue')      
    line2, = ax2.plot(data['Timestamp1'], data['MATH'], label='Voltage', color='red')

    ax1.set_xlabel('Time in us')
    ax1.set_ylim((-2,2))
    ax2.set_ylim((-400,400))
    ax1.set_ylabel('Current in A')
    ax2.set_ylabel('Voltage in V')

    plt.title('Bench Grinder Permanent Voltage & Current')

    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels, loc='upper right')
    # plt.legend(loc = 'upper right')
    # plt.show()

    # Save the plot as an HTML file
    file_link_new = file_link[:len(file_link)-4] + ".html"
    mpld3.save_html(fig, file_link_new)

data = load_data(file_link)
plot_data(data)