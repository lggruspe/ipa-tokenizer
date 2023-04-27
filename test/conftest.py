# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Some pytest stuff."""
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add options to pytest."""
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="run slow tests",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Add 'slow' marker."""
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Skip slow tests if not `--runslow`."""
    if config.getoption("--runslow"):
        return

    # Skip slow tests.
    skip_slow = pytest.mark.skip(reason="requires --runslow option")
    for item in items:
        # Usage: @pytest.mark.slow
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
