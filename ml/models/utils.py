import pandas as pd
import numpy as np

import tensorflow as tf

def feateng(train, test):

    full_data = [train, test]

    #The embarked feature has some missing value. and we try to fill those with the most occurred value ( 'S' ).
    for dataset in full_data:
        dataset['Embarked'] = dataset['Embarked'].fillna('S')

    #We have plenty of missing values in this feature. # generate random numbers between (mean - std) and (mean + std). Then we categorize age into 5 range.
    for dataset in full_data:
        age_avg = dataset.loc[:,'Age'].mean()
        age_std = dataset.loc[:,'Age'].std()
        age_null_count =   dataset.loc[:,'Age'].isnull().sum()
        age_null_random_list = np.random.randint(age_avg - age_std, age_avg + age_std, size=age_null_count)
        dataset.loc[:,'Age'][np.isnan(dataset.loc[:,'Age'])] = age_null_random_list
        dataset.loc[:,'Age'] =   dataset.loc[:,'Age'].astype(int)

    train.loc[:,'CategoricalAge'] = pd.cut(train['Age'], 5)

    for dataset in full_data:
        # Mapping Sex
        dataset['Sex'] = dataset['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
        
        # Mapping Embarked
        dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)
        
        # Mapping Age
        dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
        dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
        dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
        dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
        dataset.loc[ dataset['Age'] > 64, 'Age']                           = 4

    # Feature Selection
    #drop_elements = ['PassengerId', 'Ticket', 'Cabin','Fare','Pclass','Name']  
    drop_elements = ['Ticket', 'Cabin','Fare','Pclass','Name']  
    train = train.drop(drop_elements, axis = 1)
    train = train.drop(['CategoricalAge'], axis = 1)

    test  = test.drop(drop_elements, axis = 1)

    train.to_csv('./ml/bases/titanic/train-ready.csv',index=False)
    test.to_csv('./ml/bases/titanic/test-ready.csv',index=False)

    return train,test

def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(10).repeat().batch(batch_size)
    return dataset

def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        inputs = features
    else:
        inputs = (features, labels)

    dataset = tf.data.Dataset.from_tensor_slices(inputs)
    
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    return dataset

def get_feature_columns(X):
    feature_columns = []
    for key in X.keys():
        feature_columns.append(tf.feature_column.numeric_column(key=key))
    return feature_columns
