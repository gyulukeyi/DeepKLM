import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
from collections import defaultdict
from sys import platform
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def config():
    notch = False
    
    with open("./boxplot_config.txt", "r") as reader:
        config = reader.readlines()

    for c in config:
        if c == "\n":
            continue
        splited = c.split("=")
        typ = splited[0].rstrip().lstrip()
        setting= splited[1].rstrip().lstrip().replace("\n", "").lower()
        
        mask = "mask"
        if typ == "filepath":
            filepath = setting
        elif typ == "factor2":
            factor2 = "factor2"
            factor2_name = setting
        elif typ == "factor1":
            factor1 = "factor1"
            factor1_name = setting
        elif typ == "factor2_vals":
            factor2_vals = setting.split(" ")
        elif typ == "factor1_vals":
            factor1_vals = setting.split(" ")
        elif typ == "mask_vals":
            mask_vals = setting.split(" ")
        elif typ == "variable_value":
            variable_value = "value"
            value_name = setting
        elif typ == "notch":
            if setting == "False":
                notch = False
            else:
                notch=True
        elif typ == "title":
            title = setting
        elif typ == "size":
            size = setting
    
    check = verify_config(filepath, factor2, factor1,
                          mask, factor2_vals, factor1_vals,
                          mask_vals, variable_value, size)
    if check:
        return filepath, factor2, factor2_name, factor1, factor1_name, mask, value_name, factor2_vals, factor1_vals, mask_vals, variable_value, notch, title, size
    else:
        print("프로그램 종료")
        exit()
                
            
def verify_config(filepath, factor2, factor1, mask,
                 factor2_vals, factor1_vals, mask_vals,
                 variable_value, size):
    check_list = ["filepath", "factor2", "factor1", "mask",
                 "factor2_vals", "factor1_vals", "mask_vals",
                 "variable_value"]
    
    if size != "22" and size != "222":
        print("size는 22 또는 222여야 함")
        return False

    try:
        df = pd.read_excel(filepath)
    except FileNotFoundError:
        print("xlsx 파일의 위치가 잘못됨")
        raise
    

    for i, check in enumerate([filepath, factor2, factor1,
                               mask, factor2_vals, factor1_vals,
                               mask_vals, variable_value]):
        if check == "":
            if i == 1 and size == "22":
                continue
                
            else:
                print(check_list[i], "가 입력되지 않음")
                return False
            
        elif check == [""]:
            if i == 4 and size == "22":
                continue
        
        if i == 2 or i ==3 or i == 7: # i == 1
            try:
                test = df[check]
            except KeyError:
                print(check, "는 올바른 컬럼 이름이 아님.")
                raise
                    
        elif i == 4 or i == 5 or i == 6:
            if len(check) != 2:
                print(check_list[i], "는 반드시 공백으로 구분되는 2개의 값이어야함")
                return False
    return True

def flatten(l):
    return  [item for sublist in l for item in sublist]

def to_array(df): # from dataframe to np array
    return np.asarray(flatten(df))


