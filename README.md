The companion repository to the paper 

**Critically Assessing the State of the Art in Neural Network Verification**, Matthias König, Annelot W Bosman, Holger H Hoos, Jan N van Rijn, *submitted*. 

**Abstract:** Recent works have proposed methods to formally verify neural networks against minimal input perturbations. This type of verification is referred to as local robustness verification. The field of local robustness verification is highly diverse, as verifiers rely on a multitude of techniques, such as Mixed Integer Programming or Satisfiability Modulo Theories. At the same time, problem instances differ based on the network that is verified, the network input or the verification property. This gives rise to the question of which verification algorithm is most suitable to solve a given verification problem. To answer this question, we perform an extensive analysis of current evaluation practices for local robustness verifiers as well as an empirical performance assessment of several verification methods across a broad set of neural networks and properties. Most notably, we find that most algorithms only support ReLU-based networks, while other activation functions remain under-supported. Furthermore, we show that there is no single best algorithm that dominates in performance across all problem instances and illustrate the potential of using algorithm portfolios for more efficient local robustness verification.

This repository provides

- the performance data collected for this study;
- the scripts we used to perform the data analysis;
- an overview of the used software;
- the neural network files we employed to verifiers to.

# Data

Contains all collected performance data. The ```cpu``` sub-folder contains the individual ```.csv``` files separating between MNIST and CIFAR as well as network category, and contains performance data for all considered verifiers, epsilons, networks in the given category and test images. The data file further contains the total running time and whether the verification problem instance was found to be sat/unsat or unsolved. The ```gpu``` folder is structured similarly.

# Scripts

In ```scripts```, you can find ```tables_and_figures.py``` - this script can be used to reproduce all result related figures and tables as seen in the paper and appendix.

## Input

The input for this script consists of all ```.csv``` files found in ```performance_data```. 

## Output

Firstly, analysis results (in ```contribution_results```) consisting of standalone performance per verifier, absolute marginal contribution, relative marginal contribution, shapley value, average running time over all instances that could be solved by at least one verifier and average running time over all instances that could be solved by all verifiers. The contribution results are seperated by CPU/GPU methods and network category.
Secondly, CDF plots, which can be found in ```figures/cdf```. For each network category and GPU/CPU group a CDF plot is created, as long as there are more than two verifiers in the given category.
Thirdly, scatter plots which can be found in ```figures/scatter_plots```. For CPU/GPU seperated for each combination of verifiers in each network category a scatterplot is created. The data points indicate the running time in CPU/GPU seconds for each instance.
All output is seperated by category, CPU/GPU and MNIST/CIFAR.

# Software 

## Required tools

CPU methods: 
- DNNV version 0.4.8 (Interface to employ BaB, Marabou, Neurify, nnenum and Verinet; https://github.com/dlshriver/dnnv)

GPU methods:
- ERAN-GPUPoly (https://github.com/eth-sri/eran)
- OVAL-BaDNB (https://github.com/oval-group/oval-bab)
- beta-CROWN (https://github.com/huanzhang12/alpha-beta-CROWN)

## Tool usage

After installing the tools, you can use them to verify the networks in ```networks``` on the instances found in ```mnist_test.csv``` and ```cifar10_test.csv```. Note that we used a time budget of 3 600 seconds and set the number of CPU cores to 1 when running a verifier.

### DNNV
DNNV takes as inputs the network file and a property specification. These specifications can be found in ```dnnv-properties```. 
For example, employing Verinet through DNNV to verify mnist-net.onnx network on the first MNIST image with epsilon=0.004 can be done via the following command:

```dnnv --network N /your/path/to/networks/mnist/mnist-net.onnx /your/path/to/dnnv-properties/0004/mnist/property0.py --verinet```



### ERAN-GPUPoly
Using ERAN-GPUPoly to verify the mnist-net.onnx network on the first 100 MNIST images with epsilon=0.004 can be done via the following command:

```--netname /your/path/to/networks/mnist/mnist-net.onnx --epsilon 0.004 --domain deeppoly --dataset <mnist> --complete True --numproc 1```


### OVAL-BaDNB
The OVAL-BADNB framework provides ```local_robustness_from_onnx.py``` script that takes an input the network file. Inside the script, you can set the pertubation radius as well as the dataset (MNIST or CIFAR) and image index. Example command:

```python /your/path/to/local_robustness_from_onnx.py --network_filename /your/path/to/networks/mnist/mnist-net.onnx```

### beta-CROWN
beta-CROWN is employed on the network files provided in their repository. However, we set all hyper-parameters to default; see the ```.yaml``` files in ```beta-CROWN-configurations```. Using these configuration files, running beta-CROWN can be done through the following command, where the network, dataset and epsilon is also specified in the ```.yaml``` file:

```python /your/path/to/robustness_verifier.py --config config.yaml```

# Networks

Network files were obtained from the public repositories of [ERAN](https://github.com/eth-sri/eran), [Marabou](https://github.com/NeuralNetworkVerification/Marabou), [MIPVerify](https://github.com/vtjeng/MIPVerify.jl) (manually converted to onnx), [Venus](https://github.com/vas-group-imperial/venus), [Verinet](https://github.com/vas-group-imperial/VeriNet) and the [2021 VNN Competition](https://github.com/stanleybak/vnncomp2021). 

Some network files could not be parsed by any of the considered tools and have been removed from consideration. The final list of networks for both MNIST and CIFAR can be found in ```networks```, along with their main properties (i.e., the layer operations they employ). 
