from django.core.files.storage import FileSystemStorage
import os
import shutil


class StorageSizeLimitExceeded(Exception):
    pass


class LimitedStorage(FileSystemStorage):
    def get_media_directory_size(self):
        total_size = 0
        for path, _, filenames in os.walk(self.location):
            for filename in filenames:
                filepath = os.path.join(path, filename)
                total_size += os.path.getsize(filepath)
        return total_size


    def _save(self, name, content):
        max_size_bytes = 700 * 1024 * 1024  # 500 MB
        current_size_bytes = self.get_media_directory_size()

        if current_size_bytes + content.size > max_size_bytes:
            raise StorageSizeLimitExceeded("Storage space limit reached. Cannot upload more files.")

        return super()._save(name, content)
