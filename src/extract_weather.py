import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

CITIES = {
    "cincinnati": (39.1031, -84.5120),
    "new_york": (40.7128, -74.0060),
    "seattle": (47.6062, -122.3321),
}

def fetch_city(city: str, latitude: float, longitude: float) -> dict:
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": latitude, "longitude": longitude, "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum", "timezone": "UTC"},
        timeout=30,
    )
    response.raise_for_status()
    return {"city": city, "ingested_at": datetime.now(timezone.utc).isoformat(), "source": "open-meteo", "payload": response.json()}

def write_record(record: dict, output: Path) -> Path:
    date = record["ingested_at"][:10]
    target = output / f"ingestion_date={date}" / f"{record['city']}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2))
    return target

def main(output: Path) -> None:
    for city, coordinates in CITIES.items():
        print(write_record(fetch_city(city, *coordinates), output))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    main(args.output)
