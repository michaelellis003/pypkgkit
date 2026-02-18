"""Allow running pypkgkit as ``python -m pypkgkit``."""

import sys

from pypkgkit.cli import main

sys.exit(main())
