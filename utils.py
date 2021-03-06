from gensim.models import KeyedVectors
import tensorflow as tf
import numpy as np
import pickle as pkl
import os


def gaussian_kld(recog_mu, recog_logvar, prior_mu, prior_logvar):
    kld = -0.5 * tf.reduce_sum(1 + (recog_logvar - prior_logvar)
                               - tf.div(tf.pow(prior_mu - recog_mu, 2), tf.exp(prior_logvar))
                               - tf.div(tf.exp(recog_logvar), tf.exp(prior_logvar)), reduction_indices=1)
    return kld


def sample_gaussian(mu, logvar):
    epsilon = tf.random_normal(tf.shape(logvar), name="epsilon")
    std = tf.exp(0.5 * logvar)
    z= mu + tf.multiply(std, epsilon)
    return z


def load_vocab(vocab_file):
    """
    :param vocab_file:
    :return: a reversed dictionary, and a list that contains all the words
    """
    dic = pkl.load(open(vocab_file, 'rb'))
    rst = {idx: word for word, idx in dic.items()}
    # words = [word for word, idx in dic.items()]
    return rst#, words


def embedding_matrix(vecfile, dicts):
    pretrained = KeyedVectors.load_word2vec_format(vecfile, binary=True)

    def word_to_vec(word):
        """
        # given a word, return the embedding and index
        # if not found, return a random normal distributed vector
        """
        if word in pretrained.vocab:
            return pretrained[word]
        else:
            print(word.encode("utf-8"))
            return np.random.normal(0, 1, 300)

    embed = np.zeros(shape=(len(dicts), 300), dtype=np.float32)
    for i, w in dicts.items():
        #print(w)
        embed[i] = word_to_vec(w.lower())
    return embed


def get_ckpt(dirpath):
    if os.path.exists(dirpath):
        filepath = os.path.join(dirpath, 'checkpoint')
        if os.path.isfile(filepath):
            with open(filepath, 'r') as fin:
                data = fin.readlines()
            ckpt = os.path.join(dirpath, data[0].split('"')[1])
            print("ckpt is: ", ckpt)
            return ckpt
    return None