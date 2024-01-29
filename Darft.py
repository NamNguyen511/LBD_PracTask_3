from sympy import Symbol, sympify, simplify_logic
from sympy.logic.boolalg import Or, And, Not, to_dnf

# Define variables and weights
variables = ['a', 'b', 'c', 'd', 'e']
weights = ['w_a','w_b','w_c','w_d','w_e']

# Dummy input expression for demonstration
input_expr = "a & b | c & d | e & ~b"

def disjunctive_normal_form(expr):
    return to_dnf(expr)

def simplify_expression(expr):
    return simplify_logic(expr, form="dnf")

def find_overlaps(expr):
    common_attributes = set()
    for i, conj in enumerate(expr.args):
        for other_conj in expr.args[i+1:]:
            common_attributes |= set(literal for literal in conj.args if literal in other_conj.args)
    return common_attributes

def resolve_overlaps(expr, o):
  disjunctions = expr.args if isinstance(expr, Or) else [expr]
  new_dnf = []
  for conj in disjunctions:
    if o in conj.free_symbols:
      new_dnf.append(conj)
    else:
      new_dnf.append(And(o, conj))
      new_dnf.append(And(Not(o), conj))
  return Or(*new_dnf)

if __name__ == "__main__":
    expr = sympify(input_expr)
    print("Original Expression:", expr)

    # Transform to disjunctive normal form
    dnf_expr = disjunctive_normal_form(expr)
    print("Disjunctive Normal Form:", dnf_expr)

    # Simplify expression
    simplified_expr = simplify_expression(dnf_expr)
    print("Simplified Expression:", simplified_expr)

    # Find an overlaps
    overlaps = find_overlaps(simplified_expr)
    print("An overlap of this logical expression is:", overlaps)

    # Eliminate overlaps
    if overlaps:
        o = overlaps.pop()
        expr_without_overlaps = resolve_overlaps(simplified_expr, o)
        print("Expression without Overlaps:", expr_without_overlaps)
    else:
        expr_without_overlaps = simplified_expr

    # Applying de Morgan's law
    final_result = simplify_logic(expr_without_overlaps, form="dnf")
    print("Final Result after applying de Morgan's law:", final_result)
