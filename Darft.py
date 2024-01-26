from sympy import simplify, lambdify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf


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
    disjunctions = expr.args if isinstance(expr, Or) else [expr]
    overlaps = []

    for i in range(len(disjunctions)):
        for j in range(i+1, len(disjunctions)):
            common_attributes = set(disjunctions[i].atoms()) & set(disjunctions[j].atoms())
            if common_attributes:
                overlaps.append((i, j + i + 1, common_attributes))

    return overlaps



def resolve_overlaps(expr, overlaps):
    for overlap in overlaps:
        literal = overlap[2].pop()
        conj1_index, conj2_index = overlap[0], overlap[1]

        expr = replace_overlapping_conjunctions(expr, conj1_index, conj2_index, literal)

    return expr

def replace_overlapping_conjunctions(expr, conj1_index, conj2_index, literal):
    conjunctions = expr.args if isinstance(expr, And) else [expr]

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

    # Find an overlaps
    overlaps = find_overlaps(simplified_expr)
    print("An overlap of this logical expression is:", overlaps)

    # Step 3: Eliminate overlaps
    expr_without_overlaps = eliminate_overlaps(simplified_expr)
    print("Expression without Overlaps:", expr_without_overlaps)

    # Step 4: Transform innermost disjunctions to conjunctions and negations
    final_result = expr_without_overlaps.to_anf()
    print("Final Result after applying de Morgan law:", final_result)
