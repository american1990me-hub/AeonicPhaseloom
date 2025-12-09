# AeonicPhaseloom

Phaseloom is a bundle of moving threads. Each thread has a path in space, a spinning phase, and an optional symbol. Together they form braids whose alignment measures coherence, decoherence, and recoherence across a 3–6–9 / 27-node structure.

## Features

The Aeonic Phaseloom engine simulates **N threads**, each with:
- **Position** `x(t)`: Spatial position evolving over time
- **Phase** `θ(t)`: Angular phase in radians, continuously rotating
- **Symbol** `σ(t)`: Optional symbolic identifier

The engine computes:
- **Global Phase Coherence**: `C(t) = |(1/N)∑exp(iθ)|` - measures alignment of all threads (0 = incoherent, 1 = fully coherent)
- **Triad Balance**: Phase coherence for all 3-thread combinations - measures local alignments
- **Time-series Output**: Complete history of states and coherence values

## Installation

### Dependencies
```bash
pip install -r requirements.txt
```

### Development Installation
```bash
pip install -e .
```

## Usage

### Python API

```python
from phaseloom import Engine

# Create engine with 9 threads
engine = Engine(num_threads=9)

# Run simulation for 100 steps
engine.run(steps=100)

# Get coherence over time
coherence_data = engine.get_coherence_over_time()
for time, coherence in coherence_data[:5]:
    print(f"t={time}: C(t)={coherence:.4f}")

# Analyze triad balances
state = engine.get_state()
for indices, balance in state['triad_balances'][:5]:
    print(f"Threads {indices}: balance={balance:.4f}")
```

### Custom Update Rules

You can define custom dynamics for thread evolution:

```python
def my_update_rule(thread, thread_index, time):
    """Custom rule: position drifts, phase couples to position."""
    position_delta = 0.1 * np.sin(time * 0.1)
    phase_delta = 0.2 + 0.01 * thread.position
    new_symbol = None  # Keep current symbol
    return position_delta, phase_delta, new_symbol

engine = Engine(num_threads=6)
engine.run(steps=50, update_rule=my_update_rule)
```

### Command-Line Interface

```bash
# Basic run with 9 threads for 100 steps
python3 phaseloom_cli.py

# Custom configuration
python3 phaseloom_cli.py --threads 12 --steps 200 --record-interval 5

# Verbose output showing detailed states
python3 phaseloom_cli.py --threads 6 --steps 50 --verbose

# Save results to JSON file
python3 phaseloom_cli.py --threads 9 --steps 100 --output results.json

# Show help
python3 phaseloom_cli.py --help
```

### Example Script

Run the comprehensive examples:

```bash
python3 example.py
```

This demonstrates:
1. Basic 9-thread simulation with default dynamics
2. Custom update rules with 6 threads
3. Detailed triad balance analysis
4. Comparison of different thread counts

## Architecture

### Thread Class (`phaseloom/thread.py`)
- Represents a single thread with position, phase, and symbol
- Provides update methods with automatic phase normalization
- State extraction and representation

### Engine Class (`phaseloom/engine.py`)
- Manages N threads and their evolution
- Computes global phase coherence: `C(t) = |(1/N)∑exp(iθ)|`
- Computes triad balance for all 3-thread combinations
- Records state history for analysis
- Supports custom update rules

## Testing

Run the test suite:

```bash
# Using unittest
python3 -m unittest discover -s tests -v

# Run specific test file
python3 -m unittest tests.test_engine -v
```

All tests validate:
- Thread initialization and updates
- Phase normalization
- Coherence calculations
- Triad balance computations
- State recording and history
- Custom update rules

## Examples Output

```
=== Time step: 50 ===
Phase Coherence: 0.1533

Threads:
  Thread 0 (T0): x=0.076, θ=5.000
  Thread 1 (T1): x=0.983, θ=6.198
  Thread 2 (T2): x=1.978, θ=1.113
  ...

Triad Balances (top 5):
  Threads (2, 3, 8): 0.8742
  Threads (1, 6, 7): 0.8742
  ...
```

## Mathematical Background

### Phase Coherence
The global phase coherence is computed as the magnitude of the average complex phasor:

```
C(t) = |⟨exp(iθ)⟩| = |(1/N) ∑ₙ exp(iθₙ)|
```

Where:
- `C(t) = 1`: Perfect coherence (all phases aligned)
- `C(t) = 0`: Complete incoherence (random phases)
- `0 < C(t) < 1`: Partial coherence

### Triad Balance
For any three threads (i, j, k), the triad balance measures their mutual phase alignment:

```
B(i,j,k) = |(1/3) ∑ exp(iθ)|
```

This captures local coherence patterns within the larger ensemble.

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
