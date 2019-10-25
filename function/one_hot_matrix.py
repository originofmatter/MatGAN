import numpy as np
import pandas as pd

def one_hot_matrix(formulas, Periodic_table, point_len = 8):
	one_hot_matrix = []
	for ind, formula in enumerate(formulas):
		# formula = eval(formula)
		matrix = np.zeros(
						(1, len(Periodic_table), point_len)
					)
		keys = formula.keys()
		for symbols in keys:
			symbols_index = list(Periodic_table).index(symbols)
			matrix[0, symbols_index, int(formula[symbols]) - 1] = 1
		one_hot_matrix.append(matrix)
	one_hot_matrix = np.concatenate(one_hot_matrix, axis = 0)
	return one_hot_matrix

def get_one_hot_matrix(formulas, Periodic_table, point_len):
	periodictable_symbols = np.loadtxt(Periodic_table, dtype = str)
	matrix = one_hot_matrix(
					formulas = formulas, 
					Periodic_table = periodictable_symbols,
					point_len = point_len
				)
	return matrix
