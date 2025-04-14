from typing import Iterator
import csv
import ast
import plotly.graph_objects as go


def main():
    min_number = 4
    file_path = "Load_survey_data\\primary_use_cases.csv"
    
    rows = parse_csv(file_path)
    values = get_values(rows)
    sd = sort_dict(count_values(values))
    create_bar_plot(sd, min_number, file_path)


def parse_csv(file_name: str) -> Iterator:
    """
    Parses a CSV file and returns an iterator for each row. 
    
    Args:
        file_name (str): Name of the filepath

    Returns:
        Iterator: Each iteration returns a row of the CSV file
    """
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            yield row

    
def get_values(rows: list) -> Iterator:
    """
    Gets the values of each row and returns each value as an iterator

    Args:
        rows (list): List with element of rows where the last element of each list is the relevant data

    Returns:
        Iterator: Returns an iterator for each value of the row 
    """

    for row in rows:
        value = row[-1].strip()
        try:
            value_list = ast.literal_eval(value)
        except ValueError:
            value_list = [row[-1]]
        for item in value_list:
            yield item


def count_values(values) -> dict:
    """
    Evaluates the number of appearances of each load and saves it to a dict
    
    Args:
        values: Value which should be counted 

    Returns: 
        dict: Dict with load as key and count as value
    """
    value_dict = {}
    for value in values:
        if value in value_dict:
            value_dict[value] += 1
        else:
            value_dict[value] = 1
    value_dict.pop("nan")
    return value_dict


def sort_dict(load_stats: dict) -> dict:
    """
    Sorts the dict by descending order of the values.

    Args:
        load_stats (dict): Dict which should be sorted

    Returns:
        dict: Sorted dict
    """
    sorted_dict = dict(sorted(load_stats.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict


def create_bar_plot(sorted_dict: dict, min: int, file_link: str):
    """
    Creates a bar plot from a dict

    Args:
        sorted_dict(dict): Sorted dict with load as key and count as value
        min (int): Minimum percentage value which should be included in the plot. All lower values are truncated.
        file_link (str): Name of the file path
    """
    normalized_dict = {key: (value / 500) * 100 for key, value in sorted_dict.items()}
    filtered_dict = {key: value for key, value in normalized_dict.items() if value >= min}
    fig = go.Figure(data=[go.Bar(x=list(filtered_dict.keys()), y=list(filtered_dict.values()))])

    fig.update_layout(
        title = "Share of Households per Load",
        xaxis_title = "Name of Load",
        yaxis_title = "Percentage of Users",
        yaxis = dict(range=[0,100]) 
    )

    file_link_new = file_link[:len(file_link)-4] + ".html"
    
    try:
        fig.show()
        fig.write_html(file_link_new)
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