import os
import time
from shutil import copyfile
from .backup_report import BackupReport


# Copia sempre senza alcun controllo
RULE_ALWAYS = "always"
# Copia solo se in source è più recente (data modifica)
RULE_NEWER = "newer"
# Copia solo se non esiste
RULE_ONCE = "once"


def walk_folder(path, func):
    # dirs non non lo utilizo, ma se lo metto e non lo utilizzo, ho un errore. Uso i segnaposto '_'.
    for root, _, files in os.walk(path):
        for file in files:
            func(os.path.join(root, file))


class Backupper(object):
    def __init__(self, source_root, dest_root):
        self.source_root = os.path.abspath(source_root)
        self.dest_root = os.path.abspath(dest_root)

    def backup_file(self, file_path, dry_run):
        dest_file = self._build_dest_path(file_path)
        return dest_file

    def check_exists(self, file_path, dry_run):
        dest_file = self._build_dest_path(file_path)
        return dest_file

    def _build_dest_path(self, file_path):
        return os.path.join(self.dest_root, os.path.relpath(file_path, self.source_root))

    def backup(self, dry_run=False):
        
        # dirs non non lo utilizo, ma se lo metto e non lo utilizzo, ho un errore. Uso i segnaposto '_'.
        for root, _, files in os.walk(self.source_root):
            for file in files:
                self.backup_file(os.path.join(root, file), dry_run)

        for root, _, files in os.walk(self.dest_root):
            for file in files:
                self.check_exists(os.path.join(root, file), dry_run)


class CopyFile(Backupper):
    def __init__(self, source_root, dest_root, rules, report):
        super().__init__(source_root, dest_root)
        self.rules = rules
        self.report = report
        self.existing_files = set()

    def backup_file(self, file_path, dry_run):
        # Leggo la regola per il file:
        ext = os.path.splitext(file_path)[1]
        rule = self.rules.get(ext[1:].lower())

        if not rule:
            self.report.add_no_ruled_file(file_path)
            return

        # Ricavo percorso file destinazione
        dest_file_path = self._build_dest_path(file_path)
        exists = os.path.isfile(dest_file_path)

        if not exists:
            self.report.add_added_file(dest_file_path)
            pass

        elif rule == RULE_ALWAYS:
            self.report.add_updated_file(dest_file_path)
            pass

        elif rule == RULE_NEWER:
            newer = os.path.getmtime(file_path) > os.path.getmtime(dest_file_path)
            if newer:
                self.report.add_updated_file(dest_file_path)
                pass

        elif rule == RULE_ONCE:
            self.existing_files.add(dest_file_path)
            return

        else:
            assert False, "Rules error."

        # Eseguo la copia del file (o stampo info se dry_run):
        self.existing_files.add(dest_file_path)
        if dry_run:
            print("To copy {} -> {}".format(file_path, dest_file_path))
        else:
            self._copyfile(file_path, dest_file_path)

    def _copyfile(self, file_path, dest_file_path):
        print("coping {} to {}...".format(file_path, dest_file_path))
        # Verifica se la cartella esiste, se non esiste la crea.
        dest_folder = os.path.dirname(dest_file_path)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        # Copia il file
        copyfile(file_path, dest_file_path)

    def check_exists(self, file_path, dry_run):
        # Leggo la regola per il file:
        ext = os.path.splitext(file_path)[1]
        rule = self.rules.get(ext[1:].lower())

        if not rule:
            return

        if file_path not in self.existing_files:
            if dry_run:
                print("To delete {}".format(file_path))
            else:
                os.remove(file_path)
            self.report.add_deleted_file(file_path)

