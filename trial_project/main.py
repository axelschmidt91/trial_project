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
from functions import *
from tqdm import tqdm


def main():
    folder = open_folder_dialog()

    file_name = scan_folder(folder, "_camera")

    # print(fileName)

    reduction_factor = 3
    mean_std = np.zeros((len(file_name), 4))

    i = 0
    for file in tqdm(file_name):

        print(file)
        data = import_pre_process(file)

        red_type = 'mean'
        # reduced_data = reduction(data, reduction_factor, red_type='min')
        # reduced_data = reduction(reduced_data, reduction_factor, red_type='max')

        # reduced_data = reduction(data, reduction_factor, red_type=red_type)

        '''Save reduced data in file'''
        output_appendix = '_reduced_by_ratio_' + \
            str(reduction_factor) + '_' + red_type
        # save_to_file(reduced_data, file, output_appendix)

        '''Calculate and Save Time, Input, Output data in file'''
        output = time_in_out_width_file(data)
        # output = time_in_out_width_file(reduced_data)

        # save_to_file(output, file, appendix='_inout_for_graph')

        # tf_in, tf_out = compute_fft(output_standard)

        '''Calculate the mean and std of input and output'''
        mean_std[i, :] = mean_std_file(output)

        # show_reduced_data(data, reduced_data)
        # show_time_before_after_width_data(output)
        i += 1


    folder_name = get_folder_name(file_name)
    write_mean_std_file(folder, mean_std, folder_name)


if __name__ == '__main__':
    main()
