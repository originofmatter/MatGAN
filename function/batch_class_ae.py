import numpy as np


class Dataset():
	"""docstring data Dataset"""
	
	def __init__(self, data, shuffle = True, limited = True, consider_remain = True):

		"""
		shuffle: Boolean
			Whether to disrupt the data
		limited: Boolean
			Whether to stop after all the data is iterated
		consider_remain: Boolean
			Whether to consider residual
		"""		
		self._index_in_epoch = 0
		self._data = data
		self._epochs_completed = 0
		self._num_examples = data.shape[0]
		self.iteration = True
		self.limited = limited
		self.shuffle = shuffle
		self.consider_remain = consider_remain
		self.times = 0
		pass

	def data(self):
		return self._data
	
	def next_batch(self, batch_size):

		"""
		batch_size: Integer
			batch size number

		"""
		self.times += 1
		start = self._index_in_epoch
		if start == 0 and self._epochs_completed == 0:
			idx = np.arange(0, self._num_examples)
			if self.shuffle:
				np.random.shuffle(idx)
				self._data = self._data[idx]
		if self.consider_remain:
			if start + batch_size > self._num_examples:
				data_rest_part = self._data[start:]
				if self.limited:
					self.iteration = False
					return data_rest_part
				else:
					rest_num_examples = self._num_examples - start
					new_start = start + batch_size - self._num_examples
					remain_data = self._data[:new_start]
					self._index_in_epoch = new_start
					return np.concatenate((data_rest_part,remain_data),axis = 0)
			else:
				self._index_in_epoch += batch_size
				end = self._index_in_epoch
				return self._data[start:end]
		else:			
			self._index_in_epoch += batch_size
			end = self._index_in_epoch
			if end + batch_size > self._num_examples:
				self.iteration = False
			return self._data[start:end]
			
