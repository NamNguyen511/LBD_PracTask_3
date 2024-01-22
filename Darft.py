from sympy import simplify, lambdify
from sympy.logic.boolalg import Or, And, Not, to_dnf, simplify_logic
from sympy.abc import x, y, z  # Assuming your logical expressions involve these variables

# Define variables and weights
variables = ['a', 'b', 'c', 'd', 'e']
weights = ['w_a','w_b','w_c','w_d','w_e']

def user_input():
    # Create dictionaries to store the values of the variables and weights
    var_values = {}
    weight_values = {}

    # Get the values for the variables from the user
    for var in variables:
        value = float(input(f"Please enter a value for {var} (between [0,1]): "))
        var_values[var] = value

    # Get the values of weights for the variables from the user
    for weight in weights[:3]:
        value = float(input(f"Please enter a value for {weight} (between [0,1]): "))
        weight_values[weight] = value

    # Ask the user if they want to input more weights (maximum: 5 weights)
    """
    This implementation will be expected at least three weight's input from the user
    .If type "yes", user will input more weights manually, otherwise assign the weights to 1 automatically.
    """

    for weight in weights[3:]:
        answer = input(f"Do you want to input the {weight}? (yes/no): ")
        if answer.lower() == "yes":
            value = float(input(f"Please enter a value for {weight} (between [0,1]): "))
            weight_values[weight] = value
        else:
            weight_values[weight] = 1

    # Get the logical expression from the user
    expr_str = input("Please input a logical expression: ")
    return expr_str
def disjunctive_normal_form(expr):
    return to_dnf(expr)

def simplify_expression(expr):
    return expr.simplify()

def eliminate_overlaps(expr):
    while True:
        overlaps = find_overlaps(expr)
        if not overlaps:
            break

        expr = resolve_overlaps(expr, overlaps)

    return expr

def find_overlaps(expr):
    conjunctions = expr.args if isinstance(expr, And) else [expr]
    overlaps = []

    for i, conj1 in enumerate(conjunctions):
        for j, conj2 in enumerate(conjunctions[i + 1:]):
            common_attributes = find_common_attributes(conj1, conj2)
            if common_attributes:
                overlaps.append((i, j + i + 1, common_attributes))

    return overlaps

def find_common_attributes(conj1, conj2):
    literals1 = conj1.args if isinstance(conj1, And) else [conj1]
    literals2 = conj2.args if isinstance(conj2, And) else [conj2]

    common_attributes = set()
    for lit1 in literals1:
        if isinstance(lit1, Not):
            lit1 = lit1.args[0]
        for lit2 in literals2:
            if isinstance(lit2, Not):
                lit2 = lit2.args[0]
            if lit1 == lit2:
                common_attributes.add(lit1)

    return common_attributes

def resolve_overlaps(expr, overlaps):
    for overlap in overlaps:
        literal = overlap[2].pop()
        conj1_index, conj2_index = overlap[0], overlap[1]

        expr = replace_overlapping_conjunctions(expr, conj1_index, conj2_index, literal)

    return simplify_expression(expr)

def replace_overlapping_conjunctions(expr, conj1_index, conj2_index, literal):
    conjunctions = expr.args if isinstance(expr, Or) else [expr]

    conj1 = conjunctions[conj1_index]
    conj2 = conjunctions[conj2_index]

    new_conj1 = (literal & conj1) | (~literal & conj1)
    new_conj2 = (~literal & conj2) | (literal & conj2)

    conjunctions.pop(conj2_index)
    conjunctions.pop(conj1_index)
    conjunctions.append(new_conj1)
    conjunctions.append(new_conj2)

    return Or(*conjunctions)

if __name__ == "__main__":
    # Example usage
    input_expr = user_input()
    print("Original Expression:", input_expr)

    # Step 1: Transform to disjunctive normal form
    dnf_expr = disjunctive_normal_form(input_expr)
    print("Disjunctive Normal Form:", dnf_expr)

    # Step 2: Simplify expression
    simplified_expr = simplify_expression(dnf_expr)
    print("Simplified Expression:", simplified_expr)

    # Step 3: Eliminate overlaps
    expr_without_overlaps = eliminate_overlaps(simplified_expr)
    print("Expression without Overlaps:", expr_without_overlaps)

    # Step 4: Transform innermost disjunctions to conjunctions and negations
    final_result = expr_without_overlaps.to_anf()
    print("Final Result after applying de Morgan law:", final_result)
