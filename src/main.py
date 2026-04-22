from python_library.logger.app_logger import AppLogger

from src.app.dist_cp_migration import DistCpMigration
from src.config.project_config import ProjectConfig


def main():
    ProjectConfig.set_config("./conf/application.conf")
    AppLogger.set_config("./conf/logging.conf", ProjectConfig.instance().project_name)

    dist_cp_migration = DistCpMigration()
    dist_cp_migration.make_jobs()
    dist_cp_migration.start()

    # local_staging_migration = LocalStagingMigration()
    # local_staging_migration.make_jobs()
    # local_staging_migration.start()


if __name__ == "__main__":
    main()
