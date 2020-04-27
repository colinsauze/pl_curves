#!/usr/bin/env python3
"""
A program for graphing the evenness of bacterial communities using
Pareto-Lorenz curves of the relative abundance of a set of T-RFs against the
cumulative abundance of each T-RF. It also calculates the gini-coefficient of
these.

This implements the method described in the following papers:

https://www.nature.com/articles/ismej2010100
"Possible interactions between bacterial diversity, microbial activity and
supraglacial hydrology of cryoconite holes in Svalbard" by
Arwyn Edwards, Alexandre M Anesio, Sara M Rassner, Birgit Sattler,
Bryn Hubbard, William T Perkins, Michael Young & Gareth W Griffith
in The ISME Journal volume 5, pages 150-160 (2011)

and

https://doi.org/10.3389/fmicb.2016.00956
"Can the Bacterial Community of a High Arctic Glacier Surface Escape Viral
Control?" by Sara M. E. Rassner, Alexandre M. Anesio, Susan E. Girdwood,
Katherina Hell, Jarishma K. Gokul, David E. Whitworth and Arwyn Edwards
in Frontiers in Microbiology 21 June 2016

@author: Colin Sauze
"""


import sys
import argparse
import math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# note matplotlib.use('Agg') has to be done before any other matplotlib related
# stuff including importing pyplot. This sets the backend to make a PNG file.


def calculate_gini(data):
    '''calculates the gini coefficient.
    This code is based on:
    stackoverflow.com/questions/39512260/calculating-gini-coefficient-in-python-numpy/39513799

    Parameters
    ----------
    data
        the list of data to calculate the gini coefficient on

    Returns
    -------
    float64
        The gini coefficient for this data

    '''
    # (Warning: This is a concise implementation, but it is O(n**2)
    # in time and memory, where n = len(x).  *Don't* pass in huge
    # samples!)

    # don't attempt to compute an empty list, just return NaN instead
    if data.size == 0:
        return math.nan

    # Mean absolute difference
    mad = np.abs(np.subtract.outer(data, data)).mean()
    # Relative mean absolute difference
    rmad = mad / np.mean(data)
    # Gini coefficient
    gini = 0.5 * rmad
    return gini


def check_columns(dataframe):
    '''
    Checks all columns in the data frame sum to 1

    Parameters
    ----------
    dataframe
        The data frame to check

    Returns
    -------
    Bool
        False if a column doesn't sum to 1, True if they all do
    '''
    for col in dataframe.columns:
        total = sum(dataframe.loc[:, col])
        # print(col, "total=", total)
        if total < 0.9999 or total > 1.0001:
            # print("Error column ", col, "doesn't sum to 1.0")
            return False
    return True


def remove_zeros(dataframe):
    '''
    Removes all rows which contain only zeros

    Parameters
    ----------
    dataframe
        The data frame to check

    Returns
    -------
    pandas.core.frame.DataFrame
       The dataframe with all zero rows removed
    '''

    for row_index in dataframe.index:
        total = sum(dataframe.loc[row_index])
        if total == 0:
            # print("removing bin", row_index, "as its empty")
            dataframe = dataframe.drop(row_index)

    return dataframe


def sort_bins(dataframe):
    '''
    Sort each bin by its relative abundance

    Parameters
    ----------
    dataframe
        The data frame to check

    Returns
    -------
    list
        A list of dataframes, each dataframe contains a single sample
    '''

    # split each column into its own dataframe
    samples = []

    for col in dataframe.columns:

        # sort the bins in descending order, convert result to a new dataframe
        data = dataframe.loc[:, col].sort_values(ascending=False).to_frame()
        samples.append(data)
    return samples


def calculate_cumulative_relative_abundance(samples):
    '''
    calculates cumulative relative abundance

    Parameters
    ----------
    samples
        a list of dataframes

    Returns
    -------
    list
        a new list of dataframes, each one will have an additional column
        'cuml rel abund' with the cumulative relative abundance.
    '''

    samples2 = []
    for sample in samples:
        cum_rel_abund = []

        # calculate cumulative relative abundance and cumulative prop trfs
        for i in range(0, len(sample)):
            if i > 0:
                cum_rel_abund.append(sample.iloc[i][0] + cum_rel_abund[i - 1])
            else:
                cum_rel_abund.append(sample.iloc[i][0])

        sample['Cum Rel Abund'] = cum_rel_abund

        samples2.append(sample)

    return samples2


def calculate_cumulative_prop_trf(samples):
    '''
    calculates cumulative prop trf

    Parameters
    ----------
    samples
        A list of dataframes

    Returns
    -------
    list
        A new list of dataframes, each one will have an additional column
        'cum prop trfs' with the cumulative prop trfs.
    '''
    samples2 = []
    for sample in samples:
        cum_prop_trfs = []

        # calculate cumulative prop trfs
        for i in range(0, len(sample)):
            cum_prop_trfs.append((i + 1) / len(sample))

        sample['Cum Prop TRFs'] = cum_prop_trfs

        samples2.append(sample)

    return samples2


