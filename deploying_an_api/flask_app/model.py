
import sys
import numpy as np
from keras.callbacks import EarlyStopping
from keras.layers import Input, Embedding, Flatten, Dot
from keras.models import Model

from time import sleep
from tqdm import tqdm_notebook as tqdm

import pandas as pd


import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

class EmbeddingModel(object):
    
    def __init__(self, nb_user, nb_items, embedding_size=30):
        self._build_model(nb_user, nb_items, embedding_size=30)
        
    
    def _build_model(self, nb_users, nb_items, embedding_size=30):
        user_id_input = Input(shape=[1],name='user')
        item_id_input = Input(shape=[1], name='item')
        user_embedding = Embedding(output_dim=embedding_size, input_dim=nb_users+1,
                           input_length=1, name='user_embedding')(user_id_input)

        item_embedding = Embedding(output_dim=embedding_size, input_dim=nb_items+1,
                           input_length=1, name='item_embedding')(item_id_input)
        
        user_vecs = Flatten()(user_embedding)
        item_vecs = Flatten()(item_embedding)

        y = Dot(axes=1)([user_vecs, item_vecs])
        
        self.model = Model(inputs=[user_id_input, item_id_input], outputs=y)
        self.model.compile(optimizer='adam', loss='mse')
        
        
    def fit(self, X, y, epochs=50, verbose=False):
        """
        embedding model, with inputs of "user_id", "item_id"
        
        Param:
            X : [user_history, item_history]
            y : rating_history
        """
        early_stopping = EarlyStopping(monitor='val_loss', patience=2)
        self.model.fit(X, y, epochs=epochs, callbacks=[early_stopping],
                       batch_size=64,  validation_split=0.1,
                       shuffle=True, verbose=2)

    
    def update(self, X, y, epochs=1, verbose=False):
        """
        embedding model, with inputs of "user_id", "item_id"
        
        Param:
            X : [user_history, item_history]
            y : rating_history
        """
        self.model.fit(X, y, epochs=epochs, verbose=verbose)
        
    def predict(self, X):
        """
        perdict a rating of embedding model
        
        Params:
            input_data : [users, itmes]
        Returns:
            input
        """
        pred = self.model.predict(X)
        return float(pred)
    
