from function.reduce_to_prety import change_formula
import numpy as np
def load_data(file_path):

	file = open(file_path, "r")
	all_formula = []
	for ind, form in enumerate(file.readlines()):
		if form == "reduced_cell_formula\n":
			continue
		all_formula.append(eval(form))

	return all_formula

def main():
	formula = load_data("train_data/OQMD/formula_not.csv")
	formula = change_formula(formula)
	np.savetxt("train_data/OQMD/non-decodable.csv", formula, fmt = "%s")

if __name__ == "__main__":
	main()
