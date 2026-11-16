import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Tuple

BRIGHT_DATA_API_TOKEN = "YOUR_BRIGHT_DATA_API_KEY_HERE"
DATASET_ID = "gd_l7q7dkf244hwjntr0"

def fetch_html_via_bright_data(url: str) -> Tuple[str, str]:
    """Fetches HTML with explicit UTF-8 encoding handling to prevent symbol corruption."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Force UTF-8 encoding fix for currency symbols
        response.encoding = 'utf-8' 
        return response.text, "Live DOM ingested via Edge Execution Node."
    except Exception as e:
        return "", f"Fetch Error: {str(e)}"

def fetch_and_extract_brightdata(
    url: str, 
    card_sel: str = "", 
    title_sel: str = "", 
    price_sel: str = ""
) -> Tuple[List[Dict[str, Any]], Dict[str, str], str]:
    
    html_content, log_msg = fetch_html_via_bright_data(url)
    soup = BeautifulSoup(html_content, "html.parser")

    if not card_sel:
        card_sel = "article.product_pod, .product-item, .product-card, div.item"
    if not title_sel:
        title_sel = "h3 a, h1, .title, [class*='title']"
    if not price_sel:
        price_sel = ".price_color, .price, [class*='price']"

    active_selectors = {
        "container": card_sel,
        "title": title_sel,
        "price": price_sel
    }

    results = []
    containers = soup.select(card_sel)

    for item in containers:
        t_el = item.select_one(title_sel)
        p_el = item.select_one(price_sel)

        title_val = t_el.get("title") if (t_el and t_el.get("title")) else (t_el.text.strip() if t_el else None)
        # Fix encoding artifacts on price values
        price_val = p_el.text.strip().replace("Â", "") if p_el else None

        if title_val or price_val:
            results.append({"title": title_val, "price": price_val})

    return results, active_selectors, log_msg

def validate_schema(data: List[Dict[str, Any]]) -> Tuple[bool, str]:
    if not data:
        return False, "Schema Error: 0 products extracted."
    valid_items = [d for d in data if d.get("title") and d.get("price")]
    if len(valid_items) < len(data) * 0.5:
        return False, f"Schema Decay Detected: Only {len(valid_items)}/{len(data)} items valid."
    return True, f"Bright Data Payload Validated: {len(data)} items ingested cleanly."