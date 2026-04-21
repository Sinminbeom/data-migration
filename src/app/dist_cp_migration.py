from src.app.migration import abMigration
from src.config.project_config import ProjectConfig
from src.job.dist_cp_migration_job import DistCpMigrationJob


class DistCpMigration(abMigration):
    def __init__(self):
        super().__init__()

    def make_jobs(self) -> None:
        file_list = self.get_file_list()

        self.make_project_meta_json(file_list)

        for file in file_list:
            file_name = file.get_file_name()
            src_path = file.get_file_path()

            if self.is_file_check(file):
                continue

            dst_root_path = ProjectConfig.instance().dst_root_path

            project_name = self.get_project_name(file)

            instrument_type = self.meta_json_dict[project_name].instrument_type
            production_datetime = self.meta_json_dict[project_name].production_datetime
            production_timestamp = self.to_compact_timestamp(production_datetime)

            dst_path = (
                f"{dst_root_path}{instrument_type}/{production_timestamp}/{file_name}"
            )

            if self.src_storage is None or self.dst_storage is None:
                raise RuntimeError("storage is None")

            self.job_queue.append(
                DistCpMigrationJob(self.src_storage, src_path, dst_path)
            )
