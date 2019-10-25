"""
@author: 
@file: Produce_New_Materials.py
"""

import tensorflow as tf
from function.Config import args

def linear(input, output_dim, scope = None, name = None, stddev = 1.0):
	with tf.variable_scope(scope or "linear"):
		w = tf.get_variable(
				name = "w",
				shape = [input.get_shape()[1], output_dim], 
				initializer = tf.random_normal_initializer(stddev = stddev)
			)
		b = tf.get_variable(
				name = "b",
				shape = [output_dim],
				initializer = tf.constant_initializer(0.0)
			)
	return tf.add(tf.matmul(input, w), b, name = name)

def cnn2d(input, filter_shape, strid_shape, padding, scope = None, name = None, stddev = 1.0):
	with tf.variable_scope(scope or "cnn"):
		w = tf.get_variable(
				name = "w",
				shape = filter_shape,
				initializer = tf.random_normal_initializer(stddev = stddev)
			)
		b = tf.get_variable(
				name = "b",
				shape = filter_shape[-1],
				initializer = tf.constant_initializer(0.0)
			)
	return tf.add(
				tf.nn.conv2d(
					input = input, 
					filter = w,
					strides = strid_shape,
					padding = padding
				),
				b,
				name = name
			)
def decnn2d(input, filter_shape, output_shape, strid_shape, padding, scope = None, name = None, stddev = 1.0):
	with tf.variable_scope(scope or "decnn"):
		w = tf.get_variable(
				name = "w",
				shape = filter_shape,
				initializer = tf.random_normal_initializer(stddev = stddev)
			)
		b = tf.get_variable(
				name = "b",
				shape = filter_shape[-2],
				initializer = tf.constant_initializer(0.0)
			)

	return tf.add(
				tf.nn.conv2d_transpose(
					value = input,
					filter = w,
					output_shape = output_shape,
					strides = strid_shape,
				),
				b,
				name = name
			)

def bn_layer(x, is_training, scope = None, name = None, moving_decay = 0.9, eps = 1e-5):
	param_shape = x.get_shape()[-1]
	with tf.variable_scope(scope or "BatchNorm"):
		gamma = tf.get_variable(
					name = "gamma",
					shape = param_shape,
					initializer = tf.constant_initializer(1)
				)
		beta = tf.get_variable(
					name = "beat",
					shape = param_shape,
					initializer = tf.constant_initializer(0)
				)
		axis = list(range(len(x.get_shape()) - 1))
		batch_mean, batch_var = tf.nn.moments(
				x, 
				axis, 
				name = "moments"
			)		
		ema = tf.train.ExponentialMovingAverage(
					decay = moving_decay,
					name = "ExponentialMovingAverage"
				)
		def mean_var_with_update():
			ema_apply_op = ema.apply([batch_mean, batch_var])
			with tf.control_dependencies([ema_apply_op]):
				return tf.identity(batch_mean), tf.identity(batch_var)

		mean, var = tf.cond(
						pred = tf.equal(is_training, True), 
						true_fn = mean_var_with_update, 
						false_fn = lambda : (ema.average(batch_mean), ema.average(batch_var))
					)
	return tf.nn.batch_normalization(
				x = x, 
				mean = mean, 
				variance = var, 
				offset = beta, 
				scale = gamma, 
				variance_epsilon = eps, 
				name = name
			)

def clip(var_list):
	clip_ops = []
	for var in var_list:
		clip_bounds = [-.01, .01]
		clip_ops.append(
				tf.assign(
					var, 
					tf.clip_by_value(var, clip_bounds[0], clip_bounds[1])
				)
			)
	clip_disc_weights = tf.group(*clip_ops)
	return clip_disc_weights


def LeakyReLU(x, alpha = 0.2):
	return tf.maximum(alpha*x, x)

def optimizer(loss, var_list, gan_type = "wgan-gp", learning_rate = 0.01):

	if gan_type == "wgan":
		optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(
			loss,
			var_list = var_list
		)

	if gan_type == "wgan-gp":
		optimizer = tf.train.AdamOptimizer(
					learning_rate, beta1 = 0.5, beta2 = 0.9
				).minimize(
						loss, var_list = var_list
					)

	return optimizer

def Generator(noise, is_training, batch_size):
	l_1 = linear(
				input = noise, 
				output_dim = 4*6*128, 
				scope = "l_1", 
				name = "l1", 
			)
	bn_1 = bn_layer(
				x = l_1,
				is_training = is_training,
				scope = "bn_1",
				name = "bn1"
			)

	bn_1 = tf.reshape(tf.nn.relu(bn_1), [-1, 6, 4, 128])

	dec_2 = decnn2d(
				input = bn_1, 
				filter_shape = [5, 5, 64, 128], 
				output_shape = [batch_size, 11, 8, 64], 
				strid_shape = [1, 2, 2, 1], 
				padding = "SAME", 
				scope = "decnn_2", 
				name = "decnn2",
			)

	bn_2 = bn_layer(
				x = dec_2,
				is_training = is_training,
				scope = "bn_2",
				name = "bn2"
			)
	dec_3 = decnn2d(
				input = tf.nn.relu(bn_2), 
				filter_shape = [3, 3, 32, 64], 
				output_shape = [batch_size, 22, 8, 32], 
				strid_shape = [1, 2, 1, 1], 
				padding = "SAME", 
				scope = "decnn_3", 
				name = "decnn3",
			)
	bn_3 = bn_layer(
				x = dec_3,
				is_training = is_training,
				scope = "bn_3",
				name = "bn3"
			)
	dec_4 = decnn2d(
				input = tf.nn.relu(bn_3), 
				filter_shape = [3, 3, 16, 32], 
				output_shape = [batch_size, 43, 8, 16], 
				strid_shape = [1, 2, 1, 1], 
				padding = "SAME", 
				scope = "decnn_4", 
				name = "decnn4",
			)
	bn_4 = bn_layer(
				x = dec_4,
				is_training = is_training,
				scope = "bn_4",
				name = "bn4"
			)
	dec_5 = decnn2d(
				input = tf.nn.relu(bn_4), 
				filter_shape = [3, 3, 1, 16], 
				output_shape = [batch_size, 85, 8, 1], 
				strid_shape = [1, 2, 1, 1], 
				padding = "SAME", 
				scope = "decnn_5", 
				name = "decnn5",
			)
	output = tf.nn.sigmoid(dec_5, name = "output")
	return output

