import glob
from re import X
import pandas as pd
import numpy as np
import itertools
import json
import os
import copy 
import itertools 
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib 
import itertools


def get_marginal_contribution(data, coalition, score):
    '''
    This methods returns the marginal contributions for all the verifiers in the coalition for this category.

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    score: the total coalition score
    
    OUTPUT:
    res: output dictionary where the name of the verifier maps to the marginal contribution
    ''' 
    res ={}

    for i in coalition: 
        temp = data[data.Verifier != i]
        temp = temp.sort_values(by=['score'], ascending= False)
        temp.drop_duplicates(subset= ['instance'], inplace=True) #, keep = 'first')
        # print("marginal contribution " ,i , " is: " , score -  temp['score'].sum())
        res[i] =  score -  temp['score'].sum()
    return res

def get_total_coalition_score(data):
    '''
    This methods returns the total coalition score.

    INPUT:
    data: pandas with the experimental results, cleaned
    
    OUTPUT:
    the total coaltion score. 
    '''  
    best = copy.copy(data)
    best.sort_values(by=['score'], ascending= False)
    best.drop_duplicates(subset= ['instance'], inplace=True) 
    best = best[(best.Result == "sat") | (best.Result == "unsat") |(best.Result == "unsat/sat")  ] 
    # print("the coaltion score is " , best['score'].sum())
    return best['score'].sum()


def get_standalone(data, coalition):
    '''
    This methods returns the standalone score for all the verifiers in the coalition for this category.

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    
    OUTPUT:
    res: output dictionary where the name of the verifier maps to the standalone score of the verifier.
    ''' 
    res = {}
    for i in coalition: 
        temp = data[data.Verifier == i]
        res[i] = temp['score'].sum()
        # print("Standalone " , i , " is: " , temp['score'].sum())
    return res

def get_num_solvable(instances):
    print("the number of solvable instances is: " + len(instances))

def get_average_runtime(coalition, data):
    '''
    This methods returns the average run-time for each verifier.

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    
    OUTPUT:
    run_time: output dictionary where the name of the verifier maps to the average runtime
    ''' 
    run_time = {}
    for i in coalition:
        temp =data[data.Verifier ==i]
        run_time[i] = [temp.TotalTime.sum() / len(temp)]
    return run_time

def get_all_runtime(coalition, data):
    '''
    This methods returns the average run-time for each verifier for those instances that are solvable by all verifiers.

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    
    OUTPUT:
    runtime: output dictionary where the name of the verifier maps to the average runtime over those instances that are solvable by all verifiers.
    ''' 
    runtime = {}
    best = copy.copy(data)
    best = best.sort_values(by=['TotalTime'], ascending = False)
    best.drop_duplicates(subset= ['instance'], inplace=True)
    best = best[best.TotalTime < 3600]

    instances = (best['Image'].astype(str) +" " + best['Network'].astype(str) + " " +best['Epsilon'].astype(str) ).tolist()
    print("instances solved all", len(instances))
    data = data[data['instance'].isin(instances)]
  

    for i in coalition:
        temp = data[data.Verifier == i]
        if(len(temp) > 0):
            runtime[i] = [temp['TotalTime'].sum()/ len(temp)]
        else:
            runtime[i] = None

    return runtime
def get_solved_method(coalition, data):
    '''
    This methods returns the number of instances each verifier solved in the category.

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    
    OUTPUT:
    solved: output dictionary where the name of the verifier maps to the number of solved instances.
    ''' 
    solved = {}
    for i in coalition:
        temp =data[data.Verifier ==i]
        solved[i] = [temp.solved.sum() ]
    return solved

