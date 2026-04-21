from typing import List

from python_library.configure.app_config import AppConfig
from python_library.define.enum import IENUM


class ProjectConfig(AppConfig):
    class E_CATE_TYPE(IENUM):
        COMMON = "COOMON"
        S3 = "S3"

    class E_CATE_ELE_COMMON(IENUM):
        PROJECT_NAME = "ProjectName"
        THREAD_COUNT = "ThreadCount"
        LOCAL_DOWNLOAD_PATH = "LocalDownloadPath"
        LOCAL_SEPARATOR = "LocalSeparator"
        VOLUMES_PLACE_HOLDER = "VolumesPlaceHolder"
        pass

    class E_CATE_ELE_S3(IENUM):
        SRC_ROOT_PATH = "SrcRootPath"
        DST_ROOT_PATH = "DstRootPath"

    def __init__(self):
        super().__init__()

        self.project_name = self.get_config(
            ProjectConfig.E_CATE_TYPE.COMMON,
            ProjectConfig.E_CATE_ELE_COMMON.PROJECT_NAME,
        )
        self.thread_count: str = self.get_config(
            ProjectConfig.E_CATE_TYPE.COMMON,
            ProjectConfig.E_CATE_ELE_COMMON.THREAD_COUNT,
        )
        self.local_download_path = self.get_config(
            ProjectConfig.E_CATE_TYPE.COMMON,
            ProjectConfig.E_CATE_ELE_COMMON.LOCAL_DOWNLOAD_PATH,
        )
        self.local_separator = self.get_config(
            ProjectConfig.E_CATE_TYPE.COMMON,
            ProjectConfig.E_CATE_ELE_COMMON.LOCAL_SEPARATOR,
        )
        self.volumes_place_holder: List[str] = self.get_config(
            ProjectConfig.E_CATE_TYPE.COMMON,
            ProjectConfig.E_CATE_ELE_COMMON.VOLUMES_PLACE_HOLDER,
        )

        self.src_root_path: str = self.get_config(
            ProjectConfig.E_CATE_TYPE.S3, ProjectConfig.E_CATE_ELE_S3.SRC_ROOT_PATH
        )
        self.dst_root_path = self.get_config(
            ProjectConfig.E_CATE_TYPE.S3, ProjectConfig.E_CATE_ELE_S3.DST_ROOT_PATH
        )
