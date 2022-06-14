from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image("properties/0008/cifar/image93.npy")
x = x.reshape(N.input_shape[0])

true_class = 6

epsilon = 0.005

Forall(
    x_, Implies(x - epsilon <= x_ <= x + epsilon, np.argmax(N(x_)) == true_class)
)