"""Command-line interface to launch the BI dashboard."""

import sys
from pathlib import Path
import streamlit.web.cli as stcli


def main() -> None:
    """Launch the Streamlit Business Intelligence dashboard."""
    app_path = Path(__file__).resolve().parent / "dashboard" / "app.py"
    
    # Forward the script path and any user arguments to the Streamlit CLI
    sys.argv = ["streamlit", "run", str(app_path)] + sys.argv[1:]
    
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
