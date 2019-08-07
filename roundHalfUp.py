# copied from 15112 course note
# https://www.cs.cmu.edu/~112-n19/notes/notes-data-and-exprs.html

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding)) 