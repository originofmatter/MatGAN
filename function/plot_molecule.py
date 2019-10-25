import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def reduce_molecule(molecular_map, periodic_table, tolerate):
	periodic_table = np.loadtxt(periodic_table, dtype = str)
	# for index, molecular in enumerate(molecular_map):
	formula_str, formula_dic = "", dict()
	for ind, one_vec in enumerate(molecular_map):
		for j, num in enumerate(one_vec):
			if (num >= (1 - tolerate)) and (num <= 1):
				formula_str += periodic_table[ind] + str(j + 1)
				formula_dic[periodic_table[ind]] = str(j + 1)

	return formula_str

def plot_molecule(molecule_map, periodic_table, name, path):
	atom_formula = np.loadtxt(periodic_table, dtype = str)
	plt.figure(figsize = (85, 20))
	ax = plt.gca()
	im = ax.imshow(molecule_map, cmap = "Accent_r")
	cbar = ax.figure.colorbar(im, ax = ax, shrink = 0.3, aspect = 20, pad = 0.0005)
	ax.set_xticks(np.arange(8))
	ax.set_yticks(np.arange(atom_formula.shape[0]))
	ax.set_yticklabels(atom_formula)
	for edge, spine in ax.spines.items():
		spine.set_visible(False)
	ax.set_xticks(np.arange(8+1)-.5, minor=True)
	ax.set_yticks(np.arange(atom_formula.shape[0]+1)-.5, minor=True)
	ax.grid(which="minor", color="w", linestyle='-', linewidth = 0.3)
	ax.tick_params(which = "minor", bottom = False, left = False)
	plt.savefig(
			path + str(name)+".png",
			bbox_inches = "tight"
		)



# print(atom_vector)
# print(atom_vector.shape)

# plt.figure(figsize = (80, 20))
# ax = plt.gca()
# im = ax.imshow(atom_vector[:,:20], cmap = "BrBG_r")
# cbar = ax.figure.colorbar(im, ax = ax, shrink = 0.3, aspect = 20, pad = 0.005)

# ax.set_xticks(np.arange(20))
# ax.set_yticks(np.arange(atom_formula.shape[0]))
# ax.set_yticklabels(atom_formula)

# for edge, spine in ax.spines.items():
# 	spine.set_visible(False)
# ax.set_xticks(np.arange(20+1)-.5, minor=True)
# ax.set_yticks(np.arange(atom_formula.shape[0]+1)-.5, minor=True)
# ax.grid(which="minor", color="w", linestyle='-', linewidth = 0.3)
# ax.tick_params(which = "minor", bottom = False, left = False)
# plt.savefig("1.png",bbox_inches = "tight")

