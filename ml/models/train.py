import pandas as pd
import numpy as np

from .utils import feateng
from .utils import train_input_fn, eval_input_fn, get_feature_columns

from sklearn.model_selection import train_test_split 
from sklearn.utils import shuffle

import csv
import tensorflow as tf
import os, sys

SAVE_PATH = './ml/save'
MODEL_NAME = 'test'

def run():

    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    _train = pd.read_csv('./ml/bases/titanic/train.csv')
    _test = pd.read_csv('./ml/bases/titanic/test.csv')

    #feature engineering and cleanning Data
    train, test = feateng(_train, _test)

    y = train.pop('Survived')
    X = train

    # 20% for evaluate
    X_train, X_tmp, y_train, y_tmp = train_test_split(X, y, test_size=0.2, random_state=21)

    feature_columns = get_feature_columns(X_train)

    path = SAVE_PATH + '/' + MODEL_NAME + '.ckpt'

    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[10, 10],
        n_classes=2,
        model_dir=path)

    #train
    batch_size = 100
    train_steps = 400

    for i in range(0,100):
        
        classifier.train(
            input_fn=lambda:train_input_fn(X_train, y_train,
                                                     batch_size),
        steps=train_steps)


    eval_result = classifier.evaluate(
        input_fn=lambda:eval_input_fn(X_tmp, y_tmp,batch_size)
    )

    print (eval_result)

    predictions = classifier.predict(
        input_fn=lambda:eval_input_fn(test[:10],labels=None,
        batch_size=batch_size))

    results = list(predictions)

    #print (results)

    def x(res,j):
        class_id = res[j]['class_ids'][0]
        probability = int(results[j]['probabilities'][class_id] *100)

        if int(class_id) == 0:
            return ('%s%% probalitity to %s' % (probability,'Not survive'))
        else:
            return ('%s%% probalitity to %s' % (probability,'Survive!'))

    print ('Predictions for 10 first records on test(dataset):')

    for i in range(0,10):    
        print (x(results,i))

if __name__ == "__main__":
    run()
