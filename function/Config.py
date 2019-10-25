""" 
@author: 
@file: Config.py
"""

class Config:
    def __init__(self):
        
        self.periodic_table = "train_data/Periodic_Table/Periodic_Table.csv"

        self.gan_type = "wgan-gp"
        self.random_len = 128
        self.gamma = 10
        self.disc_iters = 1
        self.g_lr = 1e-3
        self.d_lr = 1e-2
        self.h = 85
        self.w = 8
        self.times = 100000000

        self.ICSD_gan_batch_size = 32
        self.OQMD_gan_batch_size = 512
        self.MP_gan_batch_size = 32
        self.Bandgap_gan_batch_size = 32

        self.tolerate = 0.8
        # self.ae_batch_size = 1024
        self.OQMD_ae_batch_size = 1024
        self.ICSD_ae_batch_size = 256
        self.MP_ae_batch_size = 1024

        self.ae_lr = 1e-5
        self.gen_num = 1024

        self.ae_epochs = 100000

class args(object):

    def __init__(self, config, database):

        if database == "OQMD":
            self.batch_size = config.OQMD_gan_batch_size

        elif database == "ICSD":
            self.batch_size = config.ICSD_gan_batch_size

        elif database == "MP":
            self.batch_size = config.MP_gan_batch_size

        elif database == "Bandgap":
            self.batch_size = config.Bandgap_gan_batch_size

        elif database == "ICSD_Filter":
            self.batch_size = config.Bandgap_gan_batch_size
