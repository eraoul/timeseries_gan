import sugartensor as tf
import numpy as np
import matplotlib.pyplot as plt
from model import *


__author__ = 'namju.kim@kakaobrain.com'


# set log level to debug
tf.sg_verbosity(10)


#
# hyper parameters
#

batch_size = 100   # batch size


#
# inputs
#

# target_number
target_num = tf.placeholder(dtype=tf.sg_intx, shape=batch_size)
# target continuous variable # 1
target_cval_1 = tf.placeholder(dtype=tf.sg_floatx, shape=batch_size)
# target continuous variable # 2
target_cval_2 = tf.placeholder(dtype=tf.sg_floatx, shape=batch_size)

# category variables
z = (tf.ones(batch_size, dtype=tf.sg_intx) * target_num).sg_one_hot(depth=cat_dim)

# continuous variables
z = z.sg_concat(target=[target_cval_1.sg_expand_dims(), target_cval_2.sg_expand_dims()])

# random seed = categorical variable + continuous variable + random normal
z = z.sg_concat(target=tf.random_uniform((batch_size, rand_dim)))

# generator
gen = generator(z).sg_squeeze(axis=2)


#
# run generator
#
def run_generator(num, x1, x2, fig_name='sample.png'):
    with tf.Session() as sess:
        tf.sg_init(sess)
        # restore parameters
        saver = tf.train.Saver()
        saver.restore(sess, tf.train.latest_checkpoint('asset/train'))

        # run generator
        imgs = sess.run(gen, {target_num: num,
                              target_cval_1: x1,
                              target_cval_2: x2})

        # plot result
        _, ax = plt.subplots(10, 10, sharex=True, sharey=True)
        for i in range(10):
            for j in range(10):
                ax[i][j].plot(imgs[i * 10 + j])
                ax[i][j].set_axis_off()
        plt.savefig('asset/train/' + fig_name, dpi=600)
        tf.sg_info('Sample image saved to "asset/train/%s"' % fig_name)
        plt.close()


#
# draw sample by categorical division
#

# fake image
run_generator(np.random.randint(0, cat_dim, batch_size),
              np.random.uniform(0, 1, batch_size), np.random.uniform(0, 1, batch_size),
              fig_name='fake.png')

# classified image
run_generator(np.arange(cat_dim).repeat(cat_dim),
              np.random.uniform(0, 1, batch_size), np.random.uniform(0, 1, batch_size))

#
# draw sample by continuous division
#

for i in range(10):
    run_generator(np.ones(batch_size) * i,
                  np.linspace(0, 1, cat_dim).repeat(cat_dim),
                  np.expand_dims(np.linspace(0, 1, cat_dim), axis=1).repeat(cat_dim, axis=1).T.flatten(),
                  fig_name='sample%d.png' % i)
