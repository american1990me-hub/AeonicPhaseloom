"""
Engine class for managing and simulating the Aeonic Phaseloom.
Handles N threads, computes phase coherence and triad balance.
"""

import numpy as np
from typing import List, Dict, Tuple, Callable, Optional
from .thread import Thread
from itertools import combinations


class Engine:
    """
    The Aeonic Phaseloom engine that manages multiple threads and computes
    global phase coherence and triad balance.
    """
    
    def __init__(self, num_threads: int = 9):
        """
        Initialize the engine with N threads.
        
        Args:
            num_threads: Number of threads to simulate
        """
        self.num_threads = num_threads
        self.threads: List[Thread] = []
        self.history: List[Dict] = []
        self.time = 0
        
        # Initialize threads with default values
        for i in range(num_threads):
            # Space threads evenly in position and phase
            position = i * 1.0
            phase = (2 * np.pi * i) / num_threads
            symbol = f"T{i}"
            self.threads.append(Thread(position, phase, symbol))
    
    def get_threads(self) -> List[Thread]:
        """Get all threads."""
        return self.threads
    
    def compute_phase_coherence(self) -> float:
        """
        Compute global phase coherence: C(t) = |(1/N)∑exp(iθ)|
        
        Returns:
            Phase coherence value between 0 (incoherent) and 1 (fully coherent)
        """
        if not self.threads:
            return 0.0
        
        # Sum of exp(i*theta) for all threads
        complex_sum = sum(np.exp(1j * thread.phase) for thread in self.threads)
        
        # Average and take magnitude
        coherence = np.abs(complex_sum / self.num_threads)
        
        return float(coherence)
    
    def compute_triad_balance(self, indices: Tuple[int, int, int]) -> float:
        """
        Compute balance for a triad (3-thread group).
        Triad balance measures phase alignment among three threads.
        
        Args:
            indices: Tuple of three thread indices
            
        Returns:
            Triad balance value (magnitude of average phase vector)
        """
        if len(indices) != 3:
            raise ValueError("Triad must have exactly 3 threads")
        
        # Get phases for the three threads
        phases = [self.threads[i].phase for i in indices]
        
        # Compute average phase vector
        complex_sum = sum(np.exp(1j * phase) for phase in phases)
        balance = np.abs(complex_sum / 3.0)
        
        return float(balance)
    
    def compute_all_triad_balances(self) -> List[Tuple[Tuple[int, int, int], float]]:
        """
        Compute triad balance for all possible 3-thread combinations.
        
        Returns:
            List of tuples: ((i, j, k), balance) for each triad
        """
        triads = []
        
        # Generate all combinations of 3 threads
        for indices in combinations(range(self.num_threads), 3):
            balance = self.compute_triad_balance(indices)
            triads.append((indices, balance))
        
        return triads
    
    def update(self, update_rule: Optional[Callable[[Thread, int, int], Tuple[float, float, Optional[str]]]] = None):
        """
        Update all threads using the provided update rule.
        
        Args:
            update_rule: Function that takes (thread, thread_index, time) and returns
                        (position_delta, phase_delta, new_symbol)
                        If None, uses default simple rule
        """
        if update_rule is None:
            # Default simple update rule
            update_rule = self._default_update_rule
        
        for i, thread in enumerate(self.threads):
            position_delta, phase_delta, new_symbol = update_rule(thread, i, self.time)
            thread.update(position_delta, phase_delta, new_symbol)
        
        self.time += 1
    
    def _default_update_rule(self, thread: Thread, thread_index: int, time: int) -> Tuple[float, float, Optional[str]]:
        """
        Default update rule: simple rotation and drift.
        
        Args:
            thread: The thread to update
            thread_index: Index of the thread
            time: Current time step
            
        Returns:
            Tuple of (position_delta, phase_delta, new_symbol)
        """
        # Position drifts slowly
        position_delta = 0.01 * np.sin(thread.phase)
        
        # Phase advances, with slight variation per thread
        phase_delta = 0.1 + 0.01 * thread_index
        
        # Keep symbol unchanged
        new_symbol = None
        
        return position_delta, phase_delta, new_symbol
    
    def get_state(self) -> Dict:
        """
        Get current state of all threads and computed metrics.
        
        Returns:
            Dictionary with time, thread states, coherence, and triad balances
        """
        thread_states = [thread.get_state() for thread in self.threads]
        coherence = self.compute_phase_coherence()
        triad_balances = self.compute_all_triad_balances()
        
        return {
            'time': self.time,
            'threads': thread_states,
            'coherence': coherence,
            'triad_balances': triad_balances
        }
    
    def record_state(self):
        """Record the current state to history."""
        self.history.append(self.get_state())
    
    def run(self, steps: int, update_rule: Optional[Callable] = None, record_interval: int = 1):
        """
        Run the simulation for a given number of steps.
        
        Args:
            steps: Number of time steps to simulate
            update_rule: Optional custom update rule function
            record_interval: How often to record state (1 = every step)
        """
        for step in range(steps):
            if step % record_interval == 0:
                self.record_state()
            self.update(update_rule)
        
        # Record final state
        self.record_state()
    
    def get_history(self) -> List[Dict]:
        """Get the full history of recorded states."""
        return self.history
    
    def get_coherence_over_time(self) -> List[Tuple[int, float]]:
        """
        Extract coherence values over time from history.
        
        Returns:
            List of (time, coherence) tuples
        """
        return [(state['time'], state['coherence']) for state in self.history]
    
    def print_state(self):
        """Print the current state in a readable format."""
        state = self.get_state()
        print(f"\n=== Time step: {state['time']} ===")
        print(f"Phase Coherence: {state['coherence']:.4f}")
        print(f"\nThreads:")
        for i, thread_state in enumerate(state['threads']):
            symbol = thread_state['symbol'] or 'None'
            print(f"  Thread {i} ({symbol}): x={thread_state['position']:.3f}, "
                  f"θ={thread_state['phase']:.3f}")
        
        print(f"\nTriad Balances (top 5):")
        sorted_triads = sorted(state['triad_balances'], key=lambda x: x[1], reverse=True)
        for indices, balance in sorted_triads[:5]:
            print(f"  Threads {indices}: {balance:.4f}")
