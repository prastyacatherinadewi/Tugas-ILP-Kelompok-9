

# =========================================================
# INSTRUCTION-LEVEL PARALLELISM SIMULATOR
# Hazard: WAR (Write After Read)
# =========================================================

from dataclasses import dataclass


@dataclass
class Instruction:
    name: str
    destination: str
    sources: list


# ---------------------------------------------------------
# Instruction Set
# ---------------------------------------------------------

instructions = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R4", ["R5", "R6"]),
    Instruction("I3", "R2", ["R7", "R8"]),
    Instruction("I4", "R9", ["R1", "R10"]),
    Instruction("I5", "R5", ["R11", "R12"]),
    Instruction("I6", "R13", ["R14", "R15"]),
]


# ---------------------------------------------------------
# WAR Dependency Detection
# ---------------------------------------------------------

def has_dependency(inst1, inst2):
    # WAR: inst1 reads a register that inst2 writes
    return inst2.destination in inst1.sources


# ---------------------------------------------------------
# Dependency Analysis and Graph
# ---------------------------------------------------------

def show_dependencies(instructions):
    print("\n" + "=" * 60)
    print("WAR DEPENDENCY ANALYSIS")
    print("=" * 60)

    edges = []

    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            first = instructions[i]
            second = instructions[j]

            if has_dependency(first, second):
                register = second.destination
                edges.append((first.name, second.name, register))

                print(
                    f"{second.name} depends on {first.name} "
                    f"(WAR: {register})"
                )

    if not edges:
        print("No WAR dependencies found.")

    print("\nDEPENDENCY GRAPH")
    print("-" * 60)

    for first, second, register in edges:
        print(f"{first} --WAR({register})--> {second}")

    if not edges:
        print("No dependency edges.")

    return edges


# ---------------------------------------------------------
# Sequential Execution
# ---------------------------------------------------------

def sequential_execution(instructions):
    print("\n" + "=" * 60)
    print("SEQUENTIAL EXECUTION")
    print("=" * 60)

    for cycle, inst in enumerate(instructions, start=1):
        print(
            f"Cycle {cycle}: {inst.name}: "
            f"{inst.destination} = {' + '.join(inst.sources)}"
        )

    print(f"\nTotal Sequential Cycles: {len(instructions)}")
    return len(instructions)


# ---------------------------------------------------------
# ILP / Parallel Execution
# ---------------------------------------------------------

def parallel_execution(instructions, edges):
    print("\n" + "=" * 60)
    print("WAR PARALLEL EXECUTION")
    print("=" * 60)

    completed = set()
    remaining = instructions.copy()
    cycle = 0

    while remaining:
        cycle += 1
        current_cycle = []

        for inst in remaining:
            dependencies = [
                first
                for first, second, register in edges
                if second == inst.name
            ]

            if all(dep in completed for dep in dependencies):
                current_cycle.append(inst)

        if not current_cycle:
            raise RuntimeError("Execution stalled.")

        print(f"\nCycle {cycle}:")

        for inst in current_cycle:
            print(
                f"  -> {inst.name}: "
                f"{inst.destination} = {' + '.join(inst.sources)}"
            )

        for inst in current_cycle:
            completed.add(inst.name)
            remaining.remove(inst)

    print(f"\nTotal ILP Cycles: {cycle}")
    return cycle


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

def main():
    print("\n" + "*" * 60)
    print("      INSTRUCTION-LEVEL PARALLELISM SIMULATOR")
    print("                  HAZARD: WAR")
    print("*" * 60)

    print("\nInstruction Set:")

    for inst in instructions:
        print(
            f"{inst.name}: "
            f"{inst.destination} = {' + '.join(inst.sources)}"
        )

    edges = show_dependencies(instructions)

    sequential_cycles = sequential_execution(instructions)
    parallel_cycles = parallel_execution(instructions, edges)

    speedup = sequential_cycles / parallel_cycles
    efficiency = speedup / len(instructions) * 100

    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    print(f"Sequential Cycles : {sequential_cycles}")
    print(f"ILP Cycles        : {parallel_cycles}")
    print(f"Speedup           : {speedup:.2f}x")
    print(f"ILP Efficiency    : {efficiency:.2f}%")

    print("\nConclusion:")
    print(
        "WAR dependencies preserve the original read-before-write "
        "order of instructions."
    )
    print(
        "Independent instructions can execute in parallel, "
        "while dependent writes must wait for earlier reads."
    )


if __name__ == "__main__":
    main()
