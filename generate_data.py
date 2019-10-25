"""
@author: YaboDan
@file: generate_data.py
"""
import os
import numpy as np
import pandas as pd
import argparse
import tensorflow as tf

from function.batch_class_ae import Dataset
from function.Config import Config
from function.Config import args
from function.reduce_to_prety import change_formula
import pymatgen as mg

def load_data(file_path):
	if not os.path.exists(file_path):
		myfile = open(file_path, "w")
		myfile.close()
	file = open(file_path, "r")
	all_formula = []
	for ind, form in enumerate(file.readlines()):
		if form == "reduced_cell_formula\n":
			continue
		comp = mg.Composition(form)
		reduce_formula = comp.get_el_amt_dict()
		for key in reduce_formula.keys():
			reduce_formula[key] = int(reduce_formula[key])
		all_formula.append(reduce_formula)
	return all_formula

def remove_redundancy(formula):
	re_formula = []
	for i, form in enumerate(formula):
		if form not in re_formula:
			re_formula.append(form)
	return re_formula

class generator_molecule(args):

	def __init__(self, config, database):
		if database == "OQMD":
			from gan_model.WGANGP_OQMD import GAN
		elif database == "MP":
			from gan_model.WGANGP_MP import GAN
		elif database == "ICSD":
			from gan_model.WGANGP_ICSD import GAN
		elif database == "Bandgap":
			from gan_model.WGANGP_Signal import GAN
		elif database == "ICSD_Filter":
			from gan_model.WGANGP_Signal import GAN

		super(generator_molecule, self).__init__(config, database)
		self.periodic_table = config.periodic_table
		self.tolerate = config.tolerate
		self.net = GAN(config, database, is_train = False)
		saver = tf.train.Saver()
		self.sess = tf.Session()
		saver.restore(self.sess, "check_point/iMatGAN/" + database + "/model.ckpt")

	def generator_mo(self):
		random = np.random.normal(
						loc = 0, 
						scale = 1, 
						size = [self.batch_size, 128]
					)
		generate_sample = self.sess.run(
								self.net.fake_data, 
								feed_dict = {
									self.net.random : random
								}
							)
		return generate_sample

	def reset_net(self):
		tf.reset_default_graph()

	def __call__(self, times):
		gen_molecule = []
		for i in range(times):
			molecule_mp = self.generator_mo()
			gen_molecule.append(molecule_mp)
		gen_molecule = np.concatenate(gen_molecule, axis = 0)
		_, formula = reduce_molecule(
					molecular_map = np.squeeze(gen_molecule), 
					periodic_table = self.periodic_table, 
					tolerate = self.tolerate
				)
		return gen_molecule, formula

def reduce_molecule(molecular_map, periodic_table, tolerate):
	periodic_table = np.loadtxt(periodic_table, dtype = str)
	all_for_str, all_for_dic = [], []
	for index, molecular in enumerate(molecular_map):
		formula_str, formula_dic = "", dict()
		for ind, one_vec in enumerate(molecular):
			for j, num in enumerate(one_vec):
				if (num >= (1 - tolerate)) and (num <= 1):
					formula_str += periodic_table[ind] + str(j + 1)
					formula_dic[periodic_table[ind]] = j + 1
		all_for_str.append(formula_str)
		all_for_dic.append(formula_dic)
	return np.array(all_for_str), np.array(all_for_dic)

class screen_data(object):
	
	def filter_data(self, formulas):
		filter_formula = []
		for ind, formula in enumerate(formulas):
			condition = formula != {} \
						and len(formula.keys()) > 1\
						and len(formula.keys()) <= 8
			if condition:
				filter_formula.append(formula)

		re_filter_formula = self.remove_redundancy(filter_formula)
		return re_filter_formula, len(re_filter_formula)/len(filter_formula), len(filter_formula)/len(formulas)

	def remove_redundancy(self, formula):
		re_formula = []
		for i, form in enumerate(formula):
			if form not in re_formula:
				re_formula.append(form)
		return np.array(re_formula)

class save_data(args):

	def __init__(self, config, database, gen_data):
		self.gen_material = load_data(gen_data)
		self.gen_data = gen_data
	def update_material(self, formulas):

		for material in formulas:
			if material not in self.gen_material:
				self.gen_material.append(material)
		return self.gen_material

	def __call__(self):
		self.gen_material = change_formula(self.gen_material)
		np.savetxt(self.gen_data, self.gen_material, fmt = "%s")

def main(config, database, gen_data):

	arg = args(config, database)
	Generator = generator_molecule(config, database)
	gen_molecule, gen_formula = Generator(int(config.gen_num/arg.batch_size))
	Generator.reset_net()

	Screen_data = screen_data()
		
	formula, unique_rate, unique_gen_rate = Screen_data.filter_data(gen_formula)

	Save_data = save_data(config, database, gen_data)

	material = Save_data.update_material(formula)

	Save_data()

	print("generted unique material number {}".format(len(material)))

def parse_args():

	parser = argparse.ArgumentParser() 
	parser.add_argument("database", choices = ["OQMD", "ICSD", "ICSD_Filter", "Bandgap", "MP"], type = str, 
							help = "Accoinding to database to generate data")
	parser.add_argument("gen_data", type = str, help = "the path to save generated data")

	return parser.parse_args()

if __name__ == "__main__":
	config = Config()
	main(config, parse_args().database, parse_args().gen_data)


