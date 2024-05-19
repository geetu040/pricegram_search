from __future__ import annotations

import argparse
import threading
import time

from pricegram_search import SearchEngine


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=10,
        help="Number of threads (default: 10)",
    )
    return parser.parse_args()


def data_fetcher(ids):
    # Simulate data fetching
    return [{"id": id_, "name": f"Product {id_}"} for id_ in ids]


def perform_search(engine):
    keywords = ["core i5", "16gb RAM", "512GB SSD"]
    engine.search(keywords=keywords, cluster_size=10, k=30)


def start_load_test(num_threads):
    print("\n>>> Setting Up")
    engine = SearchEngine(
        data_fetcher=data_fetcher, dump_path="./utils", verbose=False
    )

    print(">>> Starting Threads")
    start_time = time.time()
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=perform_search, args=(engine,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    time_to_execute = round(end_time - start_time, 3)

    print(">>> Results")
    print(
        f"{num_threads} threads executed concurrently in "
        f"{time_to_execute} seconds\n"
    )


if __name__ == "__main__":
    args = parse_args()
    start_load_test(args.threads)
