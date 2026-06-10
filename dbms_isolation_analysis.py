# IsoRel: Dependency Inference

def infer_dependencies(history):
    dependencies = []
    wList = {}  # Tracks the last transaction to write a rowId

    for txn, op, rowId in history:
        if op == 'W':
            if rowId in wList:
                dependencies.append(f"{wList[rowId]} --WW--> {txn}")
            wList[rowId] = txn
        elif op == 'R':
            if rowId in wList:
                dependencies.append(f"{wList[rowId]} --WR--> {txn}")
    return dependencies

# Example Execution History with Duplicate Row Identifiers
history = [('T1', 'W', 'r1'), ('T2', 'R', 'r1'), ('T3', 'W', 'r1')]

print("Inferred Dependencies:")
for dep in infer_dependencies(history):
    print(dep)

# Output:
# T1 --WR--> T2
# T1 --WW--> T3


# VeriStrong: SMT Verification

from z3 import Solver, Bool, Xor, sat

# Scenario: T1: W(x,1), T2: W(x,1), T3: R(x,1)
# Uncertainty: Did T3 read from T1 or T2?
solver = Solver()

# Boolean variables representing potential WR edges
WR_1_3 = Bool('WR_1_3')
WR_2_3 = Bool('WR_2_3')

# Constraint 1: Uniqueness (Exactly one WR edge must be true)
solver.add(Xor(WR_1_3, WR_2_3))

# Constraint 2: Order-Guided Polarity Picking
# Assume Session Order dictates T1 -> SO -> T2.
# T3 reading from T1 might violate order, so we prune it.
solver.add(WR_1_3 == False)

if solver.check() == sat:
    model = solver.model()
    print("Resolved Compatible Graph Edges:")
    if model[WR_1_3]: print("T1 --WR--> T3")
    if model[WR_2_3]: print("T2 --WR--> T3")

# Output:
# Resolved Compatible Graph Edges:
# T2 --WR--> T3
