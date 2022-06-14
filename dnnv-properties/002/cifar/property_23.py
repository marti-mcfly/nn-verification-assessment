from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image("properties/002/cifar/image23.npy")
x = x.reshape(N.input_shape[0])

true_class = 9

epsilon = 0.02

Forall(
    x_, Implies(x - epsilon <= x_ <= x + epsilon, np.argmax(N(x_)) == true_class)
)