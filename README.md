# Flask API for search name (similar) Titanic survivals  

This repo shows how to create a simple RESTful API using the Flask web framework.

1.Download the Titanic training data set for the Titanic prediction challenge from Kaggle. (https://www.kaggle.com/c/titanic/data)

2.Build a simple model (of your choice) to predict ‘survival’ based on ‘sex’, ‘age’. ‘sibsp’, ‘parch’ and ‘embarked’. Predictive accuracy of this model won’t be judged.

3.We now want to deploy this model as a Flask API. The API should take ‘Name’ as a get parameter and return both the passenger that matches the name most closely as well as the survival prediction for this particular person. Specifically

- Create an endpoint ‘survival’ which takes ‘Name’ as a query parameter
- We now want to find the passenger which most closely resembles the name provided in the get-parameter. Which method would you choose to measure how ‘close’ two names are? Briefly comment on your choice.
- Implement a lookup function that takes as input a name, finds the closest matching passenger in the training data and returns ‘sex’, ‘age’,‘sibsp’, ‘parch’ and ‘embarked’ for the matched record.
- Predict the chance of survival for that particular passenger using the model you build in 2.
- Let the API return both the matched name as well as the prediction for that name.

[Here is an article about this repo (on Medium).](https://medium.com/@dedecu/flask-api-using-dnnclassifie-tensorflow-models-based-on-kaggle-dataset-titanic-survivals-5841a7b6dd0)

## Install guide

##### Clone the repo

```bash
$ git clone https://github.com/dedeco/flask-api-titanic.git
$ cd flask-api-titanic
```

##### Create the virtualenv
```bash
$ virtualenv -p python3 flaskticenv
$ source flaskticenv/bin/activate
```

##### Install dependencies
```bash
$ pip install -r requirements.txt
```

##### Create tables
```bash
$ python create_tables.py
```

##### Train and serving and saving the model on sqlite (test.db)
```bash
$ python serve.py
```
## Running the app

```bash
$ python runserver.py
```

## Test
```bash
$ make test
```
