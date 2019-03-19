import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('Agg')


def calculate_gini(x):
    # from https://stackoverflow.com/questions/39512260/calculating-gini-coefficient-in-python-numpy/39513799#39513799
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
        print(col, "total=", total)
        if total < 0.9999 or total > 1.0001:
            print("Error column ", col, "doesn't sum to 1.0")
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
            print("removing bin", row_index, "as its empty")
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
    steps = []
    j = 0
    for col in df.columns:
        data = df.loc[:, col].sort_values(ascending=False).to_frame()

        cum_prop_trfs = []
        cum_rel_abund = []

        for i in range(0, len(data)):
            cum_prop_trfs.append((i+1) / len(data))
            if i > 0:
                cum_rel_abund.append(data.iloc[i][0] + cum_rel_abund[i-1])
            else:
                cum_rel_abund.append(data.iloc[i][0])

        data['Cum Prop TRFs'] = cum_prop_trfs
        data['Cum Rel Abund'] = cum_rel_abund

        steps.append(data)
        j = j + 1
    return steps


def remove_cumulative_abundance_over_one(steps):
    '''
    deletes all but the first item where cumulative abundance is greater than 1
    @param steps - a list of dataframes each dataframe should contain 3 columns
    one with the name of the step, Cum Prop TRFs and Cum Rel Abund.
    @return a modified version of the list with all but the first row where
    cumulative abundance is greater than 1.
    '''
    steps2 = []
    for col in steps:
        i = 0
        found = False
        new_frame = col
        for row_index in col.index:
            val = col["Cum Rel Abund"][row_index]
            # if we've already found the first row with a value of 1,
            # start removing rows
            if found:
                new_frame = new_frame.drop(row_index)
            # look for values over 1
            # floating point representation means it might not be exactly 1
            elif val > 0.999999:
                found = True
        steps2.append(new_frame)
        i = i + 1
    steps = steps2
    return steps2


def make_outputs(steps, graph_file, gini_file):
    '''
    Makes a graph and calculates the Gini coefficients
    @param steps - a list of dataframes, each dataframe should contain 3
    columns one with the name of the step, Cum Prop TRFs and Cum Rel Abund.
    @param graph_file - Name of the file to save the graph to
    @param gini_file - Name of the file to save the gini coefficient data to
    '''
    titles = []
    for col in steps:
        titles.append(col.columns[0])
    # make an empty data frame for the gini coefficients
    gini_df = pd.DataFrame(columns=['Gini', 'Corrected Gini', 'n'], index=titles)

    # make graph
    for col in steps:
        title = col.columns[0]
        plt.plot(col.loc[:, 'Cum Prop TRFs'], col.loc[:, 'Cum Rel Abund'],
                 label=title)
        plt.ylabel("Cumulative Relative Abundance")
        plt.xlabel("Cumulative Prop TRF")
        plt.grid()
        plt.legend()
        plt.savefig(graph_file)

        # calculate gini coefficient
        gini = calculate_gini(col.iloc[:, 0])
        corrected_gini = gini * (len(col) / (len(col)-1))
        gini_df.loc[title, 'Gini'] = gini
        gini_df.loc[title, 'Corrected Gini'] = corrected_gini
        gini_df.loc[title, 'n'] = len(col)

    print(gini_df)
    gini_df.to_csv(gini_file, sep='\t')


def run():
    filename = 'Enrichment_data_trimmed_tab.txt'
    df = pd.read_csv(filename, delimiter='\t', index_col='Bin')

    if check_columns(df):
        df = remove_zeros(df)
        steps = sort_bins(df)
        steps = remove_cumulative_abundance_over_one(steps)
        make_outputs(steps, "enrichment_graph.png", "enrichment_gini.tsv")


if __name__ == "__main__":
    run()
