from typing import List

from src.app.migration import abMigration
from src.config.project_config import ProjectConfig


class RoundRobinMigration(abMigration):
    def __init__(self):
        super().__init__()

        self.disks: List[str] = ProjectConfig.instance().volumes_place_holder
        self.diskSelectIndex: int = 0

    def get_disk_name(self) -> str:
        self.diskSelectIndex += 1

        if self.diskSelectIndex == len(self.disks):
            self.diskSelectIndex = 0

        return self.disks[self.diskSelectIndex]
