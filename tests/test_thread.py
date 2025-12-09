"""
Unit tests for the Phaseloom Thread class.
"""

import unittest
import numpy as np
from phaseloom import Thread


class TestThread(unittest.TestCase):
    """Test cases for the Thread class."""
    
    def test_initialization_default(self):
        """Test thread initialization with default values."""
        thread = Thread()
        self.assertEqual(thread.position, 0.0)
        self.assertEqual(thread.phase, 0.0)
        self.assertIsNone(thread.symbol)
    
    def test_initialization_custom(self):
        """Test thread initialization with custom values."""
        thread = Thread(position=5.0, phase=np.pi, symbol="A")
        self.assertEqual(thread.position, 5.0)
        self.assertEqual(thread.phase, np.pi)
        self.assertEqual(thread.symbol, "A")
    
    def test_update_position(self):
        """Test position update."""
        thread = Thread(position=1.0)
        thread.update(position_delta=2.5)
        self.assertAlmostEqual(thread.position, 3.5)
    
    def test_update_phase(self):
        """Test phase update and normalization."""
        thread = Thread(phase=0.0)
        thread.update(phase_delta=np.pi)
        self.assertAlmostEqual(thread.phase, np.pi)
        
        # Test phase wrapping
        thread.update(phase_delta=1.5 * np.pi)
        expected = (np.pi + 1.5 * np.pi) % (2 * np.pi)
        self.assertAlmostEqual(thread.phase, expected)
    
    def test_update_symbol(self):
        """Test symbol update."""
        thread = Thread(symbol="A")
        thread.update(new_symbol="B")
        self.assertEqual(thread.symbol, "B")
        
        # Test that None doesn't change symbol
        thread.update(new_symbol=None)
        self.assertEqual(thread.symbol, "B")
    
    def test_get_state(self):
        """Test state retrieval."""
        thread = Thread(position=3.5, phase=1.2, symbol="X")
        state = thread.get_state()
        
        self.assertIn('position', state)
        self.assertIn('phase', state)
        self.assertIn('symbol', state)
        self.assertEqual(state['position'], 3.5)
        self.assertEqual(state['phase'], 1.2)
        self.assertEqual(state['symbol'], "X")
    
    def test_repr(self):
        """Test string representation."""
        thread = Thread(position=1.5, phase=0.5, symbol="T")
        repr_str = repr(thread)
        self.assertIn("Thread", repr_str)
        self.assertIn("x=1.500", repr_str)
        self.assertIn("θ=0.500", repr_str)
        self.assertIn("σ=T", repr_str)


if __name__ == '__main__':
    unittest.main()
