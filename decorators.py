def sufficientinfo(function):
    def _sufficientinfo(*args, **kwargs):

        f_provided = 'f_matrix' in kwargs
        a_provided = 'a_matrix' in kwargs

        y_provided = 'y_vector' in kwargs
        v_provided = 'v_abs_vector' in kwargs
        x_provided = 'x_vector' in kwargs

        any_externalities_provided = any((y_provided, v_provided, x_provided))
        output_externalities_provided = any((x_provided, y_provided))
        possibility_1 = (f_provided and any_externalities_provided)
        possibility_2 = (a_provided and output_externalities_provided)

        valid_input = (possibility_1 or possibility_2)

        if not valid_input:
            raise IOError('')

        return function(*args,**kwargs)
    return _sufficientinfo


def inputsfromset(input_sequence):
    def _inputsfromset(function):
        def __inputsfromset(*args, **kwargs):

            function_inputs = (kwargs[x] for x in kwargs)
            valid_input = all((x in input_sequence for x in function_inputs))

            if not valid_input:
                raise IOError('')

            return function(*args, **kwargs)
        return __inputsfromset
    return _inputsfromset