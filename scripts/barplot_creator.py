import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ave(lst): 
    return sum(lst) / len(lst)

def standard_deviation(lst):
    variance = sum([((x - ave(lst)) ** 2) for x in lst]) / len(lst) 
    return variance ** 0.5

def draw_bar_plot(path):
    df = pd.read_excel(path)
    dic = {}
    for row in df.iterrows():
        row = list(row[1])
        factor = row[0]
        value = row[1]
        if factor not in dic.keys():
            dic[factor] = [value]
        else:
            dic[factor].append(value)
    fig, ax = plt.subplots()
    
    factors = []
    values = []
    errors = []
    
    items = list(dic.items())
    for item in items:
        factors.append(item[0])
        values.append(ave(item[1]))
        errors.append(standard_deviation(item[1]))
    
    plt.bar(factors, values, color='grey', width=0.4)
    plt.errorbar(factors, values, yerr=errors, fmt='none',
                ecolor="black", capsize=8, patch_artist=True)
    
    from sys import platform

    if platform == "linux" or platform == "linux2": 
        plt.rcParams['font.family'] = 'NanumGothic'
    elif platform == "darwin":
        plt.rcParams['font.family'] = 'AppleGothic' 
    elif platform == "win32":
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        print("User platform could not be identified. Korean characters may not be shown correctly when visualizing.")

    plt.xlabel("Factors", fontsize=15) 
    plt.ylabel("Average Surprisal Value", fontsize=15) 
    plt.title("Surprisal Bar Plot", fontsize=15) 
    plt.show() 