from dataclasses import dataclass
from typing import List, Optional

from meta_data.data_file import DataFile
from meta_data.extra import Extra


@dataclass
class MetaJson:
    schema_version: str
    metadata_version: int

    production_datetime: str

    client_institute: str
    client_name: str

    sample_name: str
    sample_type: str
    sample_disease: str

    instrument_type: str
    instrument_name: str
    instrument_mode: str
    instrument_operator: List[str]

    data_files: List[DataFile]
    notes: str
    extra: Optional[Extra] = None

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)
