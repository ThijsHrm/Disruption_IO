import numpy as np
import pandas as pd


# Basic Symmetric IO Model
class BSymIO:

    # ====================================
    #       init function
    # ====================================

    def __init__(self, f_matrix, y_vector, v_vector, verbose=True):

        self.__F_matrix = pd.read_csv(f_matrix, index_col=0)
        self.__Y_vector = pd.Series.from_csv(y_vector, index_col=0)
        self.__V_vector = pd.Series.from_csv(v_vector, index_col=0)
        self.__X_vector = self.__calc_X()

        self.__verbose = verbose

        self.__print_initialization(True)

    # ====================================
    #       public methods
    # ====================================

    def public_method(self):
        pass

    # ====================================
    #       communication methods
    # ====================================

    # print loaded matrices if verbose = true
    def __print_initialization(self, success):
        if success:
            print("Basic Symmetric IO Model Initiated\n\n")
            print("F matrix:\n%s\n\n" % self.__F_matrix)
            print("Y vector:\n%s\n\n" % self.__Y_vector)
            print("V vector:\n%s\n\n" % self.__V_vector)
            print("X vector:\n%s\n\n" % self.__X_vector)

    # ====================================
    #       calculation methods
    # ====================================

    # __calc_X method assesses which function to call in order to
    # calculate X depending on which information is available
    def __calc_x(self):
        # placeholder
        return self.__calc_x_from_f_and_v()

    # calculate X from F and V
    def __calc_x_from_f_and_v(self):
        # sum all inputs for each sector from other sectors
        col_sum_F = self.__F_matrix.sum(0)
        # add the value added (V)
        total_input_output_values = col_sum_F.values + self.__V_vector.values
        # create a new series containing values for X
        x_vector = pd.Series(data=total_input_output_values, index=self.__F_matrix.keys())
        return x_vector


# Temporary testing environment
if __name__ == '__main__':

    input_directory = './sample input/'
    F_file = input_directory + 'F_table.csv'
    Y_file = input_directory + 'Y_table.csv'
    V_file = input_directory + 'V_table.csv'

    model = BSymIO(f_matrix=F_file, y_vector=Y_file, v_vector=V_file)
