from archivecloner.backupper import BackupReport, CopyFile, RULE_ONCE, RULE_NEWER
from archivecloner.backup_report import BackupReport
import json
import os


rules = {'nef': RULE_ONCE, 
             'jpeg': RULE_NEWER, 
             'jpg': RULE_NEWER, 
             'png': RULE_NEWER,
             'lrcat': RULE_NEWER,
             'tiff': RULE_NEWER}

def test_backup_folders_couple():
    report = BackupReport()
    report.start()

    dirname = os.path.dirname(__file__)
    source_root = os.path.join(dirname, 'resources/backup/source')
    dest_root = os.path.join(dirname, 'resources/backup/dest')

    #bkp = CopyFile("/Users/rossellabozzini/Dev/archivecloner/tests/resources/backup/source",
 #                  "/Users/rossellabozzini/Dev/archivecloner/tests/resources/backup/Dest", rules, report)

    bkp = CopyFile(source_root, dest_root, rules, report)

    bkp.backup(True)
    report.end()

    rep_json = report.to_json()
    rep_data = json.loads(rep_json)
    backup_info_data = rep_data.get("backup_info")
    assert isinstance(backup_info_data, dict)
    assert len(backup_info_data) == 4

    added_files_data = backup_info_data.get("added_files")
    assert isinstance(added_files_data, list)
    assert len(added_files_data) == 2
    assert added_files_data[0].endswith("backup/dest/subfolder-renamed/immagine7.NEF")
    assert added_files_data[1].endswith("backup/dest/subfolder-renamed/immagine6.tiff")

    deleted_files_data = backup_info_data.get("deleted_files")
    assert isinstance(deleted_files_data, list)
    assert len(deleted_files_data) == 2
    assert deleted_files_data[0].endswith("backup/dest/subfolder2/immagine7.NEF")
    assert deleted_files_data[1].endswith("backup/dest/subfolder2/immagine6.tiff")

    no_ruled_files_data = backup_info_data.get("no_ruled_files")
    assert isinstance(no_ruled_files_data, list)
    assert len(no_ruled_files_data) == 1
    assert no_ruled_files_data[0].endswith("resources/backup/source/.DS_Store")

    updated_files_data = backup_info_data.get("updated_files")
    assert isinstance(updated_files_data, list)
    assert len(updated_files_data) == 1
    assert updated_files_data[0].endswith("resources/backup/dest/immagine1.jpeg")
        