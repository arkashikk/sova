"""
Замер скорости: умножение матриц на процессоре и на видеокарте.

Запуск из корня проекта:  python -m sova.bench_matmul
"""

import time

import torch

N = 4096
REPEATS = 10


def matmul_tflops(n: int, seconds: float):
    """Скорость в TFLOPS: умножение n×n на n×n — это 2·n³ операций."""
    if n <= 0 or seconds <= 0:
        raise ValueError("n и seconds должны быть положительными")
    return 2 * n**3 / seconds / 1e12


def time_matmul(device: str, dtype: torch.dtype, n: int = N, repeats: int = REPEATS) -> float:
    """Возвращает среднее время одного умножения N×N на N×N в секундах."""
    a = torch.randn(n, n, device=device, dtype=dtype)
    b = torch.randn(n, n, device=device, dtype=dtype)
    a @ b # прогрев
    if device == 'cuda':
        torch.cuda.synchronize() # дождаться пока видеокарта закончит прогрев
    start = time.perf_counter()
    for _ in range(repeats):
        a @ b
    if device == 'cuda':
        torch.cuda.synchronize()
    return (time.perf_counter() - start) / repeats


def check_same_result() -> float:
    """Одно и то же умножение на CPU и GPU: насколько расходятся ответы."""
    torch.manual_seed(0)
    a = torch.randn(512, 512)
    b = torch.randn(512, 512)
    on_cpu = a @ b
    on_gpu = (a.to("cuda") @ b.to("cuda")).cpu()
    return (on_cpu - on_gpu).abs().max().item()


def main() -> None:
    flop = 2 * N**3
    print(f"Умножение матриц {N}×{N}: {flop / 1e9:.0f} млрд операций за раз")
    cases = [("cpu", torch.float32)]
    if torch.cuda.is_available():
        print(f"Видеокарта: {torch.cuda.get_device_name(0)}")
        cases += [("cuda", torch.float32), ("cuda", torch.float16), ("cuda", torch.bfloat16)]
    else:
        print("CUDA недоступна: меряем только процессор")

    print(f"{'устройство':<11}{'тип':<16}{'время, мс':>10}{'TFLOPS':>9}")
    base = None
    for device, dtype in cases:
        seconds = time_matmul(device, dtype)
        base = base or seconds
        tflops = matmul_tflops(N, seconds)
        print(f"{device:<11}{str(dtype):<16}{seconds * 1000:>10.1f}{tflops:>9.2f}"
              f"   ×{base / seconds:.0f} к CPU")

    if torch.cuda.is_available():
        print(f"Расхождение CPU и GPU на 512×512: {check_same_result():.2e}")


if __name__ == "__main__":
    main()