from dataclasses import dataclass


@dataclass
class DataFile:
    s3uri: str
    checksum_sha256: str
