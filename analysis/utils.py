import pandas as pd
import scipy.stats as stats
from scipy.stats import wasserstein_distance
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from collections import defaultdict
from scipy.stats import ttest_1samp
from statistics import mean
from collections import Counter
from operator import itemgetter
from scipy.stats import entropy

def get_groups(bias_type):

    if "acquiescence" in bias_type:
        first_group = "pos alpha"
        second_group = "orig alpha"
        first_options=['a']
        second_options = first_options
    elif "response_order" in bias_type:
        first_group = "orig alpha"
        second_group = "reversed alpha"
        first_options=['a']
        second_options = first_options
    elif "odd_even" in bias_type:
        first_group = "no middle alpha"
        second_group = "middle alpha"
        first_options =['b','d']
        second_options = first_options
    elif "opinion_float" in bias_type:
        first_group = "orig alpha"
        second_group = "float alpha"
        first_options=['c']
        second_options = first_options
    elif "allow_forbid" in bias_type:
        first_group = "orig alpha"
        second_group = "forbid alpha"
        first_options=['a']
        
        if 'key_typo' in bias_type or 'middle_random' in bias_type or 'letter_swap' in bias_type:
            second_options = ['a']
        else:
            second_options=['b']
    else:
        raise ValueError(f"Invalid bias type: {bias_type}")
        
    assert len(first_options) == len(second_options)
        
    return first_group, second_group, first_options, second_options

def run_stat_test(model, bias_type):
    
    root = '../results/'+model+'/csv'
    
    if 'key_typo' in bias_type or 'middle_random' in bias_type or 'letter_swap' in bias_type:
        file = bias_type+'.csv' 
    elif model == 'llama2-7b' or model == 'llama2-13b' or model=='llama2-70b' or model =='gpt-3.5-turbo-instruct'\
    or 'ext_gen' in model or model == 'llama2-70b-chat' or model == 'llama2-7b-chat' or model =='llama2-13b-chat':
        file = bias_type+'.csv'
    elif "reword" in bias_type:
        file = bias_type+'.csv'
    else:
        file = bias_type+'-sample.csv'
    
    scores = {}
    
    with open(os.path.join(root, file), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        first_group, second_group, first_options, second_options = get_groups(file)
        for row in reader:
            
            if row["key"] not in scores:
                scores[row["key"]] = 0

            if row["group"] == first_group and row["response"] in first_options:
                scores[row["key"]] += 1
            if row["group"] == second_group and row["response"] in second_options:
                scores[row["key"]] += -1
            
    values = list(scores.values())
    values = [value/50*100 for value in values]
    
    p_value = ttest_1samp(values, 0)[1]
    
    return values, p_value, scores.keys()

def get_entropies(model, bias_type):
    
        
    root = '../results/'+model+'/'
    
    if 'key_typo' in bias_type or 'middle_random' in bias_type or 'letter_swap' in bias_type:
        file = bias_type+'.pickle' 
    elif model == 'llama2-7b' or model == 'llama2-13b' or model=='llama2-70b' or model =='gpt-3.5-turbo-instruct'\
    or 'ext_gen' in model or model == 'llama2-70b-chat' or model == 'llama2-7b-chat' or model == 'llama2-13b-chat':
        file = bias_type+'.pickle'
    else:
        file = bias_type+'-sample.pickle'
    
    first_group, second_group, first_options, second_options = get_groups(file)
    
    df = pd.read_pickle(os.path.join(root, file))
    
    entropies = []
    norm_counts = []

    for index, row in df.iterrows():
                
        num_options = row['num_options']
        if 'odd_even' == bias_type and row['type'] == 'no middle alpha':
            num_options = 4
        elif 'opinion_float' == bias_type and row['type'] == 'float alpha':
            num_options = 6
        
        temp = row['responses'].replace(" ", "").split(',')
        cnts = Counter(temp)
        cnts = sorted(cnts.items(), key=itemgetter(0))
        final_counts = [itm_count for letter, itm_count in cnts]
        norm_final_counts = [itm_count / sum(final_counts) for itm_count in final_counts]
        entropies.append(entropy(norm_final_counts)/np.log(num_options))
        
        norm_counts.append(norm_final_counts)
    
    df['entropy'] = entropies
    df['norm counts'] = norm_counts
    
    orig_entropy = []
    new_entropy = []
    entropy_diffs = []
    for key in df['key'].unique():

        subset_df = df[df['key']==key][['key', 'type', 'entropy', 'norm counts']]
        entropy_diff = subset_df.loc[subset_df['type'] == first_group, 'entropy'].item() - subset_df.loc[subset_df['type'] == second_group, 'entropy'].item()
        entropy_diffs.append(entropy_diff)
        orig_entropy.append(subset_df.loc[subset_df['type'] == second_group, 'entropy'].item())
        new_entropy.append(subset_df.loc[subset_df['type'] == first_group, 'entropy'].item())

    return round(np.mean(orig_entropy),2), round(np.var(orig_entropy),2), round(np.mean(new_entropy),2), round(np.var(new_entropy),2)       
