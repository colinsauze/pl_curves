#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:08:01 2019

@author: colin
"""
from pl_curve import remove_zeros
import pandas


def test_remove_zeros():
    # each sub list is one row
    df = pandas.DataFrame([[1, 2, 3], [0, 0, 0], [0.1, 0.0, 0.5]])
    assert len(df) == 3
    df_result = remove_zeros(df)
    # we should have lost one row
    assert len(df_result) == 2
