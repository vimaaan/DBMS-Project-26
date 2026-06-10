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
