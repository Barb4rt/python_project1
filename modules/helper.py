import os


class Helper:
    @staticmethod
    def create_directory(name, path):
        """static method to create a folder

        Args:
            name (string): How named the file
            path (string): Where sacve the file

        Returns:
            string: The path where the file is save
        """
        print(f"Création du dossier {name}...")
        try:
            separation = "\\" if "\\" in path else "/"
            fullpath = path + name
            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
                print(f"Le dossier {name} crée 🟢🟢🟢")
            else:
                print(f"Le dossier {name} existe déja 🟢🟢🟢")
        except Exception:
            print(f"{Exception} 🔴 🔴 🔴")
        return fullpath + separation
