import matplotlib.pyplot as plt
import pandas as pd


# TODO: First implementation, maybe convert to class or change some details in methods / functions
def get_results(results_file: str, separator: str = '') -> pd.DataFrame:
    data = pd.read_csv(results_file, sep=separator)
    return data


def handle_data(data: pd.DataFrame) -> (pd.DataFrame.values,
                                        pd.DataFrame.values):
    delay_time = data['t_delay'].values
    total_time = data['t_total'].values
    trigger_time = data['t_trigger'].values
    number_of_points = data['n_points'].values  # TODO: Check definition of this variable
    # TODO: Definition of efficiency may change.
    efficiency = total_time / (number_of_points * trigger_time)

    return efficiency, delay_time


# TODO: How we want visualize results and how experiment looks like
def plot_results(data: pd.DataFrame, scale: str = None) -> None:
    efficiency, delay_time = handle_data(data)
    plt.plot(delay_time, efficiency)
    plt.title('C++ vs Python efficiency')
    if scale == 'log':
        plt.yscale('log')
    plt.xlabel('Time of delay [s]')
    plt.legend(loc='upper right')
    plt.ylabel('Efficiency [%]')

    return


def get_joined_results(save_path: str = None):
    for language in ['cpp', 'python']:
        data = get_results(language)
        plot_results(data)
    plt.savefig(save_path)
    return


def main():
    get_joined_results('')
    return


if __name__ == "__main__":
    main()
