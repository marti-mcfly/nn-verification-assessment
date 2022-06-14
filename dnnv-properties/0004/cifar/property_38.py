from dnnv.properties import *
import numpy as np

N = Network("N")
x = Image("properties/0004/cifar/image38.npy")
x = x.reshape(N.input_shape[0])

true_class = 9

epsilon = 0.004

Forall(
    x_, Implies(x - epsilon <= x_ <= x + epsilon, np.argmax(N(x_)) == true_class)
)