def return_conditional_values_222(df, variables): # returning values for boxplot
    top = variables["names"]["top"]
    bottom = variables["names"]["bottom"]
    box = variables["names"]["box"]
    variable_value = variables["names"]["numeric"]

    first_col_name = top
    first_micro1 = variables[first_col_name]["value"][0]
    first_micro2 = variables[first_col_name]["value"][1]
    
    second_col_name = bottom
    second_micro1 = variables[second_col_name]["value"][0]
    second_micro2 = variables[second_col_name]["value"][1]
    
    third_col_name = box
    third_micro1 = variables[third_col_name]["value"][0]
    third_micro2 = variables[third_col_name]["value"][1]
    
    print("""
    2 by 2 by 2 plot data summary:
    
    top name = {}
    bottom name = {}
    box name = {}
    
    variable_value = {}
    
    first_col_name = {}
        first_micro1 = {}
        first_micro2 = {}
    
    second_col_name = {}
        second_micro1 = {}
        second_micro2 = {}
    
    third_col_name = {}
        third_micro1 = {}
        third_micro2 = {}
    """.format(top, bottom, box, variable_value, first_col_name, first_micro1, first_micro2, second_col_name,
              second_micro1, second_micro2, third_col_name, third_micro1, third_micro2))
    
        #f1-s1-t1
    v1 = df[df[first_col_name] == first_micro1][df[second_col_name] == second_micro1][df[third_col_name] == third_micro1][variable_value].values
        #f1-s1-t2
    v2 = df[df[first_col_name] == first_micro1][df[second_col_name] == second_micro1][df[third_col_name] == third_micro2][variable_value].values
        #f1-s2-t1
    v3 = df[df[first_col_name] == first_micro1][df[second_col_name] == second_micro2][df[third_col_name] == third_micro1][variable_value].values
        #f1-s2-t2
    v4 = df[df[first_col_name] == first_micro1][df[second_col_name] == second_micro2][df[third_col_name] == third_micro2][variable_value].values
    
        #f2-s1-t1
    v5 = df[df[first_col_name] == first_micro2][df[second_col_name] == second_micro1][df[third_col_name] == third_micro1][variable_value].values
        #f2-s1-t2
    v6 = df[df[first_col_name] == first_micro2][df[second_col_name] == second_micro1][df[third_col_name] == third_micro2][variable_value].values
        #f2-s2-t1
    v7 = df[df[first_col_name] == first_micro2][df[second_col_name] == second_micro2][df[third_col_name] == third_micro1][variable_value].values
        #f2-s2-t2
    v8 = df[df[first_col_name] == first_micro2][df[second_col_name] == second_micro2][df[third_col_name] == third_micro2][variable_value].values
    
    print("""
    {variable_value} value1: {v1}
    column {first_col_name} is {first_micro1}
    column {second_col_name} is {second_micro1}
    column {third_col_name} is {third_micro1}
    
    
    {variable_value} value2: {v2}
    column {first_col_name} is {first_micro1}
    column {second_col_name} is {second_micro1}
    column {third_col_name} is {third_micro2}
    
    
    {variable_value} value3: {v3}
    column {first_col_name} is {first_micro1}
    column {second_col_name} is {second_micro2}
    column {third_col_name} is {third_micro1}
    
    
    {variable_value} value4: {v4}
    column {first_col_name} is {first_micro1}
    column {second_col_name} is {second_micro2}
    column {third_col_name} is {third_micro2}
    
    
    {variable_value} value5: {v5}
    column {first_col_name} is {first_micro2}
    column {second_col_name} is {second_micro1}
    column {third_col_name} is {third_micro1}
    
    
    {variable_value} value6: {v6}
    column {first_col_name} is {first_micro2}
    column {second_col_name} is {second_micro1}
    column {third_col_name} is {third_micro2}
    
    
    {variable_value} value7: {v7}
    column {first_col_name} is {first_micro2}
    column {second_col_name} is {second_micro2}
    column {third_col_name} is {third_micro1}
    
    
    {variable_value} value8: {v8}
    column {first_col_name} is {first_micro2}
    column {second_col_name} is {second_micro2}
    column {third_col_name} is {third_micro2}
    
    """.format(first_col_name=first_col_name, second_col_name=second_col_name, third_col_name=third_col_name,v5=v5,
               first_micro1=first_micro1, first_micro2=first_micro2, second_micro1=second_micro1,v3=v3, v4=v4,
               second_micro2=second_micro2, third_micro1=third_micro1, third_micro2=third_micro2, v1=v1, v2=v2,
               v6=v6, v7=v7, v8=v8, variable_value=variable_value
              ))
    
    return [v1, v2, v3, v4, v5, v6, v7, v8]

def return_conditional_values_22(df, variables): # returning values for boxplot

    
    bottom = variables["names"]["bottom"]
    box = variables["names"]["box"]
    variable_value = variables["names"]["numeric"]

    first_col_name = bottom
    first_micro1 = variables[first_col_name]["value"][0]
    first_micro2 = variables[first_col_name]["value"][1]
    
    second_col_name = box
    second_micro1 = variables[second_col_name]["value"][0]
    second_micro2 = variables[second_col_name]["value"][1]
    

    print("""
    2 by 2 plot data summary:
    
    bottom name = {}
    box name = {}
    
    variable_value = {}
    
    first_col_name = {}
        first_micro1 = {}
        first_micro2 = {}
    
    second_col_name = {}
        second_micro1 = {}
        second_micro2 = {}
    
    """.format(bottom, box, variable_value, first_col_name, first_micro1, first_micro2, second_col_name,
              second_micro1, second_micro2))
    
        #f1-s1
    v1 = df[df[first_col_name] == first_micro1][df[second_col_name] == second_micro1][variable_value].values
        #f1-s2
    v2 = df[df[first_col_name] == first_micro1][df[second_col_name] == second_micro2][variable_value].values
        #f2-s1
    v3 = df[df[first_col_name] == first_micro2][df[second_col_name] == second_micro1][variable_value].values
        #f2-s2
    v4 = df[df[first_col_name] == first_micro2][df[second_col_name] == second_micro2][variable_value].values
    
    print("""
    {variable_value} value1: {v1}
    column {first_col_name} is {first_micro1}
    column {second_col_name} is {second_micro1}
    
    
    {variable_value} value2: {v2}
    column {first_col_name} is {first_micro1}
    column {second_col_name} is {second_micro2}
    
    
    {variable_value} value3: {v3}
    column {first_col_name} is {first_micro2}
    column {second_col_name} is {second_micro1}
    
    
    {variable_value} value4: {v4}
    column {first_col_name} is {first_micro2}
    column {second_col_name} is {second_micro2}
    
    
    """.format(first_col_name=first_col_name, second_col_name=second_col_name,  v1=v1, v2=v2, v3=v3, v4=v4,
               first_micro1=first_micro1, first_micro2=first_micro2, second_micro1=second_micro1,
               second_micro2=second_micro2, variable_value=variable_value))
    
    return [v1, v2, v3, v4]


