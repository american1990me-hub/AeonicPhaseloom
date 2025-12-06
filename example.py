#!/usr/bin/env python3
"""
Example demonstrating the Aeonic Phaseloom engine capabilities.
"""

import numpy as np
from phaseloom import Engine, Thread


def custom_update_rule(thread, thread_index, time):
    """
    Custom update rule with more complex dynamics.
    Threads interact based on their phase differences.
    """
    # Position evolves based on phase
    position_delta = 0.05 * np.cos(thread.phase + time * 0.01)
    
    # Phase advances with coupling to position
    phase_delta = 0.15 + 0.02 * np.sin(thread.position)
    
    # No symbol update
    new_symbol = None
    
    return position_delta, phase_delta, new_symbol


def main():
    print("=" * 60)
    print("Aeonic Phaseloom - Example Simulation")
    print("=" * 60)
    
    # Example 1: Basic simulation with default update rule
    print("\n--- Example 1: Basic 9-thread simulation ---")
    engine1 = Engine(num_threads=9)
    
    print("Initial state:")
    engine1.print_state()
    
    # Run for 50 steps
    engine1.run(steps=50, record_interval=10)
    
    print("\nFinal state:")
    engine1.print_state()
    
    # Show coherence evolution
    coherence_data = engine1.get_coherence_over_time()
    print("\nCoherence evolution:")
    for time, coherence in coherence_data:
        print(f"  t={time:3d}: C(t)={coherence:.4f}")
    
    # Example 2: Custom update rule
    print("\n\n--- Example 2: Custom update rule (6 threads) ---")
    engine2 = Engine(num_threads=6)
    
    print("Initial state:")
    engine2.print_state()
    
    # Run with custom rule
    engine2.run(steps=30, update_rule=custom_update_rule, record_interval=10)
    
    print("\nFinal state:")
    engine2.print_state()
    
    # Example 3: Analyzing triad balance
    print("\n\n--- Example 3: Triad balance analysis ---")
    engine3 = Engine(num_threads=5)
    
    # Run simulation
    engine3.run(steps=20, record_interval=5)
    
    # Analyze triads at different time points
    history = engine3.get_history()
    print(f"\nTriad balance evolution (total {len(history)} snapshots):")
    
    for state in history:
        time = state['time']
        coherence = state['coherence']
        triads = state['triad_balances']
        
        # Find max and min triad balance
        max_triad = max(triads, key=lambda x: x[1])
        min_triad = min(triads, key=lambda x: x[1])
        
        print(f"\n  t={time}: Overall coherence={coherence:.4f}")
        print(f"    Max triad balance: threads {max_triad[0]} -> {max_triad[1]:.4f}")
        print(f"    Min triad balance: threads {min_triad[0]} -> {min_triad[1]:.4f}")
    
    # Example 4: Different thread configurations
    print("\n\n--- Example 4: Comparing different thread counts ---")
    for n in [3, 6, 9, 12]:
        engine = Engine(num_threads=n)
        engine.run(steps=50)
        
        coherence_data = engine.get_coherence_over_time()
        initial_coherence = coherence_data[0][1]
        final_coherence = coherence_data[-1][1]
        
        print(f"  N={n:2d} threads: C(0)={initial_coherence:.4f}, "
              f"C(50)={final_coherence:.4f}, "
              f"ΔC={final_coherence - initial_coherence:+.4f}")
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
