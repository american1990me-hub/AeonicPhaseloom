#!/usr/bin/env python3
"""
Command-line interface for the Aeonic Phaseloom engine.
"""

import argparse
import json
import sys
from phaseloom import Engine


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Aeonic Phaseloom - Simulate threads with phase coherence"
    )
    
    parser.add_argument(
        '-n', '--threads',
        type=int,
        default=9,
        help='Number of threads to simulate (default: 9)'
    )
    
    parser.add_argument(
        '-s', '--steps',
        type=int,
        default=100,
        help='Number of time steps to simulate (default: 100)'
    )
    
    parser.add_argument(
        '-r', '--record-interval',
        type=int,
        default=1,
        help='Interval for recording state (default: 1, every step)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file for JSON results (default: print to stdout)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed state at each recorded interval'
    )
    
    args = parser.parse_args()
    
    # Create and run engine
    print(f"Initializing Aeonic Phaseloom with {args.threads} threads...")
    engine = Engine(num_threads=args.threads)
    
    if args.verbose:
        engine.print_state()
    
    print(f"Running simulation for {args.steps} steps...")
    engine.run(steps=args.steps, record_interval=args.record_interval)
    
    if args.verbose:
        engine.print_state()
    
    # Get results
    history = engine.get_history()
    coherence_data = engine.get_coherence_over_time()
    
    # Prepare output
    output_data = {
        'parameters': {
            'num_threads': args.threads,
            'steps': args.steps,
            'record_interval': args.record_interval
        },
        'coherence_over_time': [{'time': t, 'coherence': c} for t, c in coherence_data],
        'history': history
    }
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        # Print summary
        print("\n=== Simulation Summary ===")
        print(f"Initial coherence: {coherence_data[0][1]:.4f}")
        print(f"Final coherence: {coherence_data[-1][1]:.4f}")
        print(f"\nCoherence over time (sample every 10 steps):")
        for i, (t, c) in enumerate(coherence_data):
            if i % 10 == 0 or i == len(coherence_data) - 1:
                print(f"  t={t:3d}: C(t)={c:.4f}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
