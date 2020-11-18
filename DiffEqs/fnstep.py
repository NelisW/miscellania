# The order of the arguments is very important - it must be exactly this way.
# see the Theano scan documentation for the reason why.
def fn_step(current_y,previous_x,coeff):
    # Even though this looks like just a normal Python function,
    # because it is using standard Python operators and Python is 
    # not a strongly typed language, Theano can use this 
    # and just drop in its own operators to overload + and *.
    return previous_x - coeff*previous_x + current_y

