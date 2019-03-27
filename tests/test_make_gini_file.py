#!/usr/bin/env python3
from pl_curve import make_gini_file
import pandas
import numpy as np
import os


def test_make_gini_file():
    data1 = np.array([['', 'Step I', 'Cum Prop TRFs', 'Cum Rel Abund'],
                     ['219', 0.5, 0.5, 0.3],
                     ['218', 0.5, 1.0, 1.0]])

    data2 = np.array([['', 'Step II', 'Cum Prop TRFs', 'Cum Rel Abund'],
                     ['219', 0.25, 0.5, 0.4],
                     ['218', 0.75, 1.0, 1.0]])

    # create a dataframe, each sub list is one row
    df1 = pandas.DataFrame(data=data1[1:, 1:], index=data1[1:, 0],
                           columns=data1[0, 1:]).astype(np.dtype(np.float64))

    df2 = pandas.DataFrame(data=data2[1:, 1:], index=data2[1:, 0],
                           columns=data2[0, 1:]).astype(np.dtype(np.float64))

    samples = [df1, df2]

    # delete test.png if it already exists
    try:
        os.remove("test.tsv")
    # catch the error if file doesn't exist
    except FileNotFoundError as error:
        pass

    make_gini_file(samples, "test.tsv")
    assert os.path.isfile("test.tsv") is True

    data = pandas.read_csv("test.tsv", delimiter='\t', index_col=0)
    assert data.loc['Step I', 'Gini'] == 0.0
    assert data.loc['Step I', 'Corrected Gini'] == 0.0
    assert data.loc['Step II', 'Gini'] == 0.25
    assert data.loc['Step II', 'Corrected Gini'] == 0.5
