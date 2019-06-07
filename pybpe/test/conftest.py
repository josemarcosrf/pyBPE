import pytest
import os

from pybpe import pyBPE


TESTS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def train_text():
    return "this test is a simple sample test"


@pytest.fixture
def test_text():
    return "this is the simplest example"


@pytest.fixture
def vocab():
    with open(os.path.join(TESTS_DIRECTORY, "fixtures", "vocab"), 'r') as f:
        return f.read()


@pytest.fixture
def codes():
    with open(os.path.join(TESTS_DIRECTORY, "fixtures", "codes"), 'r') as f:
        return f.read()


@pytest.fixture
def output():
    with open(os.path.join(TESTS_DIRECTORY, "fixtures", "out"), 'r') as f:
        return f.read()


@pytest.fixture
def BPE():
    return pyBPE