def get_Shapley_values(coalition, data):
    '''
    This methods returns the shapley value for all the verifiers in the coalition for this category.

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    
    OUTPUT:
    shapley: output dictionary where the name of the verifier maps to the shapley value
    ''' 

    combs = getCombs(coalition)

    all_scores = {}
    for i in combs : 
        temp_data =data[data['Verifier'].isin(i)]
        score = get_total_coalition_score(temp_data)
        all_scores[str(i)] =score

    n =len(coalition)

    shapley = {}

    for i in coalition:
        temp= 0 
        for j in combs:
            if ((i in j)):
                if(len(j)>1): 
                    k = [x for x in j if x != i]
                    # print(k, all_scores[str(k)])
                    temp = temp +  (n-1)*(all_scores[str(j)]- all_scores[str(k)])
                else:
                    temp = temp + all_scores[str(j)]
        
        shapley[i] = temp/math.factorial(n)
    return shapley

def getCombs(coalition):
    '''
    This methods returns a list of combinations of the verifiers in the category. 

    INPUT:
    coalition: the verifiers to be tested in the current category
    
    OUTPUT:
    combs    : a list of combinations of verifiers in the coalition in the category.
    Each entry of the list consists of a list with atleast one verifier name. 
    ''' 
    combs =[]

    for i in coalition:
        combs.append([i])

    for i in range(2, len(coalition)+1):
       temp = itertools.combinations(coalition, r=i)
       for j in temp:
           combs.append(list(j))
      
    # permutations = list(itertools.permutations(combs))
    return combs


def cdf_per_method(coalition, data,name, names, gpu):
    '''
    This methods creates and safes a CDF plot of the coalition for the category. 

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    name: the name the plot should have
    names : a list of strings containing the names of verifiers as used in the paper
    gpu: boolean that is True if the category is a gpu category and False otherwise. 
    
    OUTPUT:
 
    ''' 
    plt.figure(figsize=(12,12))

    temp_names =[]
    for i in coalition:
        temp = data[data.Verifier == i]
        if(len(temp )>0 ):
            sns.ecdfplot(temp['TotalTime'], log_scale=True , palette="deep")
            temp_names.append(i)

    plt.legend(names)
    if(gpu == True):
        plt.xlabel("GPU time [s]")
    else:
        plt.xlabel("CPU time [s]")

    plt.ylabel("Fraction of instances solved")
    # plt.title(title)
    plt.savefig( 'figures/cdf/'+ name + '.pdf',
                        format='pdf',dpi=150)

def scatter_per_method(coalition, data, name, names,gpu):
    '''
    This creates and safes scatterplots of each combination of two verifiers in the coalition. 
    The scatterpoints consist of the solving time. 

    INPUT:
    data: pandas with the experimental results, cleaned
    coalition: the verifiers to be tested in the current category
    name: the name the plot should have
    names : a list of strings containing the names of verifiers as used in the paper
    gpu: boolean that is True if the category is a gpu category and False otherwise.
    
    OUTPUT:

    ''' 
    for i in range(0, len(coalition)-1):
        for j in range(i+1, len(coalition)):
            x = name + "_" + coalition[i] + "_" + coalition[j] + ".pdf"
            data = data.sort_values(by=['instance'], ascending= False)
            if (len(data[data.Verifier ==coalition[i]]['TotalTime'].tolist())== len(data[data.Verifier ==coalition[j]]['TotalTime'].tolist())):
 
                temp = pd.DataFrame(data = {coalition[i] :data[data.Verifier ==coalition[i]]['TotalTime'].tolist(), coalition[j]: data[data.Verifier ==coalition[j]]['TotalTime'].tolist()} ) 
                sns.set(font_scale=2)
                sns.set_style({'font.family':'serif', 'font.serif':'Times New Roman'})
                # sns.set_style("whitegrid")
                plt.figure(figsize=(12,12))
                ax = sns.scatterplot(data = temp, x = coalition[i] ,y= coalition[j] , palette="deep")
                plt.plot([10e4, 0], [10e4, 0], linewidth=1)
            
                ax.set(xscale="log", yscale="log")
                ax.set(xlim=(10e-4, 10e4))
                ax.set(ylim=(10e-4, 10e4))
                if(gpu == True):
                    ax.set(xlabel= "GPU time [s], " + names[i], ylabel="GPU time [s], " + names[j])
                else:
                    ax.set(xlabel= "CPU time [s], " + names[i], ylabel="CPU time [s], " + names[j])

                # plt.title(x)
                plt.savefig('figures/scatter_plots/' + x , format = 'pdf' )
                plt.show()
            
