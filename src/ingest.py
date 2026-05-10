"""
GDELT 2.0 ingest pipeline.

Pulls events from GDELT's 15-minute update feed, normalises into the
local schema, and persists to the DuckDB raw events store.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import requests

logger = logging.getLogger(__name__)

GDELT_BASE_URL = "http://data.gdeltproject.org/gdeltv2"
LOCAL_DB_PATH = Path("data/events.duckdb")


@dataclass
class GDELTEvent:
    """A single GDELT 2.0 event row, post-normalisation."""

    event_id: str
    timestamp: datetime
    actor1_country: str | None
    actor2_country: str | None
    event_code: str
    goldstein_scale: float | None
    avg_tone: float | None
    source_url: str
    geo_lat: float | None
    geo_lon: float | None
    geo_country: str | None


class GDELTIngest:
    """Pulls and normalises GDELT 2.0 event data."""

    def __init__(self, db_path: Path = LOCAL_DB_PATH) -> None:
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create the events table if it does not exist."""
        with duckdb.connect(str(self.db_path)) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    event_id VARCHAR PRIMARY KEY,
                    timestamp TIMESTAMP,
                    actor1_country VARCHAR,
                    actor2_country VARCHAR,
                    event_code VARCHAR,
                    goldstein_scale DOUBLE,
                    avg_tone DOUBLE,
                    source_url VARCHAR,
                    geo_lat DOUBLE,
                    geo_lon DOUBLE,
                    geo_country VARCHAR
                )
                """
            )

    def pull_window(self, hours: int = 24) -> list[GDELTEvent]:
        """Pull all GDELT events from the last `hours` hours."""
        # TODO: enumerate 15-minute windows, fetch CSVs, parse into GDELTEvent
        raise NotImplementedError("Ingest window enumeration in progress")

    def persist(self, events: list[GDELTEvent]) -> int:
        """Persist events to DuckDB. Returns the count inserted."""
        # TODO: bulk insert with conflict handling on event_id
        raise NotImplementedError("Bulk insert in progress")


def main(window_hours: int = 24) -> None:
    """CLI entry point: pull, normalise, persist."""
    logging.basicConfig(level=logging.INFO)
    ingest = GDELTIngest()
    events = ingest.pull_window(window_hours)
    n = ingest.persist(events)
    logger.info("Persisted %d events from the last %d hours", n, window_hours)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=str, default="24h")
    args = parser.parse_args()
    hours = int(args.window.rstrip("h"))
    main(hours)