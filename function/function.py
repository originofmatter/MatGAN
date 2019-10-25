import numpy as np


class Normalizer(object):
	def __init__(self,data):
		data=data.astype(np.float32)		
		self.mean=np.mean(data,axis=0)
		self.std=np.std(data,axis=0)

	def norm(self,data):
		data=data.astype(np.float32)
		return (data - self.mean) / self.std

	def denorm(self,data):		
		data=data.astype(np.float32)
		return data * self.std + self.mean

	def state_dict(self):
		return {"mean": self.mean,
				"std": self.std}

	def load_state_dict(sefl, state_dict):
		self.mean = state_dict["mena"]
		self.std = state_dict["std"]

class Scaling(object):
	def __init__(self, data):
		self.max = np.max(data)
		self.min = np.min(data)

	def scal(self, data):
		data = (data - self.min) / (self.max - self.min)
		return data

	def descal(self, data):
		data = data * (self.max - self.min) + self.min
		return data

	def state_dict(self):
		return {"max": self.max,
				"min": self.min}

	def load_state_dict(self, state_dict):
		self.max = state_dict["max"]
		self.min = state_dict["min"]

class Iny(object):
	def In(self, data):
		data = np.log(data)
		return data
	
	def deIn(self, data):
		data = np.exp(data)
		return data