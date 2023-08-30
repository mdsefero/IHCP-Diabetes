

import pandas as pd

#Step 1
'''
df_DM = pd.read_csv("DMdata.csv", index_col='Pregnancy ID' )
df_met = pd.read_csv("Met_data.csv", index_col='Pregnancy ID')

df_out = df_DM.merge(df_met, left_index=True, right_index=True)
df_out.to_csv("IHCP_final.csv", index=True)
'''

#Some manual editing

#Step 2
df_IHCP = pd.read_csv("IHCP_Cohort_subj.txt.csv", index_col='Pregnancy ID' )
df_add = pd.read_csv("IHCP_final.csv", index_col='Pregnancy ID' )

merged_df = df_IHCP.join(df_add, how='inner')
merged_df.to_csv("IHCP_finalfinal.csv", index=True)
