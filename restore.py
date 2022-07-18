import os

from shutil import copy as shutil_copy
from datetime import datetime


class BGX:

    base_files = ["application", "core", "plugins"]  # files that you always have in bgx directory.

    config_name = "settings_modern.dat"
    config_dir = f"backup/{config_name}"
    old_config_dir = f"backup/old_{config_name}"

    roaming_dir = os.getenv("APPDATA")
    roaming_content = os.listdir(roaming_dir)

    def __init__(self):
        response = self.start()
        print(response)  # console output.

    def start(self) -> str:
        if not self.__check_settings():
            # if the configuration to be installed was not found.
            return "Add your BGX configuration to the backup folder in this directory."

        bgx_folder = self.__get_bgx_folder()

        if bgx_folder["error"]:
            # if no matching folder was found.
            return bgx_folder["message"]

        if not self.__check_bgx_dir(bgx_folder["path"]):
            # just a warning, that some essential bgx folder has not been identified.
            print("One of the essential folders are not in the BGX directory.")

        bgx_folder = bgx_folder["path"]
        config_to_backup = f"{bgx_folder}/{self.config_name}"

        try:
            shutil_copy(config_to_backup, self.old_config_dir)
        except FileNotFoundError:
            # if an old configuration was not found.
            return "Your new settings have been installed."
        else:
            return "Your new settings have been installed and the old ones have been saved."
        finally:
            shutil_copy(self.config_dir, bgx_folder)

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
        # basically, this function takes the folder that was most recently edited.

        objects = {}

        for folder in possible_folders:
            path = f"{self.roaming_dir}/{folder}"
            creation_timestamp = os.stat(path).st_mtime
            date_object = datetime.fromtimestamp(creation_timestamp)
            objects[date_object] = path

        latest_edited = max(objects.keys())
        return objects.get(latest_edited)

    def __check_settings(self) -> bool:
        return os.path.exists(self.config_dir)

    def __check_bgx_dir(self, bgx_folder: str) -> bool:
        return all(folder in os.listdir(bgx_folder) for folder in self.base_files)


if __name__ == "__main__":
    bgx = BGX()
    input(":)")
