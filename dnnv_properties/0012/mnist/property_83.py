from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image("properties/0012/mnist/image83.npy")
x = x.reshape(N.input_shape[0])

true_class = 7

epsilon = 0.012

Forall(
    x_, Implies(x - epsilon <= x_ <= x + epsilon, np.argmax(N(x_)) == true_class)
)