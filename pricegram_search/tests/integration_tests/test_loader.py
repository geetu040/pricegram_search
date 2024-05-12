from __future__ import annotations

import os
import shutil

from pricegram_search.loader import Initializer


def test_initializer():
    initializer = Initializer()
    initializer.dump_path = "dummy_dump_path"
    initializer.init(skip_init=False, verbose=False)

    assert os.path.exists("dummy_dump_path")

    # Cleaning up
    shutil.rmtree("dummy_dump_path")
