from pathlib import Path
from src.extract_weather import write_record

def test_partitioned_output(tmp_path: Path):
    record = {"city": "cincinnati", "ingested_at": "2026-08-12T10:00:00+00:00", "source": "test", "payload": {}}
    target = write_record(record, tmp_path)
    assert target == tmp_path / "ingestion_date=2026-08-12" / "cincinnati.json"
    assert target.exists()
