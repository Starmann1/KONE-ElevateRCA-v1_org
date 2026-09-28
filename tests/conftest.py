import sys
import os
import pytest

# Add root directory to python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.engine import ElevateRCAEngine


@pytest.fixture(scope="session")
def engine():
    """Session-scoped ElevateRCAEngine instance for fast test execution."""
    return ElevateRCAEngine(
        failure_modes_path="knowledge/failure_modes.yaml",
        causal_links_path="knowledge/causal_links.yaml",
        corrective_actions_path="knowledge/corrective_actions.yaml"
    )
