from datetime import datetime

def parse_date(s):
    """Converte string AAAA-MM-DD para datetime."""
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None

def format_currency(v):
    """Formata valores para R$."""
    return f"R${v:,.2f}" if isinstance(v, (int, float)) else v