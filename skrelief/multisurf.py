import numpy as np
from scipy.stats import rankdata
import os
from sklearn.base import BaseEstimator, TransformerMixin

from julia import Julia
jl = Julia(compiled_modules=False)
script_path = os.path.abspath(__file__)
jl.eval('push!(LOAD_PATH, "' + script_path[:script_path.rfind('/')] + '/")')

from julia import MultiSURF as MultiSURF_jl

class MultiSURF(BaseEstimator, TransformerMixin):
    """sklearn compatible implementation of the MultiSURF algorithm

    Reference:
        Ryan Urbanowicz, Randal Olson, Peter Schmitt, Melissa Meeker, and
        Jason Moore. Benchmarking Relief-based feature selection methods for
        bioinformatics data mining. Journal of Biomedical Informatics, 85, 2018.

    Args:
        n_features_to_select (int): number of features to select from dataset.
        dist_func (function): function used to measure similarities between samples.
        If equal to None, the default implementation of L1 distance in Julia is used.
        f_type (string): specifies whether the features are continuous or discrete 
        and can either have the value of "continuous" or "discrete".

    Attributes:
        n_features_to_select (int): number of features to select from dataset.
        dist_func (function): function used to measure similarities between samples.
        f_type (string): continuous or discrete features.
        _multisurf (function): function implementing MultiSURF algorithm written in Julia programming language.
    """
   
    def __init__(self, n_features_to_select=10, dist_func=lambda x1, x2 : np.sum(np.abs(x1-x2), 1), f_type="continuous"):
        self.n_features_to_select = n_features_to_select
        self.dist_func = dist_func
        self.f_type = f_type
        self._multisurf = MultiSURF_jl.multisurf


    def fit(self, data, target):
        """
        Rank features using MultiSURF feature selection algorithm

        Args:
            data (numpy.ndarray): matrix of data samples
            target (numpy.ndarray): vector of target values of samples

        Returns:
            (object): reference to self
        """

        # Compute feature weights and rank.
        if self.dist_func is not None:
            # If distance function specified.
            self.weights = self._multisurf(data, target, self.dist_func, f_type=self.f_type)
        else:
            # If distance function not specified, use default L1 distance (implemented in Julia).
            self.weights = self._multisurf(data, target, f_type=self.f_type)
        self.rank = rankdata(-self.weights, method='ordinal')
        
        # Return reference to self.
        return self


    def transform(self, data):
        """
        Perform feature selection using computed feature ranks.

        Args:
            data (numpy.ndarray): matrix of data samples on which to perform feature selection.

        Returns:
            (numpy.ndarray): result of performing feature selection.
        """

        # select n_features_to_select best features and return selected features.
        msk = self.rank <= self.n_features_to_select  # Compute mask.
        return data[:, msk]  # Perform feature selection.

