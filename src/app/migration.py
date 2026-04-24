import time
from abc import abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
import json

from python_library.job.job import IJob
from python_library.logger.app_logger import AppLogger
from python_library.storage.s3.s3_storage_factory import S3StorageFactory
from python_library.storage.s3.s3_storage_info_factory import S3StorageInfoFactory
from python_library.storage.storage import IStorage
from python_library.storage.storage_file import StorageFile
from python_library.thread.multi_thread_manager import MultiThreadManager
from python_library.thread.queue_thread import QueueThreading

from src.config.project_config import ProjectConfig
from meta_data.meta_json import MetaJson


class WorkThread(QueueThreading):
    def action(self) -> None:
        time.sleep(0.001)
        job: IJob | None = self.pop_shared_job_queue()
        if job is None:
            return
        job.execute()


class MigrationManager(MultiThreadManager):
    def action(self) -> None:
        pass


class abMigration:
    PROJECT_DEPTH = 4
    UPLOAD_FILE_NAME = "meta.json"
    UPLOAD_EXTENSIONS = [".raw"]

    def __init__(self) -> None:
        super().__init__()

        self.src_storage: Optional[IStorage] = None
        self.dst_storage: Optional[IStorage] = None

        self.multi_thread_manager = MigrationManager()

        self.meta_json_dict: Dict[str, MetaJson] = dict()

        self._init_threads()
        self._init_storage()

    def _init_threads(self) -> None:
        thread_count = int(ProjectConfig.instance().thread_count)
        for _ in range(thread_count):
            self.multi_thread_manager.append(WorkThread())

    def _init_storage(self) -> None:
        src_storage_factory = S3StorageFactory(S3StorageInfoFactory())
        dst_storage_factory = S3StorageFactory(S3StorageInfoFactory())
        self.src_storage = src_storage_factory.create_storage()
        self.dst_storage = dst_storage_factory.create_storage()

        self.src_storage.connect()
        self.dst_storage.connect()

    def get_file_list(self) -> List[StorageFile]:
        src_root_path = ProjectConfig.instance().src_root_path

        if self.src_storage is None:
            raise RuntimeError("storage is not initialized")

        file_list = self.src_storage.get_file_list(src_root_path)
        return file_list

    def make_project_meta_json(self, file_list: List[StorageFile]) -> None:
        for file in file_list:
            if file.get_depth() == self.PROJECT_DEPTH:
                file_path = file.get_file_path()
                meta_json_path = f"{file_path}{abMigration.UPLOAD_FILE_NAME}"

                if self.src_storage is None:
                    raise RuntimeError("storage is not initialized")

                if not self.src_storage.is_exists(meta_json_path):
                    continue

                meta_json_text = self.src_storage.read(meta_json_path)
                meta_json_data = json.loads(meta_json_text)

                meta_json = MetaJson(**meta_json_data)

                self.meta_json_dict[file.get_file_name()] = meta_json

    def get_project_name(self, file: StorageFile) -> str:
        return file.get_file_path().split("/")[abMigration.PROJECT_DEPTH]

    def to_compact_timestamp(self, ts: str) -> str:
        if ts.endswith("Z"):
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%Y%m%dT%H%M%SZ")
        else:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
            return dt.strftime("%Y%m%dT%H%M%S")

    def is_file_check(self, file: StorageFile) -> bool:
        file_name = file.get_file_name()
        file_path = file.get_file_path()

        # TODO : TEST 코드
        if not any(
            keyword in file_path
            for keyword in [
                "TEST_PROJECT"
                # "AMC_KKK_TEST",
                # "biobigdata_TEST",
                # "faims_test_TEST"
            ]
        ):
            return True

        if file.is_dir():
            return True

        if (
            not any(ext in file_name for ext in self.UPLOAD_EXTENSIONS)
            and file_name != abMigration.UPLOAD_FILE_NAME
        ):
            return True

        project_name = self.get_project_name(file)
        if project_name not in self.meta_json_dict:
            AppLogger.instance().error(f"{project_name} : meta.json not found")
            return True

        return False

    @abstractmethod
    def make_jobs(self) -> None:
        pass

    def start(self):
        self.multi_thread_manager.start()
