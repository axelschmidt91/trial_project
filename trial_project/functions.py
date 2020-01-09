from tkinter import *
from tkinter import filedialog
from pathlib import Path
import numpy as np
import statistics
import matplotlib.pyplot as plt
import os
from scipy import signal
from scipy.fftpack import fft
from file_handler import *

"""Module for several functions"""


def get_folder_name(file_name):
    """Extracts the name of a trial from the foldername. From format: YYYY_MM_DD_hh_mm_ss_'folder_name'
    
    :param file_name: path str or list of path str of file/s 
    :type file_name: list,str
    :return: type depending on argument type. Extracted trial names of folder/s
    :rtype: list, str
    """    
    if isinstance(file_name, list):
        folder_name = list()

        for name in file_name:

            temp = name.rsplit('\\')
            temp = temp[-2][20:]

            folder_name.append(temp)

        return folder_name
    elif isinstance(file_name, str):
        temp = file_name.rsplit('\\')
        folder_name = temp[-2][20:]

        return folder_name
    else:
        print("No valid file type. 'list' or 'str' are valid")


def show_time_before_after_width_data(output):
    pass


def compute_fft(data):
    # Number of sample points
    number_sample_points = data.shape[0]

    # sample spacing
    T = np.mean(np.diff(data[:, 0]))
    print('sample spacing: ' + str(T))

    # calculate Fourier frequencies
    yf_in = fft(data[:, 1])
    yf_out = fft(data[:, 2])

    print(yf_out)

    # set x axis frequency values
    xf = np.linspace(0.0, 1.0 / (2.0 * T), number_sample_points // 2)

    # plot diagramms
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    # ax1.plot(xf, 2.0 / number_sample_points * np.abs(yf_in[0:number_sample_points // 2]))
    ax1.semilogy(xf, 2.0 / number_sample_points *
                 np.abs(yf_in[0:number_sample_points // 2]))
    # ax2.plot(xf, 2.0 / number_sample_points * np.abs(yf_out[0:number_sample_points // 2]))
    ax2.semilogy(xf, 2.0 / number_sample_points *
                 np.abs(yf_out[0:number_sample_points // 2]))

    plt.grid()
    plt.show()

    return yf_in, yf_out


def filter_data(data, filter_type='lowpass', filter_frequence=1):

    signalc = data

    # first parameter is signal order and the second one refers to frequency limit. I set limit 30 so that I can see
    # only below 30 frequency signal component
    b, a = signal.butter(5, 30, btype='low', analog=True)
    output = signal.filtfilt(b, a, signalc)
    plt.plot(output)

    return output


def write_mean_std_file(folder, mean_std, folder_name):

    np.set_printoptions(formatter={'float_kind': '{:f}'.format})
    mean_std = np.around(mean_std, decimals=3, )

    str_data = 'Trial name\tInput mean\tInput std\tOutput mean\tOutput std'

    for row in range(len(mean_std)):

        str_data = '\n'.join([str_data, str(folder_name[row])])

        for cell in mean_std[row]:
            str_data = '\t'.join([str_data, str(cell)])

    print(str_data)
    # str_data = '\n'.join('\t'.join(str(cell) for cell in row) for row in mean_std)

    folder = Path(folder)
    output_file_name = folder / 'mean_std_values'

    output_file = open(output_file_name, 'w+')
    output_file.write(str_data)
    output_file.close()

    pass


def mean_std_file(element):
    mean_std = np.zeros((1, 4))

    mean_std[0, 0] = np.mean(element[:, 1])
    mean_std[0, 1] = np.std(element[:, 1])
    mean_std[0, 2] = np.mean(element[:, 2])
    mean_std[0, 3] = np.std(element[:, 2])

    return mean_std


def time_in_out_width_file(data):
    print('write time, before and after width in file')
    output = np.zeros((data.shape[0], 3))
    output[:, 0] = data[:, 0]
    output[:, 1] = data[:, 4]
    output[:, 2] = data[:, 2]

    np.set_printoptions(formatter={'float_kind': '{:f}'.format})
    output = np.around(output, decimals=3)

    return output


def import_pre_process(file_path):
    """imports from `file_path` and converts input into a numpy array.
    
    :param file_path: complete string to file location that should be loaded. Necassary
    :type file_path: str
    :return: ndarray (2D) with the data in the input file. Each row is a meassurement point.
    :rtype: ndarray
    """
    lines = np.loadtxt(file_path, dtype=str, comments="#",
                       delimiter="\t", unpack=False)

    for row in range(len(lines)):
        for col in range(len(lines[row])):
            lines[row][col] = float(lines[row][col].replace(',', '.'))

    data = np.asarray(lines.astype(np.float))

    data[:, 0] = data[:, 0] - np.ones(data[:, 0].shape) * data[0, 0]
    data = np.around(data, decimals=3)
    np.set_printoptions(formatter={'float_kind': '{:f}'.format})

    return data


def reduction(data, reduced_factor, red_type='mean'):
    """Reduce the data by every the `reduced_factor`
    
    :param data: which should be converted
        (Necessary)
    :type data: ndarray
    :param reduced_factor: How many rows (measurement points) should be computed together
    :type reduced_factor: int
    :param red_type: Type by which the reduction should be done.
        Available:
            'max': returns the max value of the `reduced_factor` compared measurement points.
            'min': returns the min value of the `reduced_factor` compared measurement points.
            'mean': returns the mean value of the `reduced_factor` compared measurement points., defaults to 'mean'
    :type red_type: str, optional
    :raises ValueError: if no valid 'red_type' was choosen, a ValueError will be raised.
    :return: reduced Data
    :rtype: ndarray
    """
    print('reduction type: ' + red_type)
    print('Reduce Data')
    step_size = reduced_factor
    reduced_data = np.zeros(
        (int(np.ceil(len(data) / step_size)), len(data[0])))
    reduced_index = np.arange(0, len(reduced_data))

    for jump in reduced_index:
        col_means = []
        analyzing_data = np.transpose(
            data[jump * step_size:(jump + 1) * step_size])
        for col in range(len(data[jump])):
            if red_type == 'mean':
                col_means.append(np.around(statistics.mean(
                    analyzing_data[col]), decimals=3))
            elif red_type == 'max':
                col_means.append(
                    np.around(max(analyzing_data[col]), decimals=3))
            elif red_type == 'min':
                col_means.append(
                    np.around(min(analyzing_data[col]), decimals=3))
            else:
                raise ValueError(
                    "reduction type option must be one of 'mean', 'max', 'min'")
        reduced_data[jump] = np.asarray(col_means)

    print('Setting Time')
    reduced_data[:, 0] = reduced_data[:, 0] - \
        np.ones(reduced_data[:, 0].shape) * reduced_data[0, 0]
    np.set_printoptions(suppress=False, formatter={
                        'float_kind': '{:f}'.format})
    reduced_data = np.around(reduced_data, decimals=3)

    return reduced_data


def save_to_file(reduced_data, file_path, appendix='_new'):

    print('Output Data')
    str_data = '\n'.join('\t'.join(str(cell) for cell in row)
                         for row in reduced_data)

    output_file_name = file_path + appendix

    output_file = open(output_file_name, 'w+')
    output_file.write(str_data)
    output_file.close()

    print('calculation done.')

    pass


def show_reduced_data(data, reduced_data):

    plt.figure(1)
    plt.subplot(211)
    plt.plot(data[:, 0], data[:, 2])
    plt.plot(data[:, 0], data[:, 4])
    plt.xlabel('Time')
    plt.ylabel('width')
    plt.title('input/original data')

    plt.subplot(212)
    plt.plot(reduced_data[:, 0], reduced_data[:, 2])
    plt.plot(reduced_data[:, 0], reduced_data[:, 4])
    plt.xlabel('Time')
    plt.ylabel('width')
    plt.title('reduced data')
    pass