def get_names_and_files(benchmark, categorie):
    '''
    This method returns the data for a categorie and benchmark as well as a list of the names as used in the paper, 
    this is needed for the plot titles. 

    INPUT:
    benchmark: the name of the benchmark, this is either "cifar" or "mnist" in the current research. 
    categorie : list of names of verifiers in the coalition of this categorie, these are the names as indicated in the data. 
   
    OUTPUT:
    names : list of names for the benchmark+categorie verifiers as used in the paper
    file  :  pandas dataframe containing the result data for a specific benchmark + categorie. 
    '''
    if("Relu+Maxpool"  in categorie):
        if(benchmark == "mnist"):
            if("gpu" in categorie):
                names = ["BaDNB", "GPUPoly"]
                file = pd.read_csv('performance_data/gpu/GPU_MNIST_MAXPOOL_0002.csv')
                return names, file
            else:
                names = [ "Marabou"]
                file = pd.read_csv('performance_data/cpu/cpu_mnist_Relu+Maxpool.csv')
                return names, file
        elif(benchmark == "cifar"):
            if("gpu" in categorie):
                names = ["BaDNB", "GPUPoly"]
                file = pd.read_csv('performance_data/gpu/GPU_CIFAR_MAXPOOL_0002.csv')
                return names, file
            else:
                names = ["Marabou"]
                file = pd.read_csv('performance_data/cpu/cpu_cifar_Relu+Maxpool.csv')
                return names, file
    elif("Tanh"  in categorie):
        if(benchmark == "mnist"):
            if("gpu" in categorie):
                names = [ "GPUPoly"]
                file = pd.read_csv('performance_data/gpu/GPU_MNIST_TANH_0002.csv')
                return names, file
            else:
                names = ["Verinet"]
                file = pd.read_csv('performance_data/cpu/cpu_mnist_Tanh.csv')
                return names, file
        elif(benchmark == "cifar"):
            if("gpu" in categorie):
                names = [ "GPUPoly"]
                file = pd.read_csv('performance_data/gpu/GPU_CIFAR_TANH_0002.csv')
                return names, file
            else:
                names = ["Verinet"]
                file = pd.read_csv('performance_data/cpu/cpu_cifar_Tanh.csv')
                return names, file
    elif("Sigmoid" in categorie):
        if(benchmark == "mnist"):
            if("gpu" in categorie):
                names = [ "GPUPoly"]
                file = pd.read_csv('performance_data/gpu/GPU_MNIST_SIGMOID_0002.csv')
                return names, file
            else:
                names = ["Marabou",  "Verinet"]
                file = pd.read_csv('performance_data/cpu/cpu_mnist_Sigmoid.csv')
                return names, file
        elif(benchmark == "cifar"):
            if("gpu" in categorie):
                names = ["GPUPoly"]
                file = pd.read_csv('performance_data/gpu/GPU_CIFAR_SIGMOID_0002.csv')
                return names, file
            else:
                names = [ "Marabou",  "Verinet"]
                file = pd.read_csv('performance_data/cpu/cpu_cifar_Sigmoid.csv')
                return names, file
    elif ("Relu" in categorie):
        if(benchmark == "mnist"):
            if("gpu" in categorie):
                names = ["BaDNB", "GPUPoly", "beta-CROWN"]
                file = pd.read_csv('performance_data/gpu/GPU_MNIST_RELU_0002.csv')
                return names, file
            else:
                names = ["BaBSB", "Marabou", "Neurify","nnenum",  "Verinet"]
                file = pd.read_csv('performance_data/cpu/cpu_mnist_Relu.csv')
                return names, file
        elif(benchmark == "cifar"):
            if("gpu" in categorie):
                names = ["BaDNB", "GPUPoly", "beta-CROWN"]
                file = pd.read_csv('performance_data/gpu/GPU_CIFAR_RELU_0002.csv')
                return names, file
            else:
                names = ["BaBSB", "Marabou", "Neurify","nnenum",  "Verinet"]
                file = pd.read_csv('performance_data/cpu/cpu_cifar_Relu.csv')
                return names, file


