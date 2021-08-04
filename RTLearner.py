import numpy as np


class RTLearner(object):
    """
    This is a Decision Tree Learner.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, leaf_size =1, verbose=False):
        """
        Constructor method
        """
        self.leaf_size = leaf_size

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "samoozegar3"

    def build_tree(self, X, Y):
        """
        build a decision tree
        return: an array of trees
        """
        #check stopping criteria
        #leaf_size criteria to stop the algorithm
        if X.shape[0] <= self.leaf_size:
            return np.array([[-1 , np.mean(Y), np.nan, np.nan]]) #return an array of [factor_index, splitVal, right tree, left tree]
        if X.shape[0]==1:
            return np.array([[-1, Y[0], np.nan, np.nan]]) #-1 represents leaf
        if all(x == Y[0] for x in Y):
            return np.array([[-1, Y[0], np.nan, np.nan]])

        np.random.seed(903650161)  #gid
        # randomly determine best feature to split
        feature_indx = np.random.randint(X.shape[1])

        #find split value
        splitVal = float(X[np.random.randint(np.shape(X)[0]), feature_indx] + X[
            np.random.randint(np.shape(X)[0]), feature_indx]) / 2

        #find left split
        lefttree_X = X[X[:, feature_indx] <= splitVal]
        lefttree_Y = Y[X[:, feature_indx] <= splitVal]

        # if after split all data points fall in one node, we are done!
        if (lefttree_X.shape[0] == 0 or lefttree_X.shape[0] == X.shape[0]):
            return np.array([[-1, np.mean(Y), np.nan, np.nan]])
        #find right split
        righttree_X = X[X[:,feature_indx] > splitVal]
        righttree_Y = Y[X[:, feature_indx] > splitVal]



        lefttree = self.build_tree(lefttree_X, lefttree_Y)
        righttree = self.build_tree(righttree_X, righttree_Y)
        # print ('lefttree', lefttree)
        root = [feature_indx, splitVal, 1, lefttree.shape[0]+1] #left tree is built next, and right tree is 1+rows of left tree

        return np.vstack((root, lefttree, righttree))

    def make_prediction(self, node, x, node_index):
        """
        make prediction for a single data point

        return: predicted value for x
        type: float
        """
        #if the node is terminal node or leaf
        if node[0]== -1:
            return node[1]  #return prediction
        # print ('node[0]', node[0])
        # print ('x[node[0', x[node[0]])
        if x[int(node[0])] > node[1]: #if value of x at split feature > splitVal , right tree
            node_index = int(node_index + node[3]) #update index of node
            return self.make_prediction(self.RTLearner[node_index], x,node_index)
        else:
            node_index = int(node_index + node[2])
            return self.make_prediction(self.RTLearner[node_index], x, node_index)



    def add_evidence(self, X, Y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """

        self.RTLearner = self.build_tree(X, Y)


    def query(self, X_test):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        prediction =[]
        for x in X_test:
            prediction.append(self.make_prediction(self.RTLearner[0], x, 0))
        return prediction


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
    # # y = np.array([3, 4, 6, 5, 6, 8, 7,5])
    # # x = np.array([[0.61, 0.63, 8.4],
    # #                 [0.885, 0.33, 9.1],
    # #               [0.56, 0.5, 9.4],
    # #               [0.735, 0.57, 9.8],
    # #               [0.32, 0.78, 10],
    # #               [0.26, 0.63, 11.8],
    # #              [0.5, 0.68, 10.5],
    # #              [0.725, 0.39, 10.9]])
    #
    #
    # dtlearner = DTLearner(leaf_size = 1)
    #
    #
    # dtlearner.add_evidence(x,y)
    # print (dtlearner.build_tree(x,y))
    # # x_test = np.array([[0.56, 0.5, 9.4]])
    # print( dtlearner.query(x_test))