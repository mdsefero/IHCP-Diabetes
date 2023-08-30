
import subprocess
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib ###required because running 'headless' on Ubuntu for windows
matplotlib.use('Agg') ###required because running 'headless' on Ubuntu for windows
import matplotlib.pyplot as plt
import statsmodels.api as sm
global Category20c # D3 Category20c palette
Cat20c = ['#3182bd', '#6baed6', '#9ecae1', '#c6dbef', #blues [0-3]
          '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', #oranges [4-7]
          '#31a354', '#74c476', '#a1d99b', '#c7e9c0', #greens [8-13]
          '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', #purples [14-17]
          '#636363', '#969696', '#bdbdbd', '#d9d9d9'] #greys [18-21]


def ct_to_percent(contingency_table):
    return contingency_table.apply(lambda x: (100 * x / float(x.sum())).round(2))


def plot_chi (name, contingency_table):
    colors = [Cat20c[2], Cat20c[6]]
    contingency_table.T.plot(kind='bar', stacked=True, color=colors) #transposes 'T'
    plt.xticks(range(len(contingency_table.columns)), contingency_table.columns, rotation=0)
    plt.ylabel('Subjects (%)', fontweight='bold')
    plt.title(name, fontweight='bold')
    legend_title = contingency_table.index.name
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2, fancybox=False, shadow=False, title=legend_title)
    plt.tight_layout(rect=[0, 0.1, 1, 0.9])  # Adjust the rect values to leave space for the legend
    filename = f"{name}.png"
    plt.savefig(filename, bbox_inches='tight')
    #plt.show() #Unhash to bring up instead of save. Does not work in Ubuntu for windows
    # Open the file in Windows
    command = f'explorer.exe "{filename}"'
    subprocess.call(command, shell=True)


def chi (name, treatment, outcome): 
    # Create a contingency table
    contingency_table = pd.crosstab(treatment, outcome)
    CT_percentage = ct_to_percent(contingency_table)
    # Perform chi-squared test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print (f"{chr(10)}{name} results:")
    # Print the results
    print ("N: ", contingency_table.values.sum())
    print ("Contingency_table:\n",contingency_table)
    print ("\nCT as %:\n", CT_percentage)
    print ("Chi-squared statistic:", chi2.round(2))
    print ("P-value:", p_value)
    #print("Degrees of freedom:", dof)
    #df.to_csv(f"{name}.csv", index=false) 
    plot_chi(name, CT_percentage)


def subset_diabetes_data(df):
    variables_of_interest = [
        'Type I diabetes', 
        'Type II diabetes',
        'Gestational diabetes',
        'Uncontrolled diabetes',
        'Metformin', 
        'IHCP'
        ]          
    df = df.fillna('')# Remove NaN's throws error
    df = df[variables_of_interest]
    df = df.applymap(lambda s: s.lower()) #All lower case for 1/0 conversion 
    return df, variables_of_interest


#Calculate odds ratio using logistic regression 
def odds_ratio(df): 
    print (f"{chr(10)*3}Starting Logit Regression for Odds Ratios")
    #subset and process data
    OR_df, variables_of_interest = subset_diabetes_data(df)
    OR_df['Outcome'] = OR_df['IHCP'] # Define outcome of interest i.e. IHCP
    variables_of_interest.remove('IHCP') #Since it is the target remove from analysis var  
    
    for i in OR_df: OR_df[i] = OR_df[i].map({'yes': 1, 'no': 0})#convert y/n to 1/0 
    OR_df = OR_df.dropna()#have to drop misssing data or does not work
    
    # Fit a logistic regression model
    X = OR_df[variables_of_interest]  # Multiple exposures as predictor variables
    y = OR_df['Outcome']
    X = sm.add_constant(X)  # Add an intercept term
    logit_model = sm.Logit(y, X)
    result = logit_model.fit()
    
    odds_ratios = np.exp(result.params).round(4)
    p_values = result.pvalues
    confidence_intervals = result.conf_int().apply(np.exp).round(4)

    print("Odds Ratios:")
    print(odds_ratios)
    print("\np-values:")
    print(p_values)
    print("\nConfidence Intervals:")
    print(confidence_intervals)
 
 
def metformin_subanalysis(df):
    met_sub_df, variables_of_interest = subset_diabetes_data(df)
    met_sub_df['AnyDM'] = np.where((met_sub_df['Type II diabetes'] == 'yes') | 
                                   (met_sub_df['Gestational diabetes'] == 'yes') |
                                   (met_sub_df['Type I diabetes'] == 'yes') 
                                   , 'yes', 'no')
    GDM_df = met_sub_df[met_sub_df['Gestational diabetes'] == 'yes']
    T2DM_df = met_sub_df[met_sub_df['Type II diabetes'] == 'yes']
    any_df = met_sub_df[met_sub_df['AnyDM'] == 'yes']
    chi('GDM only', GDM_df['Metformin'], GDM_df['IHCP'])
    chi('T2DM only', T2DM_df['Metformin'], T2DM_df['IHCP'])
    chi('AnyDM', any_df['Metformin'], any_df['IHCP'])
 
 
def main():       
    df = pd.read_csv("IHCP_finalfinal.csv", index_col='Pregnancy ID' )   
    #Dictionary of chi comparisons to make 
    comparissons = {
        'T1DM': [df['Type I diabetes'], df['IHCP']], 
        'T2DM': [df['Type II diabetes'], df['IHCP']],
        'GDM': [df['Gestational diabetes'], df['IHCP']],
        'Uncontroled diabetes': [df['Uncontrolled diabetes'], df['IHCP']],
        'Metformin': [df['Metformin'], df['IHCP']]
        }
    for name, data in comparissons.items():
        chi(name, data[0], data[1])
    odds_ratio(df)
    metformin_subanalysis(df)


if __name__ == '__main__': 
    main()