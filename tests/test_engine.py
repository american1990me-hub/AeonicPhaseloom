"""
Unit tests for the Phaseloom Engine class.
"""

import unittest
import numpy as np
from phaseloom import Engine, Thread


class TestEngine(unittest.TestCase):
    """Test cases for the Engine class."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = Engine(num_threads=5)
        self.assertEqual(engine.num_threads, 5)
        self.assertEqual(len(engine.get_threads()), 5)
        self.assertEqual(engine.time, 0)
        self.assertEqual(len(engine.history), 0)
    
    def test_initial_thread_configuration(self):
        """Test that threads are initialized with proper spacing."""
        engine = Engine(num_threads=4)
        threads = engine.get_threads()
        
        # Check that threads have different initial phases
        phases = [t.phase for t in threads]
        self.assertEqual(len(set(phases)), 4)  # All different
        
        # Check that symbols are set
        for i, thread in enumerate(threads):
            self.assertEqual(thread.symbol, f"T{i}")
    
    def test_phase_coherence_fully_aligned(self):
        """Test coherence when all threads have same phase."""
        engine = Engine(num_threads=3)
        
        # Set all threads to same phase
        for thread in engine.get_threads():
            thread.phase = 0.0
        
        coherence = engine.compute_phase_coherence()
        self.assertAlmostEqual(coherence, 1.0, places=5)
    
    def test_phase_coherence_random(self):
        """Test coherence with random phases."""
        engine = Engine(num_threads=10)
        
        # Set random phases
        np.random.seed(42)
        for thread in engine.get_threads():
            thread.phase = np.random.uniform(0, 2 * np.pi)
        
        coherence = engine.compute_phase_coherence()
        # Random phases should give low coherence
        self.assertGreaterEqual(coherence, 0.0)
        self.assertLessEqual(coherence, 1.0)
    
    def test_triad_balance_aligned(self):
        """Test triad balance with aligned phases."""
        engine = Engine(num_threads=5)
        
        # Set specific phases
        for thread in engine.get_threads():
            thread.phase = 0.0
        
        balance = engine.compute_triad_balance((0, 1, 2))
        self.assertAlmostEqual(balance, 1.0, places=5)
    
    def test_triad_balance_validation(self):
        """Test that triad balance requires exactly 3 threads."""
        engine = Engine(num_threads=5)
        
        with self.assertRaises(ValueError):
            engine.compute_triad_balance((0, 1))
        
        with self.assertRaises(ValueError):
            engine.compute_triad_balance((0, 1, 2, 3))
    
    def test_compute_all_triads(self):
        """Test computing all triad balances."""
        engine = Engine(num_threads=4)
        triads = engine.compute_all_triad_balances()
        
        # For 4 threads, there are C(4,3) = 4 triads
        self.assertEqual(len(triads), 4)
        
        # Check format
        for indices, balance in triads:
            self.assertEqual(len(indices), 3)
            self.assertGreaterEqual(balance, 0.0)
            self.assertLessEqual(balance, 1.0)
    
    def test_update_default_rule(self):
        """Test default update rule."""
        engine = Engine(num_threads=3)
        
        initial_phases = [t.phase for t in engine.get_threads()]
        
        engine.update()
        
        # Check that phases changed (always happens with default rule)
        for i, thread in enumerate(engine.get_threads()):
            self.assertNotEqual(thread.phase, initial_phases[i])
        
        # Check time incremented
        self.assertEqual(engine.time, 1)
    
    def test_update_custom_rule(self):
        """Test custom update rule."""
        engine = Engine(num_threads=2)
        
        def custom_rule(thread, idx, time):
            return 1.0, 0.5, f"S{idx}"
        
        engine.update(update_rule=custom_rule)
        
        # Check that custom rule was applied
        for i, thread in enumerate(engine.get_threads()):
            self.assertEqual(thread.symbol, f"S{i}")
    
    def test_get_state(self):
        """Test state retrieval."""
        engine = Engine(num_threads=3)
        state = engine.get_state()
        
        self.assertIn('time', state)
        self.assertIn('threads', state)
        self.assertIn('coherence', state)
        self.assertIn('triad_balances', state)
        
        self.assertEqual(len(state['threads']), 3)
        self.assertIsInstance(state['coherence'], float)
        self.assertIsInstance(state['triad_balances'], list)
    
    def test_record_state(self):
        """Test state recording."""
        engine = Engine(num_threads=3)
        
        engine.record_state()
        self.assertEqual(len(engine.history), 1)
        
        engine.update()
        engine.record_state()
        self.assertEqual(len(engine.history), 2)
        
        # Check that states are different
        self.assertNotEqual(engine.history[0]['time'], engine.history[1]['time'])
    
    def test_run_simulation(self):
        """Test running a simulation."""
        engine = Engine(num_threads=4)
        
        engine.run(steps=10, record_interval=2)
        
        # Should have recorded at steps 0, 2, 4, 6, 8, and final (10)
        # That's 6 recordings total
        self.assertEqual(len(engine.history), 6)
        self.assertEqual(engine.time, 10)
    
    def test_get_coherence_over_time(self):
        """Test extracting coherence time series."""
        engine = Engine(num_threads=3)
        engine.run(steps=5)
        
        coherence_data = engine.get_coherence_over_time()
        
        # Should have 6 points (0, 1, 2, 3, 4, 5)
        self.assertEqual(len(coherence_data), 6)
        
        # Check format
        for time, coherence in coherence_data:
            self.assertIsInstance(time, int)
            self.assertIsInstance(coherence, float)
            self.assertGreaterEqual(coherence, 0.0)
            self.assertLessEqual(coherence, 1.0)


if __name__ == '__main__':
    unittest.main()
