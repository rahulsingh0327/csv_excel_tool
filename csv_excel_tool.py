from server import mcp
import os
from typing import Any, Dict, List
import pandas as pd


def csv_preview(path: str, n: int = 5) -> List[Dict[str, Any]]:
    """
    Return the first `n` rows of a CSV/XLSX file as list of dicts.

    Args:
        path: Path to csv or xlsx file.
        n: Number of lines/rows to preview.

    Returns:
        List of row dictionaries (string keys to Python values).

    Raises:
        RuntimeError if pandas is not installed or file can't be read.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xls", ".xlsx"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    return df.head(n).to_dict(orient="records")


@mcp.tool()
def csv_excel_tool(action: str, path: str, n: int = 5) -> Dict[str, Any]:
    """
    CSV / Excel helper supporting 'preview' and 'stats'.

    Args:
        action: "preview" or "stats".
        path: Local file path.
        n: Number of rows to preview.

    Returns:
        preview -> rows; stats -> column and row counts.

    Notes:
        Uses pandas; supports CSV and XLSX.
    """
    action = action.lower()
    if action == "preview":
        return {"preview": csv_preview(path, n)}
    if action == "stats":
        ext = os.path.splitext(path)[1].lower()
        df = pd.read_excel(path) if ext in (".xls", ".xlsx") else pd.read_csv(path)
        return {"rows": int(df.shape[0]), "columns": int(df.shape[1]), "columns_list": list(df.columns)}
    raise ValueError("Unsupported action. Use preview/stats.")

