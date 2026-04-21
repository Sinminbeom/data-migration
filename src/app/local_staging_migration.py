from python_library.storage.storage_file import StorageFile

from src.app.round_robin_migration import RoundRobinMigration
from src.config.project_config import ProjectConfig
from src.job.local_staging_migration_job import LocalStagingMigrationJob


class LocalStagingMigration(RoundRobinMigration):
    def __init__(self):
        super().__init__()

    def make_jobs(self):
        file_list = self.get_file_list()

        self.make_project_meta_json(file_list)

        for file in file_list:
            file_name = file.get_file_name()
            file_path = file.get_file_path()

            if self.is_file_check(file):
                continue

            project_name = self.get_project_name(file)

            dst_root_path = ProjectConfig.instance().dst_root_path

            instrument_type = self.meta_json_dict[project_name].instrument_type

            production_datetime = self.meta_json_dict[project_name].production_datetime
            production_timestamp = self.to_compact_timestamp(production_datetime)

            local_path = self.get_local_path(
                file, instrument_type, production_timestamp
            )

            dst_path = (
                f"{dst_root_path}{instrument_type}/{production_timestamp}/{file_name}"
            )

            if self.src_storage is None or self.dst_storage is None:
                raise RuntimeError("storage is not initialized")

            self.job_queue.append(
                LocalStagingMigrationJob(
                    self.src_storage, file_path, local_path, self.dst_storage, dst_path
                )
            )

    def get_local_path(
        self, file: StorageFile, instrument_type: str, production_datetime: str
    ) -> str:
        file_name = file.get_file_name()
        disk_name = self.get_disk_name()

        local_download_path = ProjectConfig.instance().local_download_path
        local_separator = ProjectConfig.instance().local_separator

        local_path = f"{local_download_path}{disk_name}{local_separator}{instrument_type}{local_separator}{production_datetime}{local_separator}{file_name}"
        return local_path
