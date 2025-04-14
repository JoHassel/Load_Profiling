import pandas as pd
import os
from typing import List
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def main():
    header_rows = 12
    dir = ".\\Osci_data_diff_probe"
    downsample_rate = 10
    avg_size = 50
    call_counter = 0
    
    
    filepaths = get_filepaths(dir)
    expected_counts = len(filepaths)
    print(f"Found {expected_counts} CSV files. Plotting to HTML files now...")
    for filepath in filepaths:
        data = load_data(filepath, downsample_rate, avg_size, header_rows)
        call_counter +=1
        save_plot_to_html(data, filepath, call_counter, expected_counts)

def get_filepaths(dir: str) -> List[str]:
    """
    Gets all filepaths of CSV files in the current directory.

    Args:
        dir (str): Path of the directory where to look for csv files

    Returns:
        List[str]: All filepaths of CSV files
    """
    all_filepaths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.splitext(filepath)[1] == ".csv":
                all_filepaths.append(filepath)
    return all_filepaths    


def load_data(filepath: str, downsample_rate: int, avg_size:int, header_rows: int,) -> pd.DataFrame:
    """
    Loads the data from a CSV file and downsamples it.
    
    Args:
        filepath (str): String with the file path
        downsample_rate (int): Rate by which is downsampled. 
        avg_size (int): Numbre of indexes which are grouped and averaged over
        header_rows (int): Number of header rows which should be skipped

    Returns:
        pd.DataFrame: Downsampled data from CSV file
    """
    df = pd.read_csv(filepath, skiprows=header_rows, names=['Timestamp', 'Voltage', 'Current'])

    def downsample(df: pd.DataFrame, downsample_rate: int) -> pd.DataFrame:
        """
        Downsamples the dataframe by a selected downsample rate.

        Args:
            df (pd.DataFrame): Original data from CSV file
            downsample_rate (int): Rate by which is downsampled. 
            avg_size (int): Numbre of indexes which are grouped and averaged over
        
        Returns:
            pd.DataFrame: Downsampled and averaged data from CSV file
        """
        df_downsampled = df.iloc[::downsample_rate]
        n_groups = df_downsampled.shape[0] / avg_size
        df_downsampled_grouped = df.groupby(pd.cut(df.index, int(n_groups)), observed=False).mean()
        return df_downsampled_grouped

    return downsample(df, downsample_rate)


def save_plot_to_html(data: pd.core.frame.DataFrame, file_link: str, call_counter: int, expected_counts: int):
    """
    Plots the data to a line plot and saves it to a html file.

    Args:
        data (pd.DataFrame): Data frame with to be plotted data
        file_link (str): String with the file path
        call_counter (int): Count of the function calls 
        expected_counts (int): Expected number of function calls
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=data['Timestamp'], y=data['Current'], name='Current'), secondary_y=False)
    fig.add_trace(go.Scatter(x=data['Timestamp'], y=data['Voltage'], name='Voltage'), secondary_y=True)

    current_axis_limit = max(abs(data['Current'])) * 1.1
    voltage_axis_limit = max(abs(data['Voltage'])) * 1.1

    fig.update_layout(
        title = os.path.basename(file_link),
        xaxis_title = "Time in s",
        yaxis_title = "Current in A",
        yaxis = dict(range=[-current_axis_limit, current_axis_limit]),
        yaxis2_title = "Voltage in V",
        yaxis2 = dict(overlaying='y', side='right', range=[-voltage_axis_limit,voltage_axis_limit])
    )

    file_link_new = file_link[:len(file_link)-4] + ".html"
    
    try:
        fig.write_html(file_link_new)
        print(f"{call_counter}/{expected_counts} done: Successfully saved plot as {file_link_new}")
    except FileNotFoundError:
        print("The directory does not exist.")
    except PermissionError:
        print("You do not have permission to write to this directory.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except NotADirectoryError:
        print("The parent directory does not exist.")
    except TypeError as e:
        print(f"A type error occurred: {e}")
    except ValueError as e:
        print(f"A value error occurred: {e}")


if __name__ == "__main__":
    main()