def set_names(variables, top, bottom, numeric):
    temp = defaultdict()
    temp["names"] = defaultdict()
    temp["names"].update({"top" : top})
    temp["names"].update({"bottom" : bottom})
    temp["names"].update({"numeric" : numeric})
    temp["names"].update({"box" : "mask"})
    temp["names"] = dict(temp["names"])
    variables.update(temp)
    
    return variables

def draw22(values, variables, notch=False, title="boxplot_result"):
    label_title = variables["factor1"]["name"]
    labels = variables["factor1"]["value"]
    
    
    color_title = variables["mask"]["name"]
    color_names = variables["mask"]["value"]
    
    value_name = variables["numeric"]["name"]

    left_positions=[-0.4, 0.4]
    right_positions=[1.6, 2.4]
    ticks=[0, 2]
    
    left_color = ['pink']
    right_color = ['lightgreen']
    
#    fontprop = fm.FontProperties("NanumGothic")

    if platform == "linux" or platform == "linux2": 
        flist = fm.get_fontconfig_fonts()
        available_fonts = [fm.FontProperties(fname=fname).get_name() for fname in flist]
        fontprop = fm.FontProperties("NanumGothic")
    elif platform == "darwin":
        fontprop = fm.FontProperties("AppleGothic")
    elif platform == "win32":
        fontprop = fm.FontProperties("Malgun Gothic")
    else:
        print("User platform could not be identified. Korean characters may not be shown correctly when visualizing.")
    
    # first plot
    fig = plt.figure(figsize=(10, 8))
    fig.suptitle(title, fontsize=35, fontproperties=fontprop)
    
    left_group1 = [values[0], values[1]]
    right_group1 = [values[2], values[3]]

    bplot1_1 = plt.boxplot(left_group1[0], widths=0.35,
                             positions=[left_positions[0]],
                             notch=notch,
                             patch_artist=True)  
    bplot1_2 = plt.boxplot(left_group1[1], widths=0.35,
                             positions=[left_positions[1]],
                             notch=notch,
                             patch_artist=True)  
    bplot2_1 = plt.boxplot(right_group1[0], widths=0.35,
                             positions=[right_positions[0]],
                             notch=notch,
                             patch_artist=True)  
    bplot2_2 = plt.boxplot(right_group1[1], widths=0.35,
                             positions=[right_positions[1]],
                             notch=notch,
                             patch_artist=True)  
    plt.xticks(ticks, labels, fontsize=15, fontproperties=fontprop)
    
    for bplot in (bplot1_1, bplot1_2, bplot2_1, bplot2_2):
        if bplot == bplot1_1 or bplot == bplot2_1:
            for patch, color in zip(bplot['boxes'], left_color):
                patch.set_facecolor(color)
        else:
            for patch, color in zip(bplot['boxes'], right_color):
                patch.set_facecolor(color)

    plt.grid(True)
    plt.xlabel(label_title, fontsize=20, fontproperties=fontprop)
    plt.ylabel(value_name, fontsize=20, fontproperties=fontprop)
    plt.legend([bplot1_1["boxes"][0], bplot1_2["boxes"][0]], color_names, loc='upper right', fontsize=15, prop=fontprop)
    plt.savefig("./"+title+".jpg", dpi=400)
    plt.show()
    
