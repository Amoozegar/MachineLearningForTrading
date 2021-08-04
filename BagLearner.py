import numpy as np
import RTLearner as rt

class BagLearner(object):
    """
    This is a Bag Learner.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, learner, kwargs , bags , boost= False, verbose=False):
        """
        Constructor method
        """
        self.learner = learner
        self.arguments = kwargs
        self.bagCount = bags
        self.boost = boost
        self.verbose= verbose
        self.learners = []

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "samoozegar3"




    def add_evidence(self, X, Y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        for i in range(self.bagCount):
            new_learner = self.learner(**self.arguments)
            data_indx =np.random.choice(Y.shape[0], Y.shape[0], replace=True)
            newX = X[data_indx]
            newY = Y[data_indx]
            new_learner.add_evidence(newX,newY)
            self.learners.append(new_learner)

    def query(self, X_test):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        predicted = []
        for single_learner in self.learners:
            predicted.append(single_learner.query(X_test))
        # print ('predicted',predicted)
        return np.mean(predicted, axis=0)



if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")

