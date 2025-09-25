import json
from pathlib import Path

from chaincompass import parse_quote


def test_parse_quote_sample_response():
    sample_path = Path(__file__).resolve().parents[1] / "sample_response.json"
    data = json.loads(sample_path.read_text())

    summary = parse_quote(data)

    assert summary["provider"] == "AcrossV4"
    assert isinstance(summary["time_seconds"], int)
    assert summary["time_seconds"] == 48
    assert abs(summary["fees_usd"] - (0.25 + 0.0098 + 0.0116 + 0.0048)) < 1e-6
    assert abs(summary["output_usd"] - 99.0625) < 1e-6

