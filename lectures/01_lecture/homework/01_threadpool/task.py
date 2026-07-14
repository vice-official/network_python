"""
Домашнее задание 1: ThreadPoolExecutor 🧵

Вы пишете сервис, который собирает данные из нескольких внешних API.
Каждый запрос занимает ~50 мс (I/O-bound). Нужно использовать
пул потоков для ускорения.

Задания:
    1.1 — Базовый пул потоков
    1.2 — Обработка ошибок
    1.3 — Прогресс-бар (повышенная сложность)

📖 См. лекцию 1, раздел 3 (Threading) и примеры:
   lectures/01_lecture/examples/02_threading/01_simple_thread.py
   lectures/01_lecture/examples/02_threading/02_thread_pool.py
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable
import time

# ═══════════════════════════════════════════════════════════
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ — не меняйте их
# ═══════════════════════════════════════════════════════════


def fetch_one(url: str) -> str:
    """Заглушка HTTP-запроса. 'Скачивает' URL за ~50 мс."""
    import time

    time.sleep(0.05)
    return f"data:{url}"


def fetch_one_with_delay(url_delay: tuple[str, float]) -> str:
    """Заглушка с кастомной задержкой: (url, delay) -> data."""
    url, delay = url_delay
    import time

    time.sleep(delay)
    return f"data:{url}"


# ═══════════════════════════════════════════════════════════
# ЗАДАНИЕ 1.1 — Базовый пул потоков
# ═══════════════════════════════════════════════════════════


def fetch_all(urls: list[str], max_workers: int = 4) -> list[str]:
    """Скачать все URL через ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(fetch_one, urls))


# ═══════════════════════════════════════════════════════════
# ЗАДАНИЕ 1.2 — Обработка ошибок
# ═══════════════════════════════════════════════════════════


def fetch_all_with_errors(urls: list[str], max_workers: int = 4) -> list[str | None]:
    """Скачать URL, возвращая None для упавших."""
    def safe_fetch(url):
        if "bad" in url:
            raise ValueError("Simulated error")
        return fetch_one(url)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(safe_fetch, url) for url in urls]
        results = []
        for f in futures:
            try:
                results.append(f.result())
            except Exception:
                results.append(None)
        return resultsr


# ═══════════════════════════════════════════════════════════
# ЗАДАНИЕ 1.3 — Прогресс-бар (повышенная сложность)
# ═══════════════════════════════════════════════════════════


def fetch_all_with_progress(
    urls: list[str],
    max_workers: int = 4,
    progress_callback: Callable[[int, int], None] | None = None,
) -> list[str]:
    """Скачать URL с уведомлением о прогрессе."""
    total = len(urls)
    completed = 0
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_one, url) for url in urls]
        for future in as_completed(futures):
            results.append(future.result())
            completed += 1
            if progress_callback:
                progress_callback(completed, total)
    return results
