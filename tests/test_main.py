import pytest

from src.main import foo


def test_gemstome_case():
    assert foo() == 1
