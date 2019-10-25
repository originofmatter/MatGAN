import numpy as np
import matplotlib.pyplot as plt

class Oversampling(object):

	def __init__(self, x, y, bins = 100, plot = False):
		self.feature = x
		self.target = y
		self.In_numb = bins
		self.n, self.bins = np.histogram(y, bins = self.In_numb , density = False)
		self.over_sample_x = []
		self.over_sample_y = []
		self.over_sample_x_median = []
		self.over_sample_y_median = []


		self.plot = plot
		self.reduce_index = []
		if self.plot:
			ax = plt.gca()
			ax.spines["top"].set_visible(False)
			ax.spines["right"].set_visible(False)
			plt.bar(left = self.bins[:-1], height = self.n, width = 1)
			plt.show()

	def uniform_sample_max(self):
		n_max = self.n.max()
		for ind, n in enumerate(self.n):
			add_sample = n_max - n
			if add_sample == 0:
				continue
			else:
				multiple = int(add_sample // n)
				remainder = add_sample % n
				subset = []
				for i, ys in enumerate(self.target):
					if ys > self.bins[ind] and ys < self.bins[ind+1]:
						subset.append(i)
				for time in range(multiple):
					for index in subset:
						self.over_sample_x.append(self.feature[index])
						self.over_sample_y.append(self.target[index])
				slect = np.arange(remainder)
				np.random.shuffle(slect)
				for index in np.array(subset)[slect]:
					self.over_sample_x.append(self.feature[index])
					self.over_sample_y.append(self.target[index])
		self.feature = np.concatenate((self.feature, self.over_sample_x), axis = 0)
		self.target = np.concatenate((self.target, self.over_sample_y))
		shuffle_ind = np.arange(self.feature.shape[0])
		np.random.shuffle(shuffle_ind)
		if self.plot:
			n, bins = np.histogram(self.target[shuffle_ind], bins = self.In_numb , density = False)
			ax = plt.gca()
			ax.spines["top"].set_visible(False)
			ax.spines["right"].set_visible(False)
			plt.bar(left = bins[:-1], height = n, width = 1)
			plt.show()
		return self.feature[shuffle_ind], self.target[shuffle_ind]

	def uniform_sample_median(self):
		median = np.median(self.n)
		for ind, n in enumerate(self.n):
			sample =  n - median
			if sample == 0 or n == 0:
				continue
			if sample > 0:
				reduce_sample = sample
				reduce_ind = []
				for i, ys in enumerate(self.target):
					if ys > self.bins[ind] and ys < self.bins[ind+1]:
						reduce_ind.append(i)
				select_reduce = np.arange(reduce_sample, dtype = int)
				np.random.shuffle(select_reduce)
				reduce_ind = np.array(reduce_ind)[select_reduce]
				self.reduce_index.append(reduce_ind)
			if sample < 0:
				add_sample = -1 * sample
				multiple = int(add_sample // n)
				remainder = add_sample % n
				subset = []
				for i, ys in enumerate(self.target):
					if ys > self.bins[ind] and ys < self.bins[ind+1]:
						subset.append(i)
				for time in range(multiple):
					for index in subset:
						self.over_sample_x_median.append(self.feature[index])
						self.over_sample_y_median.append(self.target[index])
				slect = np.arange(remainder,dtype = int)
				np.random.shuffle(slect)
				for index in np.array(subset)[slect]:
					self.over_sample_x_median.append(self.feature[index])
					self.over_sample_y_median.append(self.target[index])
		self.reduce_index = np.concatenate(self.reduce_index, axis = 0)
		self.feature = np.delete(self.feature, self.reduce_index, axis = 0)
		self.target = np.delete(self.target, self.reduce_index, axis = 0)
		self.feature = np.concatenate((self.feature, self.over_sample_x_median), axis = 0)
		self.target = np.concatenate((self.target, self.over_sample_y_median))
		shuffle_ind = np.arange(self.feature.shape[0])
		np.random.shuffle(shuffle_ind)
		if self.plot:
			n, bins = np.histogram(self.target[shuffle_ind], bins = self.In_numb , density = False)
			ax = plt.gca()
			ax.spines["top"].set_visible(False)
			ax.spines["right"].set_visible(False)
			plt.bar(left = bins[:-1], height = n, width = 1)
			plt.show()
		return self.feature[shuffle_ind], self.target[shuffle_ind]
