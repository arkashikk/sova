"""
Тесты замера скорости: формула TFLOPS и работа time.matmul.
"""

import pytest

torch = pytest.importorskip("torch")

from sova.bench_matmul import matmul_tflops, time_matmul


def test_tflops_known_value():
    assert matmul_tflops(1000, 1.0) == pytest.approx(0.002)


@pytest.mark.parametrize("n, seconds", [(0, 1.0), (-5, 1.0), (100, 0.0)])
def test_tflops_rejects_bad_input(n, seconds):
    with pytest.raises(ValueError):
        matmul_tflops(n, seconds)


def test_time_matmul_small_on_cpu():
    seconds = time_matmul("cpu", torch.float32, n=64, repeats=2)
    assert 0 < seconds < 1