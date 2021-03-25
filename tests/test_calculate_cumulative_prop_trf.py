#!/usr/bin/env python3
from pl_curve import calculate_cumulative_relative_abundance
from pl_curve import remove_cumulative_abundance_over_one
from pl_curve import calculate_cumulative_prop_trf
import pandas
import numpy as np


def test_calculate_cumulative_prop_trf():

    data1 = np.array([['', 'Step I'],
                     ['219', 0.239709],
                     ['218', 0.190986]])

    data2 = np.array([['', 'Step II'],
                     ['219', 0.434289],
                     ['218', 0.193835]])

    # create a dataframe, each sub list is one row
    df1 = pandas.DataFrame(data=data1[1:, 1:], index=data1[1:, 0],
                           columns=data1[0, 1:]).astype(np.dtype(np.float64))

    df2 = pandas.DataFrame(data=data2[1:, 1:], index=data2[1:, 0],
                           columns=data2[0, 1:]).astype(np.dtype(np.float64))

    samples = [df1, df2]

    samples = calculate_cumulative_relative_abundance(samples)
    samples = remove_cumulative_abundance_over_one(samples)
    result = calculate_cumulative_prop_trf(samples)

    df1_res = result[0]
    df2_res = result[1]

    assert 'Cum Prop TRFs' in df1_res.columns
    assert 'Cum Prop TRFs' in df2_res.columns

    assert df1_res.loc['219', 'Cum Prop TRFs'] == 0.5
    assert df1_res.loc['218', 'Cum Prop TRFs'] == 1.0

    assert df2_res.loc['219', 'Cum Prop TRFs'] == 0.5
    assert df2_res.loc['218', 'Cum Prop TRFs'] == 1.0
