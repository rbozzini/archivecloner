import json
from datetime import datetime


class BackupReport(object):

    def __init__(self):
        self.added_files = []
        self.updated_files = []
        self.deleted_files = []
        self.no_ruled_files = []
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = datetime.now()

    def end(self):
        self.end_time = datetime.now()

    def add_added_file(self, file):
        self.added_files.append(file)

    def add_updated_file(self, file):
        self.updated_files.append(file)

    def add_deleted_file(self, file):
        self.deleted_files.append(file)

    def add_no_ruled_file(self, file):
        self.no_ruled_files.append(file)

    def to_json(self):
        report = {}

        # duration
        if self.start_time is not None and self.end_time is not None:
            report['start_date'] = self.start_time
            report['end_date'] = self.end_time
            report['duration'] = self._get_duration()

        # Backup_info
        backup_info = {}
        backup_info['added_files'] = self.added_files
        backup_info['updated_files'] = self.updated_files
        backup_info['deleted_files'] = self.deleted_files
        backup_info['no_ruled_files'] = self.no_ruled_files
        report['backup_info'] = backup_info
        
        return json.dumps(report, indent=4, sort_keys=True, default=str)

    def _get_duration(self):
        diff = self.end_time - self.start_time

        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)

if __name__ == "__main__":
    report = BackupReport()
    report.add_added_file("added_file_1")
    report.add_added_file("added_file_2")
    report.add_added_file("added_file_3")
    report.add_updated_file("updated_file_1")
    report.add_updated_file("updated_file_2")
    report.add_deleted_file("deleted_file_1")
    report.add_no_ruled_file("no_ruled_file_1")
    report.add_no_ruled_file("no_ruled_file_1")
    print(report.to_json())
