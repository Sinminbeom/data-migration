from dataclasses import dataclass


@dataclass
class Extra:
    plate_position: str
    extraction_batch: str
    temperature_celsius: float
    internal_standard_used: str
    preprocessing_version: str
