br_dataframe = br_dataframe[br_dataframe[state_column_name].isin(states_filter)].cx[:-42,:].reset_index()