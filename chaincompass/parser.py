from typing import Any


def parse_quote(quote_data: dict[str, Any]) -> dict[str, float | str | int]:
    """
    Extracts a compact summary from a LI.FI quote response.

    Returns a dictionary containing provider name, execution time in seconds,
    total fees in USD, and the estimated received amount in USD.
    """
    estimate = quote_data.get("estimate", {})
    tool_details = quote_data.get("toolDetails", {})

    provider_name = tool_details.get("name", "N/A")
    execution_time_seconds = int(estimate.get("executionDuration", 0) or 0)
    final_output_usd_raw = estimate.get("toAmountUSD", "0")

    total_fees_usd = 0.0
    for fee in estimate.get("feeCosts", []) or []:
        try:
            total_fees_usd += float(fee.get("amountUSD", "0") or 0)
        except (TypeError, ValueError):
            continue

    try:
        final_output_usd = float(final_output_usd_raw or 0)
    except (TypeError, ValueError):
        final_output_usd = 0.0

    return {
        "provider": provider_name,
        "time_seconds": execution_time_seconds,
        "fees_usd": total_fees_usd,
        "output_usd": final_output_usd,
    }

