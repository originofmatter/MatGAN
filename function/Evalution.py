import numpy as np

class Evaluating_ML(object):
	def __init__(self):
		self.all_data = []

	def update(self, target, pre):
		target_len = len(target.shape)
		pre_len = len(pre.shape)
		if target_len == 1:
			target = target.reshape(target.shape[0], 1)
		if pre_len == 1:
			pre = pre.reshape(pre.shape[0],1)
		self.target = target
		self.pre = pre
		self.difference = np.subtract(target, pre)
		self.square = np.square(self.difference)
		self.mean = sum(target) / len(target)
		self.all_data.append(
				np.concatenate(
					[self.target, self.pre], 
					axis = 1
				)
			)

	def mae(self):
		result = sum(np.abs(self.difference))/len(self.difference)
		return result[0]

	def mse(self):
		result = sum(self.square) / len(self.difference)
		return result[0]

	def rmse(self):
		return (self.mse())**0.5
	
	def R(self):
		result = 1 - self.mse() / np.var(self.concat()[:,0])
		return result

	def concat(self):
		con = np.concatenate(self.all_data, axis = 0)
		return con

class Evaluating_DL(object):

	def __init__(self):
		self.reset()

	def reset(self):
		self.ab_diff = 0
		self.sq_diff = 0
		self.length = 0
		self.all_data = []

	def update(self, target, pre):
		target_len = len(target.shape)
		pre_len = len(pre.shape)
		if target_len == 1:
			target = target.reshape(target.shape[0], 1)
		if pre_len == 1:
			pre = pre.reshape(pre.shape[0],1)
		self.ab_diff += np.sum(np.abs(target - pre))
		self.sq_diff += np.sum(np.square(target - pre))
		self.length += len(target)
		self.all_data.append(
				np.concatenate(
					[target, pre],
					axis = 1
				)
			)
	def concat(self):
		con = np.concatenate(self.all_data, axis = 0)
		return con

	def mae(self):
		return self.ab_diff / self.length

	def mse(self):
		return self.sq_diff / self.length
	
	def rmse(self):
		return np.sqrt(self.mse()) 
	
	def R(self):
		return 1 - self.mse()/np.var(self.concat()[:,0])
	
	def get_result(self):
		target, pre = self.concat()[:,0], self.concat()[:,1]
		return target, pre

class Loss(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.all_loss = []
	def update(self, loss):
		self.all_loss.append(loss)
	def mean_loss(self):
		return 	np.mean(self.all_loss)

class accuracy(object):
	def __init__(self):
		self.reset()
	def reset(self):
		self.result = []
	def update(self, target, pre):
		# print(pre[:3])
		# print(target[:3])
		self.result.append(
				target == pre
			)
	def acc(self):
		result = np.concatenate(self.result, axis = 0)
		return float(sum(result))/len(result)

class evaluation_gan(object):

	def __init__(self):

		self.total_loss = 0

	def updata(self, g_loss):
		self.total_loss += np.abs(g_loss)

	def reset(self):
		self.total_loss = 0