def draw222(values, variables, notch=False, title="boxplot_result"):
    label_title = variables["factor1"]["name"]
    labels = variables["factor1"]["value"]
    
    top_title = variables["factor2"]["name"]
    titles = variables["factor2"]["value"]
    
    color_title = variables["mask"]["name"]
    color_names = variables["mask"]["value"]
    
    value_name = variables["numeric"]["name"]
    
    left_positions=[-0.4, 0.4]
    right_positions=[1.6, 2.4]
    ticks=[0, 2]
    
    left_color = ['pink']
    right_color = ['lightgreen']
    
 #    fontprop = fm.FontProperties("NanumGothic")

    if platform == "linux" or platform == "linux2": 
        flist = fm.get_fontconfig_fonts()
        available_fonts = [fm.FontProperties(fname=fname).get_name() for fname in flist]
        fontprop = fm.FontProperties("NanumGothic")
    elif platform == "darwin":
        fontprop = fm.FontProperties("AppleGothic")
    elif platform == "win32":
        fontprop = fm.FontProperties("Malgun Gothic")
    else:
        print("User platform could not be identified. Korean characters may not be shown correctly when visualizing.")
    
    # first plot
    fig = plt.figure(figsize=(10, 8))
    fig.suptitle(top_title + "(" + titles[0] + ")", fontsize=35, fontproperties=fontprop)
    
    left_group1 = [values[0], values[1]]
    right_group1 = [values[2], values[3]]

    bplot1_1 = plt.boxplot(left_group1[0], widths=0.35,
                             positions=[left_positions[0]],
                             notch=notch,
                             patch_artist=True)  
    bplot1_2 = plt.boxplot(left_group1[1], widths=0.35,
                             positions=[left_positions[1]],
                             notch=notch,
                             patch_artist=True)  
    bplot2_1 = plt.boxplot(right_group1[0], widths=0.35,
                             positions=[right_positions[0]],
                             notch=notch,
                             patch_artist=True)  
    bplot2_2 = plt.boxplot(right_group1[1], widths=0.35,
                             positions=[right_positions[1]],
                             notch=notch,
                             patch_artist=True)  
    plt.xticks(ticks, labels, fontsize=15, fontproperties=fontprop)
    
    for bplot in (bplot1_1, bplot1_2, bplot2_1, bplot2_2):
        if bplot == bplot1_1 or bplot == bplot2_1:
            for patch, color in zip(bplot['boxes'], left_color):
                patch.set_facecolor(color)
        else:
            for patch, color in zip(bplot['boxes'], right_color):
                patch.set_facecolor(color)

    plt.grid(True)
    plt.xlabel(label_title, fontsize=20, fontproperties=fontprop)
    plt.ylabel(value_name, fontsize=20, fontproperties=fontprop)
    plt.legend([bplot1_1["boxes"][0], bplot1_2["boxes"][0]], color_names, loc='upper right', fontsize=15, prop=fontprop)
    plt.savefig("./"+title+"1.jpg", dpi=400, fontproperties=fontprop)
    plt.show()
    
    # second plot
    fig = plt.figure(figsize=(10, 8))
    fig.suptitle(top_title + "(" + titles[1] + ")", fontsize=35, fontproperties=fontprop)

    left_group2 = [values[4], values[5]]
    right_group2 = [values[6], values[7]]

    bplot3_1 = plt.boxplot(left_group2[0], widths=0.35,
                             positions=[left_positions[0]],
                             notch=notch,
                             patch_artist=True)  
    bplot3_2 = plt.boxplot(left_group2[1], widths=0.35,
                             positions=[left_positions[1]],
                             notch=notch,
                             patch_artist=True)  
    bplot4_1 = plt.boxplot(right_group2[0], widths=0.35,
                             positions=[right_positions[0]],
                             notch=notch,
                             patch_artist=True)  
    bplot4_2 = plt.boxplot(right_group2[1], widths=0.35,
                             positions=[right_positions[1]],
                             notch=notch,
                             patch_artist=True)
    plt.xticks(ticks, labels, fontsize=15, fontproperties=fontprop)

    for bplot in (bplot3_1, bplot3_2, bplot4_1, bplot4_2):
        if bplot == bplot3_1 or bplot == bplot4_1:
            for patch, color in zip(bplot['boxes'], left_color):
                patch.set_facecolor(color)
        else:
            for patch, color in zip(bplot['boxes'], right_color):
                patch.set_facecolor(color)

    plt.grid(True)
    plt.xlabel(label_title, fontsize=20, fontproperties=fontprop)
    plt.ylabel(value_name, fontsize=20, fontproperties=fontprop)
    plt.legend([bplot4_1["boxes"][0], bplot4_2["boxes"][0]], color_names, loc='upper right', fontsize=15, prop=fontprop)
    plt.savefig("./"+title+"2.jpg", dpi=400)
    plt.show()


def draw_box_plot():
    notch=True

    filepath, factor2, factor2_name, factor1, factor1_name, mask, value_name, factor2_vals, factor1_vals, mask_vals, variable_value, notch, title, size = config()
    df = pd.read_excel(filepath)

    variables = defaultdict()
    if size == "222":
        variables["factor2"] = {"name": factor2_name, "value":factor2_vals}
    variables["factor1"] = {"name": factor1_name, "value":factor1_vals}
    variables["mask"] = {"name": mask, "value": mask_vals}
    variables["numeric"] = {"name": value_name, "value":variable_value}
    variables["size"] = size
    variables = dict(variables)
    variables = set_names(variables, top=factor2, bottom=factor1, numeric=variable_value)

    values=[]
    if variables["size"] == "222":
        values = return_conditional_values_222(df, variables)
    elif variables["size"] == "22":
        values = return_conditional_values_22(df, variables)

    #values[""]

    if variables["size"] == "222":
        draw222(values, variables, notch=notch, title=title)
    else:
        draw22(values, variables, notch=notch, title=title)