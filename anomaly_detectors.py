import abc
import pandas as pd
import numpy as np

from update_formulae import (
    rolling_window_update,
    decision_rule
)

from scipy.stats import norm
from sklearn.base import BaseEstimator

THRESHHOLD = 0.99

class AnomalyMixin(object):
    """
    This is a Mixin class for all Anomaly detectors compatible to BaseEstimator from scikit-learn
    """
    _estimator_type = "anomaly"
    def fit_score(self, X):
        """
        Fits the model on X and scores each datapoint in X.

        parameters:
        X: ndarray, shape(n_samples, n_features)
           inputdata
        Returns:
        Y: ndarray, shape (n_samples,)
           anomaly scores
        """
        self.fit(X)
        return self.score_anomaly(X)
    
    def score_anomaly(self, X):
        raise NotImplementedError
    
    def update(self, X):
        raise NotImplementedError

    def flag_anomaly(self, X):
        raise NotImplementedError
    
    def fit(self, X):
        raise NotImplementedError



class Gaussian1D(BaseEstimator, AnomalyMixin):
    def __init__(self, ff = 1.0, threshold=THRESHHOLD):
        self.ff = ff
        self.threshold = threshold
        self.ess_ = 1
        self.mu_ = 0
        self.std_ = 1

    def fit(self, x):
        x = pd.Series(x)
        # self.__setattr__('mu_', np.mean(x))
        # self.__setattr__('std_', np.std(x, ddof=1))
        # self.__setattr__('ess_', len(x))

    def update(self, x):  # allows mini-batch
       pass
    
    def score_anomaly(self, x):
        x = pd.Series(x)
        scaled_x = np.abs(x - self.mu_)/(1.0*self.std_)
        return norm.cdf(scaled_x)
    def flag_anomaly(self, x):
        return decision_rule(self.score_anomaly(x), self.threshold)