def remove_cumulative_abundance_over_one(samples):
    '''
    deletes all but the first item where cumulative abundance is greater than 1

    Parameters
    ----------
    samples
        A list of dataframes each dataframe should have 3 columns. One with the
        name of the step, Cum Prop TRFs and Cum Rel Abund.

    Returns
    -------
    list
        A modified version of the list with all but the first row where
        cumulative abundance is greater than 1.
    '''
    samples2 = []

    # get each sample in turn
    for col in samples:
        found = False
        new_frame = col

        # go through each row and check for values over 1
        for row_index in col.index:
            val = col["Cum Rel Abund"][row_index]
            # if we've already found the first row with a value of 1,
            # then start removing rows
            if found:
                # remove the row and save the resulting frame back to new_frame
                new_frame = new_frame.drop(row_index)
            # look for values over 1
            # floating point representation means it might not be exactly 1
            elif val > 0.999999:
                found = True
        # add the new reduced dataframe to a list to replace samples
        samples2.append(new_frame)

    return samples2


def make_graph(samples, filename):
    '''
    Makes a graph

    Parameters
    ----------
    samples
        A list of dataframes, each dataframe should contain 3 columns one with
        the name of the step, Cum Prop TRFs and Cum Rel Abund.
    filename
        Name of the file to save the graph to
    '''

    # the - prefix means a line will drawn
    # see https://matplotlib.org/api/markers_api.html for a list of markers
    markerlist = ["-+", "-,", "-o", "-*", "-.", "-^", "-<", "->", "-v"]

    # the list of markers to use, must be longer or equal to number of steps
    # check it really is
    assert len(markerlist) >= len(samples)

    # counter for going through the makerlist
    i = 0
    # make graph
    for col in samples:
        # get the title of current sample from the heading of its 1st column
        title = col.columns[0]

        plt.xlim(0, 1.0)
        plt.ylim(0, 1.05)

        plt.annotate("",
                     xy=(0, 0), xycoords='data',
                     xytext=(1, 1), textcoords='data',
                     arrowprops=dict(arrowstyle="-",
                                     connectionstyle="arc3,rad=0."), )

        # plot cumulative prop trfs vs cumulative relative abundance
        plt.plot(col.loc[:, 'Cum Prop TRFs'], col.loc[:, 'Cum Rel Abund'],
                 markerlist[i], label=title)
        plt.ylabel("Cumulative Relative Abundance")
        plt.xlabel("Cumulative Prop TRF")
        plt.grid()
        plt.legend()
        plt.savefig(filename)
        i = i + 1


def make_gini_file(samples, gini_file):
    '''
    Calculates the Gini coefficients and saves them to a TSV file

    Parameters
    ----------
    samples
        A list of dataframes, each dataframe should contain 3 columns one with
        the name of the step, Cum Prop TRFs and Cum Rel Abund.
    gini_file
        Name of the file to save the gini coefficient data to
    '''
    titles = []
    for col in samples:
        titles.append(col.columns[0])
    # make an empty data frame for the gini coefficients
    gini_dataframe = pd.DataFrame(columns=['Gini', 'Corrected Gini', 'n'],
                                  index=titles)

    # make graph
    for col in samples:
        # get the title of current sample from the heading of its 1st column
        title = col.columns[0]

        # calculate gini coefficient and corrected gini (g * (n/n-1))
        gini = calculate_gini(col.iloc[:, 0])
        corrected_gini = gini * (len(col) / (len(col) - 1))

        # add gini coefficients into a dataframe for saving the result
        gini_dataframe.loc[title, 'Gini'] = gini
        gini_dataframe.loc[title, 'Corrected Gini'] = corrected_gini
        gini_dataframe.loc[title, 'n'] = len(col)

    print(gini_dataframe)
    # save the gini coefficients to a file
    gini_dataframe.to_csv(gini_file, sep='\t')


def run(input_file, graph_file, output_file):
    '''
    runs everything
    **** change this function to alter filenames ****

    Parameters
    ----------
    input_file
        The file to read data from
    graph_file
        The file to save the graph as
    output_file
        The file to save the data to
    '''

    dataframe = pd.read_csv(input_file, delimiter='\t', index_col='Bin')

    # check all columns sum to 1, if so proceed and calculate/graph
    if check_columns(dataframe):
        dataframe = remove_zeros(dataframe)
        samples = sort_bins(dataframe)
        samples = calculate_cumulative_relative_abundance(samples)
        samples = remove_cumulative_abundance_over_one(samples)
        samples = calculate_cumulative_prop_trf(samples)
        make_graph(samples, graph_file)
        make_gini_file(samples, output_file)
        return samples
    else:
        sys.stderr.write("Error: columns don't sum to 1\n")
        sys.exit(1)


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('-g', '--graph', help='Graph file name',
                        default='graph.png', required=False)
    parser.add_argument('-o', '--output', help='Output data file name',
                        required=False)

    args = parser.parse_args()

    if args.output is None:
        args.output = args.inputfile + ".output.tsv"

    print("Input file:", args.inputfile)
    print("Output file:", args.output)
    print("Graph file", args.graph)
    sample_data = run(args.inputfile, args.graph, args.output)