def get_csv_for_all(benchmarks, categories): 
    '''
    This function created csv for each of the indicates categories and benchmarks, 
    consisting of marginal contribution, shapley value, standalone, average runtime and average runtime over the instances solvable by all in the coalition. 
    It also calls the functions for the scatterplot and CDF plots. 

    INPUT:
    benchmarks: list of strings of the benchmarks that need to be tested. 
    categories: dictionary which maps the categorie name to a list of verifier names as indicated in the data. 


    OUTPUT:

    ''' 
    

    for i in categories:
        coalition = categories[i]
        df = pd.DataFrame(columns = coalition)
        for j in benchmarks:
            print("this is categorie ", i, " and benchmark ", j)
            names, data = get_names_and_files(j, i)
            if(len(data) >0):
                x =  get_standalone(data, coalition)
                temp = pd.DataFrame(x, index=[ j + " standalone"])
                df = pd.concat([df, temp])
            
                score = get_total_coalition_score(data)
                x = get_marginal_contribution(data, coalition, score)
                temp = pd.DataFrame(x, index=[ j + " marginal contribution"])
                df = pd.concat([df, temp])
                
                x = get_Shapley_values(coalition, data)
                temp = pd.DataFrame(x, index=[ j + " shapley values"])
                df = pd.concat([df, temp])
                
                x = get_solved_method( coalition, data)
                temp = pd.DataFrame(x, index=[ j + " number solved"])
                df = pd.concat([df, temp])

                x = get_average_runtime( coalition, data)
                temp = pd.DataFrame(x, index=[ j + " Average runtime"])
                df = pd.concat([df, temp])
                
                x = get_all_runtime(coalition, data)
                temp = pd.DataFrame(x, index=[ j + " All runtime"])
                df = pd.concat([df, temp])
                
                # '''Make the plot'''
                gpu = False
                if("gpu" in i ):
                    gpu = True
                scatter_per_method(coalition, data, i + "_" + j, names, gpu)
                cdf_per_method(coalition, data, i + "_" + j+ ".pdf", names, gpu)

        df =df.T
        df.to_csv('contribution_results/'+ i + ".csv")




# ''''Here the main part starts!!'''

benchmarks = ["mnist", "cifar" ] #, "all"]
categories ={ "cpu_Relu"           :["babsb", "marabou", "neurify","nnenum",  "verinet"],
              "cpu_Sigmoid"        :["marabou", "verinet"],
              "cpu_Relu+Maxpool"   :["marabou"], 
              "cpu_Tanh"           :["verinet"],  
              "gpu_Relu"           :["bab","eran", "abcrown"],
              "gpu_Sigmoid"        :["eran"],
              "gpu_Relu+Maxpool"   :["bab", "eran"], 
              "gpu_Tanh"           :["eran"]}



'''When running this, the results for all the benchmarks and categories will be created. 
   #TODO: Make sure the directory names as indicated in get_names_and_files match yours.
    '''
get_csv_for_all(benchmarks, categories)


'''If you'd like partial results see code here as example'''

# #only mandatory step!
# names, data = get_names_and_files("mnist" , categories["cpu_Relu"])

# #get shapley values
# print(get_Shapley_values( categories["Relu"], data))
# #get cdf for this categorie
# cdf_per_method( data, "test_cdf" ,names, False)