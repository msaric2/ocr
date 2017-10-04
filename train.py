# -*- coding: utf-8 -*-

import caffe
import sys
import numpy as np


file = open('output.log', 'wt')
sys.stdout = file
sys.stderr = file
solver = caffe.get_solver('c:/Users/Matko/PycharmProjects/untitled/caffee/lenet_solver_digits_lettersV8.prototxt')
# solver.restore('c:/Users/Matko/PycharmProjects/untitled/caffee/trainedModelsLetters/_iter_300.solverstate')
solver.solve()


# for i in range(300):
#     solver.step(1)


