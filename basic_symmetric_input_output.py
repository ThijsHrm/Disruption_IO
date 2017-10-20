import numpy as np
import pandas as pd
from decorators import sufficientinfo

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
                 v_vector=None,
                 x_vector=None,
                 verbose=True,
                 unit='currency'):

        self.__F_matrix = pd.read_csv(f_matrix, index_col=0) if f_matrix else None
        self.__A_matrix = pd.read_csv(a_matrix, index_col=0) if a_matrix else None

        self.__Y_vector = pd.Series.from_csv(y_vector, index_col=0) if y_vector else None
        self.__V_vector = pd.Series.from_csv(v_vector, index_col=0) if v_vector else None
        self.__X_vector = pd.Series.from_csv(x_vector, index_col=0) if x_vector else None

        self.__verbose = verbose
        self.__unit = unit

        self.__print_initialization(True)

    # ====================================
    #       public communication methods
    # ====================================

    def show_data(self):
        print("A matrix:\n%s\n\n" % self.__A_matrix)
        print("F matrix:\n%s\n\n" % self.__F_matrix)
        print("Y vector:\n%s\n\n" % self.__Y_vector)
        print("V vector:\n%s\n\n" % self.__V_vector)
        print("X vector:\n%s\n\n" % self.__X_vector)

    # ====================================
    #       public calculation methods
    # ====================================

    # calculate X from F and V
    def calc_x_from_f_and_v(self, store=True):
        x_vector = self.__calc_x_by_addition(0, self.__V_vector.values)
        if store:
            self.__store_X(x_vector)
        return x_vector

    def calc_x_from_f_and_y(self, store=True):
        x_vector = self.__calc_x_by_addition(1, self.__Y_vector.values)
        if store:
            self.__store_X(x_vector)
        return x_vector

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
        print('%s internally stored with following values:\n%s' % (vector_name, values))

    # ====================================
    #       private calculation methods
    # ====================================

    def __calc_x_by_addition(self, dimension, externality_vector):
        # sum all inputs for each sector from other sectors
        col_sum_f = self.__F_matrix.sum(dimension)
        # add the value added (V)
        total_input_output_values = col_sum_f.values + externality_vector
        # create a new series containing values for X
        x_vector = pd.Series(data=total_input_output_values, index=self.__F_matrix.keys())
        return x_vector

    # ====================================
    #       private storage methods
    # ====================================

    def __store_X(self, values):
        self.__X_vector = values
        if self.__verbose:
            self.__print_storage('X vector', values)


# Temporary testing environment
if __name__ == '__main__':

    input_directory = './sample input/'
    F_file = input_directory + 'F_table.csv'
    V_file = input_directory + 'V_table.csv'

    model = BSymIO(f_matrix=F_file, v_vector=V_file)

    model.calc_x_from_f_and_v()
