#!/usr/bin/env python3

from pl_curve import sort_bins
import pandas
import numpy as np


def test_sort_bins():
    '''
    test the sort_bins function
    '''
    data = np.array([['', 'Col1', 'Col2'],
                    ['Row1', 1, 2],
                    ['Row2', 3, 4],
                    ['Row3', 2, 3]])

    # create a dataframe, each sub list is one row
    df = pandas.DataFrame(data=data[1:, 1:], index=data[1:, 0],
                          columns=data[0, 1:])

    result = sort_bins(df)

    # check each column is in order
    for col in result:
        max_value = col.max()[0]
        for i in col.values:
            assert float(i[0]) <= max_value
            max_value = float(i[0])
