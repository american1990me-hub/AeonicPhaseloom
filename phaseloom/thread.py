"""
Thread class representing a single thread in the Phaseloom.
Each thread has position x(t), phase θ(t), and optional symbol σ(t).
"""

import numpy as np
from typing import Optional


class Thread:
    """
    Represents a single thread with position, phase, and optional symbol.
    
    Attributes:
        position (float): The spatial position x(t) of the thread
        phase (float): The phase angle θ(t) in radians
        symbol (Optional[str]): An optional symbolic identifier σ(t)
    """
    
    def __init__(self, position: float = 0.0, phase: float = 0.0, symbol: Optional[str] = None):
        """
        Initialize a thread with position, phase, and optional symbol.
        
        Args:
            position: Initial position x(0)
            phase: Initial phase θ(0) in radians
            symbol: Optional symbolic identifier
        """
        self.position = position
        self.phase = phase
        self.symbol = symbol
    
    def update(self, position_delta: float = 0.0, phase_delta: float = 0.0, 
               new_symbol: Optional[str] = None):
        """
        Update the thread state by applying deltas.
        
        Args:
            position_delta: Change in position
            phase_delta: Change in phase (radians)
            new_symbol: Optional new symbol (if None, keeps current)
        """
        self.position += position_delta
        self.phase += phase_delta
        # Normalize phase to [0, 2π)
        self.phase = self.phase % (2 * np.pi)
        
        if new_symbol is not None:
            self.symbol = new_symbol
    
    def get_state(self) -> dict:
        """
        Get the current state of the thread.
        
        Returns:
            Dictionary containing position, phase, and symbol
        """
        return {
            'position': self.position,
            'phase': self.phase,
            'symbol': self.symbol
        }
    
    def __repr__(self) -> str:
        symbol_str = f", σ={self.symbol}" if self.symbol else ""
        return f"Thread(x={self.position:.3f}, θ={self.phase:.3f}{symbol_str})"
