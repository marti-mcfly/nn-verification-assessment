The companion repository to the paper 

**Critically Assessing the State of the Art in Neural Network Verification**, Matthias König, Annelot W Bosman, Holger H Hoos, Jan N van Rijn, *submitted*. 

**Abstract:** Recent works have proposed methods to formally verify neural networks against minimal input perturbations. This type of verification is referred to as local robustness verification. The field of local robustness verification is highly diverse, as verifiers rely on a multitude of techniques, such as Mixed Integer Programming or Satisfiability Modulo Theories. At the same time, problem instances differ based on the network that is verified, the network input or the verification property. This gives rise to the question of which verification algorithm is most suitable to solve a given verification problem. To answer this question, we perform an extensive analysis of current evaluation practices for local robustness verifiers as well as an empirical performance assessment of several verification methods across a broad set of neural networks and properties. Most notably, we find that most algorithms only support ReLU-based networks, while other activation functions remain under-supported. Furthermore, we show that there is no single best algorithm that dominates in performance across all problem instances and illustrate the potential of using algorithm portfolios for more efficient local robustness verification.

This repository provides

- the performance data collected for this study;
- the scripts we used to perform the data analysis;
- an overview of the used software;
- the neural network files we employed to verifiers to.

# Data

# Scripts

# Software 

## Tools used

- DNNV version 0.4.8 (https://github.com/dlshriver/dnnv)
- ERAN-GPUPoly (https://github.com/eth-sri/eran)
- OVAL-BaB (https://github.com/oval-group/oval-bab)
- ab-CROWN (https://github.com/huanzhang12/alpha-beta-CROWN)

## Tool usage

# Networks
