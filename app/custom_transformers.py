from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np

class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.n_features_in = X.shape[1]
        return self

    def transform(self, X, y=None):
        assert self.n_features_in == X.shape[1]
        return np.log(X)
