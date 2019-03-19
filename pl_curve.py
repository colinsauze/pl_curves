import pandas as pd
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def calculate_gini(x):
    '''
    calculates the gini coefficient

    code from:
    stackoverflow.com/questions/39512260/calculating-gini-coefficient-in-python-numpy/39513799

    @param x - the list of data to calculate the gini coefficient on
    @return the gini coefficient for this data
    '''
    # (Warning: This is a concise implementation, but it is O(n**2)
    # in time and memory, where n = len(x).  *Don't* pass in huge
    # samples!)

    # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g


def check_columns(df):
    '''
    Checks all columns in the data frame sum to 1
    @param df - the data frame to check
    @return False if a column doesn't sum to 1, True if they all do
    '''
    for col in df.columns:
        total = sum(df.loc[:, col])
        # print(col, "total=", total)
        if total < 0.9999 or total > 1.0001:
            # print("Error column ", col, "doesn't sum to 1.0")
            return False
    return True


def remove_zeros(df):
    '''
    Removes all rows which contain only zeros
    @param df - the data frame to check
    @return The dataframe with all zero rows removed
    '''

    for row_index in df.index:
        total = sum(df.loc[row_index])
        if total == 0:
            # print("removing bin", row_index, "as its empty")
            df = df.drop(row_index)

    return df


def sort_bins(df):
    '''
    Sort each bin by its relative abundance,
    calculates cumulative relative abundance and cumulative proportional TRFs
    @param df - the data frame to check
    @return A list of dataframes, each dataframe contains the step names,
    cumulative relative abundance and cumulative proportional TRFs.
    '''

    # split each column into its own dataframe
    samples = []
    j = 0
    for col in df.columns:

        # sort the bins in descending order, convert result to a new dataframe
        data = df.loc[:, col].sort_values(ascending=False).to_frame()

        cum_prop_trfs = []
        cum_rel_abund = []

        # calculate cumulative relative abundance and cumulative prop trfs
        for i in range(0, len(data)):
            cum_prop_trfs.append((i+1) / len(data))
            if i > 0:
                cum_rel_abund.append(data.iloc[i][0] + cum_rel_abund[i-1])
            else:
                cum_rel_abund.append(data.iloc[i][0])

        data['Cum Prop TRFs'] = cum_prop_trfs
        data['Cum Rel Abund'] = cum_rel_abund

        samples.append(data)
        j = j + 1
    return samples


def remove_cumulative_abundance_over_one(samples):
    '''
    deletes all but the first item where cumulative abundance is greater than 1
    @param samples - a list of dataframes each dataframe should have 3 columns
    one with the name of the step, Cum Prop TRFs and Cum Rel Abund.
    @return a modified version of the list with all but the first row where
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
    @param samples - a list of dataframes, each dataframe should contain 3
    columns one with the name of the step, Cum Prop TRFs and Cum Rel Abund.
    @param filename - Name of the file to save the graph to
    '''

    # make graph
    for col in samples:
        # get the title of current sample from the heading of its 1st column
        title = col.columns[0]

        # plot cumulative prop trfs vs cumulative relative abundance
        plt.plot(col.loc[:, 'Cum Prop TRFs'], col.loc[:, 'Cum Rel Abund'],
                 label=title)
        plt.ylabel("Cumulative Relative Abundance")
        plt.xlabel("Cumulative Prop TRF")
        plt.grid()
        plt.legend()
        plt.savefig(filename)


def make_gini_file(samples, gini_file):
    '''
    Calculates the Gini coefficients and saves them to a TSV file
    @param samples - a list of dataframes, each dataframe should contain 3
    columns one with the name of the step, Cum Prop TRFs and Cum Rel Abund.
    @param gini_file - Name of the file to save the gini coefficient data to
    '''
    titles = []
    for col in samples:
        titles.append(col.columns[0])
    # make an empty data frame for the gini coefficients
    gini_df = pd.DataFrame(columns=['Gini', 'Corrected Gini', 'n'],
                           index=titles)

    # make graph
    for col in samples:
        # get the title of current sample from the heading of its 1st column
        title = col.columns[0]

        # calculate gini coefficient and corrected gini (g * (n/n-1))
        gini = calculate_gini(col.iloc[:, 0])
        corrected_gini = gini * (len(col) / (len(col)-1))

        # add gini coefficients into a dataframe for saving the result
        gini_df.loc[title, 'Gini'] = gini
        gini_df.loc[title, 'Corrected Gini'] = corrected_gini
        gini_df.loc[title, 'n'] = len(col)

    print(gini_df)
    # save the gini coefficients to a file
    gini_df.to_csv(gini_file, sep='\t')


def run():
    '''
    runs everything
    **** change this function to alter filenames ****
    '''

    filename = 'Enrichment_data_trimmed_tab.txt'
    df = pd.read_csv(filename, delimiter='\t', index_col='Bin')

    # check all columns sum to 1, if so proceed and calculate/graph
    if check_columns(df):
        df = remove_zeros(df)
        samples = sort_bins(df)
        make_graph(samples, "enrichment_graph.png")
        samples = remove_cumulative_abundance_over_one(samples)
        make_gini_file(samples, "enrichment_gini.tsv")
    else:
        sys.stderr.write("Error: columns don't sum to 1\n")
        sys.exit(1)


if __name__ == "__main__":
    run()
