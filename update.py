from pathlib import Path
from typing import Any, List
from urllib.request import urlopen, HTTPError, URLError


class FileReader:
    @staticmethod
    def readFile(filename: str) -> List[str]:
        with open(filename) as file:
            return set(file.readlines())

class FileWriter:
    @staticmethod
    def write(filename: str, text: str, mode: str = 'w+') -> None:
        with open(filename, mode=mode) as file:
            file.write(text)

    @staticmethod
    def writelines(filename: str, text: Any, mode: str = 'w+') -> None:
        with open(filename, mode=mode) as file:
            file.writelines(text)

    @staticmethod
    def create_empty_file(filename: str) -> None:
        with open(filename, 'w+'):
            pass


class BlocklistUpdater:
    def __init__(self, reader: FileReader = FileReader(), writer: FileWriter = FileWriter()):
        self.bad_url_found = False
        self.reader = reader
        self.writer = writer
        self.adlists = "adlists.list"
        self.hostlist = set()

    def update(self, filename: str) -> None:
        self.writer.create_empty_file(self.adlists)
        blocklist = self.reader.readFile(filename)
        print(f"Original size: {len(blocklist)}")

        blocklist = self._request_data(blocklist)
        print(f"New size: {len(blocklist)}")
        self.writer.writelines(filename, blocklist)

    def _request_data(self, blocklist: List[str]) -> List[str]:
        for url in blocklist.copy():
            try:
                self._append_to_adlists(url)
            except HTTPError:
                print(f"Error at {url}\n")
                self.bad_url_found = True
                blocklist.remove(url)
            except URLError:
                print(f"Connection refused by {url}\n")
                self.bad_url_found = True
                blocklist.remove(url)
        return blocklist

    def _append_to_adlists(self, url: str) -> None:
        with urlopen(url) as response:
            self.writer.write(
                self.adlists,
                str(response.read().decode("utf-8")),
                'a+'
            )

if __name__ == '__main__':
    BlocklistUpdater().update("blocklist.txt")