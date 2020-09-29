import numpy as np
from scipy.stats import rankdata
from sklearn.base import BaseEstimator, TransformerMixin

from julia import Julia
Julia(compiled_modules=False)
from julia import Relief as Relief_jl


class SURFStar(BaseEstimator, TransformerMixin):
    """sklearn compatible implementation of the SURFStar algorithm.

    Reference:
        Casey S. Greene, Daniel S. Himmelstein, Jeff Kiralis, and Jason H. Mo-
        ore. The informative extremes: Using both nearest and farthest indivi-
        duals can improve Relief algorithms in the domain of human genetics.
        In Clara Pizzuti, Marylyn D. Ritchie, and Mario Giacobini, editors,
        Evolutionary Computation, Machine Learning and Data Mining in Bi-
        oinformatics, pages 182–193. Springer, 2010.

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
    """
   
    def __init__(self, n_features_to_select=10, dist_func=None, f_type="continuous"):
        self.n_features_to_select = n_features_to_select
        self.dist_func = dist_func
        self.f_type = f_type


    def fit(self, data, target):
        """
        Rank features using SURFStar feature selection algorithm

        Args:
            data (numpy.ndarray): matrix of data samples
            target (numpy.ndarray): vector of target values of samples

        Returns:
            (object): reference to self
        """

        # Compute feature weights and rank.
        if self.dist_func is not None:
            # If distance function specified.
            self.weights = Relief_jl.surfstar(data, target, self.dist_func, f_type=self.f_type)
        else:
            # If distance function not specified, use default L1 distance (implemented in Julia).
            self.weights = Relief_jl.surfstar(data, target, f_type=self.f_type)
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

