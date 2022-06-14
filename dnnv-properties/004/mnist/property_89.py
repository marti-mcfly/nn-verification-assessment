from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image("properties/004/mnist/image89.npy")
x = x.reshape(N.input_shape[0])

true_class = 1

epsilon = 0.04

Forall(
    x_, Implies(x - epsilon <= x_ <= x + epsilon, np.argmax(N(x_)) == true_class)
)