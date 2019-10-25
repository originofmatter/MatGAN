import tensorflow as tf
import numpy as np
import tensorflow.contrib.slim as slim
import time, os, re
from collections import OrderedDict, defaultdict

def elemenet(formulas):
	elements = ['H', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Sc', 'Ti', 'V', 
	            'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 
	            'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 
	            'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 
	            'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu']

	formulare = re.compile(r'([A-Z][a-z]*)(\d*)')
	def parse_formula(formula):
	    pairs = formulare.findall(formula)
	    length = sum((len(p[0]) + len(p[1]) for p in pairs))
	    assert length == len(formula)
	    formula_dict = defaultdict(int)
	    for el, sub in pairs:
	        formula_dict[el] += float(sub) if sub else 1
	    return formula_dict

	# formulas = ["Sb2PmSmAc",'Er2Lu', 'YSm2']
	formulas = [parse_formula(x) for x in formulas]
	# print(formulas)

	input = np.zeros(shape=(len(formulas), 86), dtype=np.float32)
	i = -1
	for formula in formulas:
	    i+=1
	    keys = formula.keys()
	    values = formula.values()
	    total = float(sum(values))
	    for k in keys:
	        input[i][elements.index(k)] = formula[k]/total
	data = input

	test_X = data
	test_y = np.zeros((86), np.float32)

	batch_size = 1

	architecture = '1024x4-512x3-256x3-128x3-64x2-32x1-1'
	activation = 'relu'
	dropouts = [0.8, 0.9, 0.7, 0.8]
	SEED = 66478
	num_input = 86

	def model_slim(data, architecture, train=True):
	    # global  activation
	    activation = "relu"
	    nets = []
	    if train:
	        reuse = None
	    else:
	        reuse = True

	    if activation == 'relu':
	        activation = tf.nn.relu

	    archs = architecture.strip().split('-')
	    net = data
	    for i in range(len(archs)):
	        arch = archs[i]
	        if 'x' in arch:
	            [{'doi': '10.1063/1.3253115'}]

	            arch = arch.split('x')
	            num_outputs = int(arch[0])
	            layers = int(arch[1])
	            j=0
	            for l in range(layers):
	                print('adding fully connected layers with %d outputs'%num_outputs)
	                net = slim.layers.fully_connected(net, num_outputs=num_outputs, scope='fc' + str(i)+'_'+str(j),
	                                                      activation_fn=activation, reuse=reuse)
	                nets.append(net)
	                j+=1
	            if len(dropouts) > i:
	                print('adding dropout', dropouts[i])
	                net = tf.nn.dropout(net, dropouts[i], seed=SEED)
	        else:
	            print('adding final layer with 1 output')
	            net = slim.layers.fully_connected(net, num_outputs=1, scope='fc' + str(i),
	                                              activation_fn=None, reuse=reuse)
	            nets.append(net)
	    net = tf.squeeze(net)
	    nets.append(net)
	    return nets

	tf.reset_default_graph()
	train_data_node = tf.placeholder(tf.float32, shape=(batch_size, num_input))
	eval_data = tf.placeholder(tf.float32, shape=(batch_size, num_input))
	logitss = model_slim(train_data_node, architecture)
	logits = logitss[-1]
	train_labels_node = tf.placeholder(tf.float32, shape=(batch_size))
	print('logits shape: ', logitss[-1].get_shape())
	eval_predictions = model_slim(eval_data, architecture,train=False)
	eval_prediction = eval_predictions[-1]

	sess = tf.Session()
	sess.run(tf.initialize_all_variables())
	train_writer = tf.summary.FileWriter('summary', graph_def=sess.graph_def)
	saver = tf.train.Saver()

	model_path = os.getcwd() + '/check_point/ElemNet/model.ckpt'
	assert  model_path is not None
	print('Restoring model from %s' % model_path)
	saver.restore(sess, model_path)

	size = data.shape[0]
	predictions = np.ndarray(shape=(size), dtype=np.float32)
	for begin in range(0, size, batch_size):
	    end = begin + batch_size
	    if end <= size:
	        # predictions[:,begin:end] \
	        outputs = sess.run(eval_prediction, feed_dict={eval_data: data[begin:end, ...]})
	        predictions[begin:end] = outputs 
	    else:
	        outputs = sess.run(eval_prediction, feed_dict={eval_data: data[-batch_size:, ...]})
	        predictions[-batch_size:] = outputs

	return predictions