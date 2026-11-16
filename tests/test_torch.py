"""
Тесты PyTorch: умножение матриц верно на CPU и совпадает на GPU.
"""

import pytest

# Если PyTorch не установлен, тесты этого файла пропускаются, а не падают.
torch = pytest.importorskip("torch")


def test_matmul_on_cpu():
    # Пример, который легко проверить руками: [1 2; 3 4] · [5; 6] = [17; 39]
    a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    b = torch.tensor([[5.0], [6.0]])
    assert torch.equal(a @ b, torch.tensor([[17.0], [39.0]]))


@pytest.mark.skipif(not torch.cuda.is_available(), reason="нет видеокарты с CUDA")
def test_gpu_matches_cpu():
    torch.manual_seed(0)
    a = torch.randn(256, 256)
    b = torch.randn(256, 256)
    on_gpu = (a.to("cuda") @ b.to("cuda")).to("cpu")
    # Порядок сложений на GPU другой, поэтому сравниваем с допуском, а не на равенство.
    assert torch.allclose(a @ b, on_gpu, atol=1e-3)