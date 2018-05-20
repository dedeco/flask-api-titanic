import tensorflow as tf
import os
import pandas as pd
import numpy as np

from .utils import eval_input_fn, get_feature_columns

SAVE_PATH = './ml/save'
MODEL_NAME = 'test'

def run():

    path = SAVE_PATH + '/' + MODEL_NAME + '.ckpt'

    train = pd.read_csv('./ml/bases/titanic/train-ready.csv')
    train.pop('Survived')

    feature_columns = get_feature_columns(train)

    #restore model saved (after train)
    classifier = tf.estimator.DNNClassifier(
        feature_columns=feature_columns,
        hidden_units=[10, 10],
        n_classes=2,
        model_dir=path)

    test = pd.read_csv('./ml/bases/titanic/test-ready.csv')
    _test = pd.read_csv('./ml/bases/titanic/test.csv')

    #do prediction using saved model
    predictions = classifier.predict(
        input_fn=lambda:eval_input_fn(test,labels=None,
        batch_size=100))

    results = list(predictions)

    pgrs_survivals = [ int(x['class_ids'][0]) for x in results]
    pgrs_prob = [ x['probabilities'][1] * 100 for x in results]

    test['Survived'] = pgrs_survivals
    test['ChangeToSurvive'] = pgrs_prob
    test['Name'] = _test['Name']
    #test.to_csv('./data/titanic/results.csv',index=False)
    
    return test