import numpy as np
import pandas as pd
from decorators import *

# Basic Symmetric IO Model
class BSymIO:

    # ====================================
    #       init function
    # ====================================

    @sufficientinfo
    def __init__(self,
                 f_matrix=None,
                 a_matrix=None,
                 y_vector=None,
                 v_abs_vector=None,
                 v_coef_vector=None,
                 x_vector=None,
                 verbose=True,
                 unit='currency'):

        self.__F = pd.read_csv(f_matrix, index_col=0) if f_matrix else None
        self.__A = pd.read_csv(a_matrix, index_col=0) if a_matrix else None

        self.__Y = pd.Series.from_csv(y_vector, index_col=0) if y_vector else None
        self.__V_abs = pd.Series.from_csv(v_abs_vector, index_col=0) if v_abs_vector else None
        self.__V_coef = pd.Series.from_csv(v_coef_vector, index_col=0) if v_coef_vector else None
        self.__X = pd.Series.from_csv(x_vector, index_col=0) if x_vector else None

        self.__verbose = verbose
        self.__unit = unit

        if self.__verbose:
            self.__print_initialization(True)

    # ====================================
    #       public communication methods
    # ====================================

    def show_data(self):
        print("A matrix:\n%s\n\n" % self.__A)
        print("F matrix:\n%s\n\n" % self.__F)
        print("Y vector:\n%s\n\n" % self.__Y)
        print("V vector:\n%s\n\n" % self.__V_abs)
        print("X vector:\n%s\n\n" % self.__X)

    # ====================================
    #       public calculation methods
    # ====================================

    # calculate X from F and V
    def calc_x_from_f_and_v(self, store=True):
        x_vector = self.__calc_x_by_addition(dimension=0)
        if store:
            self.__store('X', x_vector)
        return x_vector

    def calc_x_from_f_and_y(self, store=True):
        x_vector = self.__calc_x_by_addition(dimension=1)
        if store:
            self.__store('X', x_vector)
        return x_vector

    def calc_x_from_a_and_y(self, store=True):
        x_vector = self.__calc_x_with_leontief_inverse()
        if store:
            self.__store('X', x_vector)
        return x_vector

    def calc_a_from_f_and_x(self, store=True):
        a_matrix = self.__calc_a()
        if store:
            self.__store('A', a_matrix)
        return a_matrix

    # ====================================
    #       private communication methods
    # ====================================

    # print loaded matrices if verbose = true
    def __print_initialization(self, success):
        if success:
            print("Basic Symmetric IO Model Initiated with following data provided:\n\n")
            self.show_data()

    @staticmethod
    def __print_storage(vector_name, values):
        print('\n%s internally stored with following values:\n%s' % (vector_name, values))

    # ====================================
    #       private calculation methods
    # ====================================

    @inputsfromset([0,1])
    def __calc_x_by_addition(self, dimension):
        # Note: dimension 0 sums vertically, dimension 1 sums horizontally

        # sum all inputs for each sector from other sectors
        col_sum_f = self.__F.sum(dimension)
        # Pick the correct externality vactor to add up to the summed values
        externality_vector = self.__V_abs.values if (dimension == 0) else self.__Y.values
        output_values = col_sum_f.values + externality_vector
        # create a new series containing values for X
        x_vector = pd.Series(data=output_values, index=self.__F.keys())
        return x_vector

    def __calc_x_with_leontief_inverse(self):
        I_matrix = np.identity(len(self.__Y))
        A_matrix = self.__A.values
        Y_matrix = self.__Y.values
        leontief_inverse = np.linalg.inv(I_matrix - A_matrix)
        output_values = np.dot(leontief_inverse, Y_matrix)
        x_vector = pd.Series(data=output_values, index=self.__F.keys())
        return x_vector

    def __calc_a(self):
        inverse_multiplication_factors = (1 / self.__X)
        a_matrix = self.__F * inverse_multiplication_factors
        return a_matrix

    # ====================================
    #       private storage methods
    # ====================================

    def __store(self, dir_name, values):
        attr = '_BSymIO__%s' % dir_name
        self.__setattr__(attr, values)
        if self.__verbose:
            self.__print_storage(dir_name.replace('_',' '), values)


# Temporary testing environment
if __name__ == '__main__':

    input_directory = './sample input/'
    F_file = input_directory + 'F_table.csv'
    V_file = input_directory + 'V_table.csv'
    Y_file = input_directory + 'Y_table.csv'

    model = BSymIO(f_matrix=F_file, v_abs_vector=V_file, y_vector=Y_file)

    model.calc_x_from_f_and_v()
    model.calc_a_from_f_and_x()
    model.calc_x_from_a_and_y()
