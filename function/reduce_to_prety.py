import os
import sys 
import numpy as np

def load_data(file_path):
	file = open(file_path, "r")
	all_formula = []
	for ind, form in enumerate(file.readlines()):
		# print(ind, form)
		if form == "reduced_cell_formula\n":
			continue
		all_formula.append(eval(form))
	return all_formula

def change_formula(reduce_formula):
	sys.path.append("../")
	metals = np.loadtxt("train_data/Periodic_Table/metals.csv", delimiter = ",", dtype = str)[:,1]
	non_metals = np.loadtxt("train_data/Periodic_Table/non_metals.csv", delimiter = ",", dtype = str)[:,1]
	all_form = []
	for i, formula in enumerate(reduce_formula):
		keys = formula.keys()
		me, me_ind = [], []
		no_me, no_me_ind = [], []
		for key in keys:
			if key in metals:
				index = np.squeeze(np.argwhere(metals == key))
				me.append(key), me_ind.append(int(index))
			elif key in non_metals:
				index = np.squeeze(np.argwhere(non_metals == key))
				no_me.append(key), no_me_ind.append(index)
		me_ind = np.argsort(np.array(me_ind))
		no_me_ind = np.argsort(-1*np.array(no_me_ind))
		
		me = np.array(me)[me_ind]
		no_me = np.array(no_me)[no_me_ind]
		
		form = ""
		for metal in me:
			if formula[metal] == 1:
				form += metal
			else:
				form += (metal + str(formula[metal]))
		for noe_metal in no_me:
			if formula[noe_metal] == 1:
				form += noe_metal
			else:
				form += (noe_metal + str(formula[noe_metal]))
		all_form.append(form)
	return np.array(all_form)

if __name__ == "__main__":
	formula = load_data(os.path.dirname(os.getcwd()) + "/train_data/ICSD/train_formula.csv")
	# print(formula)
	change_formula(formula)