def Discriminator(inputs, is_training):
	cn_1 = cnn2d(
				input = inputs, 
				filter_shape = [3, 3, 1, 16], 
				strid_shape = [1, 1, 1, 1], 
				padding = "SAME", 
				scope = "cnn_1", 
				name = "c1"
			)

	cn_2 = cnn2d(
				input = LeakyReLU(cn_1), 
				filter_shape = [3, 3, 16, 16], 
				strid_shape = [1, 2, 1, 1], 
				padding = "SAME", 
				scope = "cnn_2", 
				name = "c2"
			)
	bn_2 = bn_layer(
				x = cn_2,
				is_training = is_training,
				scope = "bn_2",
				name = "bn2"
			)
	cn_3 = cnn2d(
				input = LeakyReLU(bn_2), 
				filter_shape = [3, 3, 16, 32], 
				strid_shape = [1, 1, 1, 1], 
				padding = "SAME", 
				scope = "cnn_3", 
				name = "c3"
			)
	bn_3 = bn_layer(
				x = cn_3,
				is_training = is_training,
				scope = "bn_3",
				name = "bn3"
			)
	cn_4 = cnn2d(
				input = LeakyReLU(bn_3), 
				filter_shape = [3, 3, 32, 64], 
				strid_shape = [1, 1, 1, 1], 
				padding = "SAME", 
				scope = "cnn_4", 
				name = "c4"
			)	
	bn_4 = bn_layer(
				x = cn_4,
				is_training = is_training,
				scope = "bn_4",
				name = "bn4"
			)
	
	cn_5 = cnn2d(
				input = LeakyReLU(bn_4), 
				filter_shape = [5, 5, 64, 128], 
				strid_shape = [1, 2, 2, 1], 
				padding = "SAME", 
				scope = "cnn_5", 
				name = "c5"
			)
	bn_5 = bn_layer(
				x = cn_5,
				is_training = is_training,
				scope = "bn_5",
				name = "bn5"
			)
	axis_1, axis_2  = bn_5.get_shape()[1], bn_5.get_shape()[2]
	output = linear(
					input = LeakyReLU(
							tf.reshape(bn_5, [-1, axis_1*axis_2*128])
						),
					output_dim = 1, 
					scope = "linear",
					name = "output"
				)
	return output

class GAN(args):

	def __init__(self, config, database, is_train = True):
		super(GAN, self).__init__(config, database)
		self.config = config
		self.h = config.h
		self.w = config.w
		self.random_len = config.random_len
		self.g_lr = config.g_lr
		self.d_lr = config.d_lr
		self.gamma = config.gamma
		self.gan_type = config.gan_type

		self.real_data = tf.placeholder(
							tf.float32, 
							shape = (self.batch_size, self.h, self.w, 1), 
							name = "real_data"
						)

		self.random = tf.placeholder(
							tf.float32,
							shape = (self.batch_size, self.random_len),
							name = "random"
						)

		self.build(is_train = is_train)

	def build(self, is_train = True):

		with tf.variable_scope("G"):
			self.fake_data = Generator(
									self.random, 
									is_training = is_train,
									batch_size = self.batch_size
								)

		with tf.variable_scope("D"):
			self.disc_real = Discriminator(
								self.real_data,
								is_training = is_train
							)

		with tf.variable_scope("D", reuse = tf.AUTO_REUSE):
			self.disc_fake = Discriminator(
								self.fake_data,
								is_training = is_train
							)

		self.gen_cost = -tf.reduce_mean(self.disc_fake)
		self.disc_cost = tf.reduce_mean(self.disc_fake) - tf.reduce_mean(self.disc_real)

		if self.gan_type == "wgan-gp":
			epsilon = tf.random_uniform(
						shape = [self.batch_size, 1, 1, 1], minval = 0., maxval = 1.
					)

			interpolated_image = self.real_data + epsilon * (self.fake_data - self.real_data)

			with tf.variable_scope("D", reuse = tf.AUTO_REUSE):
				d_interpolated = Discriminator(
									interpolated_image,
									is_training = is_train
								)
			grad_d_interpolated = tf.gradients(
											d_interpolated, [interpolated_image]
										)[0]
			slopes = tf.sqrt(
						1e-8 + tf.reduce_sum(
									tf.square(grad_d_interpolated), 
									axis = [1, 2, 3]
								)
					)
			gradient_penalty = tf.reduce_mean((slopes - 1.) ** 2)

			self.disc_cost += self.gamma * gradient_penalty
			tf.summary.scalar("loss/gradient_penalty", gradient_penalty)

		vars = tf.trainable_variables()
		self.g_params = [v for v in vars if v.name.startswith("G/")]
		self.d_params = [v for v in vars if v.name.startswith("D/")]

		if self.gan_type == "wgan":
			self.wclip = clip(self.d_params)
	
		self.opt_g = optimizer(
						self.gen_cost, self.g_params, learning_rate = self.g_lr
					)
		self.opt_d = optimizer(
						self.disc_cost, self.d_params, learning_rate = self.d_lr
					)
