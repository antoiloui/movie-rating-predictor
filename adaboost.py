import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
import base_methods as base


def adaboost():
    prefix = 'Data/'

    # ------------------------------- Learning ------------------------------- #
    # Load training data
    R = pd.read_csv('predicted_matrix.txt', sep=" ", header=None)
    user_movie_pairs = base.load_from_csv(os.path.join(prefix, 'data_train.csv'))
    training_labels = base.load_from_csv(os.path.join(prefix, 'output_train.csv'))

    # Build the training learning matrix
    X_train = base.create_learning_matrices(R.values, user_movie_pairs)

    # Build the model
    y_train = training_labels

    # Best estimator after hyperparameter tuning
    base_model = DecisionTreeRegressor()
    model =  AdaBoostRegressor(base_model)
    with base.measure_time('Training'):
        print("Training with adaboost...")
        model.fit(X_train, y_train)

    # -----------------------Submission: Running model on provided test_set---------------------------- #
    #Load test data
    test_user_movie_pairs = base.load_from_csv(os.path.join(prefix, 'data_test.csv'))

    # Build the prediction matrix
    X_ts = base.create_learning_matrices(R.values, test_user_movie_pairs)

    # Predict
    y_pred = model.predict(X_ts)

    fname = base.make_submission(y_pred, test_user_movie_pairs, 'MF_withAdaboost')
    print('Submission file "{}" successfully written'.format(fname))

if __name__ == '__main__':
    adaboost()
    