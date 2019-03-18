import pandas

df = pandas.read_csv('Enrichment_data_trimmed_tab.txt', delimiter='\t', index_col='Bin')

# check all columns sum to 1
for col in df.columns:
    total = sum(df.loc[:, col])
    print(col, "total=", total)
    if total < 0.9999 or total > 1.0001:
        print("Error column ", col, "doesn't sum to 1.0")


# remove rows which are all zeros
for row_index in df.index:
    total = sum(df.loc[row_index])
    if total == 0:
        print("removing bin", row_index, "as its empty")
        df = df.drop(row_index)

# sort bins for each stage
# split each column into its own dataframe
columns = []
j =  0
for col in df.columns:
    data = df.loc[:, col].sort_values(ascending=False).to_frame()
    
    cum_prop_trfs = []
    cum_rel_abund = []
    
    for i in range(0,len(data)):
        cum_prop_trfs.append((i+1) / len(data))
        if i > 0:
            cum_rel_abund.append(data.iloc[i][0] + cum_rel_abund[i-1])
        else:
            cum_rel_abund.append(data.iloc[i][0])
    
    data['Cum Prop TRFs']=cum_prop_trfs
    data['Cum Rel Abund']=cum_rel_abund
    
    columns.append(data)
    j = j + 1

