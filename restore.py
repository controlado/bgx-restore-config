import os
import shutil
from datetime import datetime


class BGX:

    base_files = ["application", "core", "plugins"]
    backup_dir = "backup/settings_modern.dat"
    roaming_dir = os.getenv("APPDATA")
    roaming_content = os.listdir(roaming_dir)

    def __init__(self):
        response = self.start()
        print(response)  # console output.

    def start(self) -> str:
        if not self.__check_settings():
            return "Add your BGX configuration to the backup folder in this directory."

        bgx_folder = self.__get_bgx_folder()

        if bgx_folder["error"]:
            # if no matching folder was found.
            return bgx_folder["message"]

        if not self.__check_bgx_dir(bgx_folder["path"]):
            return "One of the essential folders are not in the BGX directory."

        try:
            shutil.copy(self.backup_dir, bgx_folder["path"])
        except Exception as error:
            return f"Something wrong happened ({error})"
        else:
            return "The backup file has been moved successfully."

    def __get_bgx_folder(self) -> dict:
        possible_folders = [
            folder
            for folder in self.roaming_content
            if len(folder) == 32
        ]

        if not possible_folders:
            return {
                "path": None,
                "error": True,
                "message": "Reinstall BGX."
            }

        if len(possible_folders) == 1:
            return {  # dir: C:\Users\User\AppData\Roaming\BGX
                "path": f"{self.roaming_dir}/{possible_folders[0]}",
                "error": False,
                "message": "Success."
            }

        return {  # if there is another folder with 32 characters.
            "path": self.__get_correct_folder_path(possible_folders),
            "error": False,
            "message": "Success."
        }

    def __get_correct_folder_path(self, possible_folders: list) -> str:
        objects = {}

        for folder in possible_folders:
            path = f"{self.roaming_dir}/{folder}"
            creation_timestamp = os.stat(path).st_mtime
            date_object = datetime.fromtimestamp(creation_timestamp)
            objects[date_object] = path

        latest_edited = max(objects.keys())
        return objects.get(latest_edited)

    def __check_settings(self) -> bool:
        return os.path.exists(self.backup_dir)

    def __check_bgx_dir(self, bgx_folder: str) -> bool:
        return all(folder in os.listdir(bgx_folder) for folder in self.base_files)


if __name__ == "__main__":
    bgx = BGX()
    input(":)")
