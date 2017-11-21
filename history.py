import os


class History(list):
    def __init__(self, file_name: str, read_count: int):
        super().__init__()
        self._file_name = file_name
        self._curr_pos = 0
        self._history_uploaded = 0
        self._read_history(read_count)

    # submit upload unload
    def upload_history(self):
        if len(self) == 0 or len(self) == self._history_uploaded:
            return
        self._write_history()

    def append(self, obj: str) -> None:
        super().append(obj)
        self._curr_pos = len(self)  # делаем на 1 больше, чтобы при навигации не было скачка на -2


    @property
    def current_word(self) -> str:
        return self[self._curr_pos]

    def _write_history(self):
        is_new = True
        if os.path.exists(self._file_name):
            is_new = False
        with open(self._file_name, 'a') as f:
            if not is_new:
                f.write('\n')
            f.write('\n'.join(self[self._history_uploaded:]))

    def _read_history(self, n: int) -> None:
        if not os.path.exists(self._file_name):
            return
        with open(self._file_name, "r") as f:
            lines_list = list(map(str.strip, f.readlines()[-n:]))

        self.extend(lines_list)
        self._history_uploaded = len(lines_list)
        self._curr_pos = len(self) # делаем на 1 больше

    def navigate_back(self) -> str:
        if self._curr_pos <= 0:
            self._curr_pos = 0
            return self[0]
        self._curr_pos -= 1
        return self[self._curr_pos]

    def navigate_forward(self) -> str:
        if self._curr_pos >= (len(self) - 1):
            self._curr_pos = len(self) - 1
            return self[len(self) - 1]
        self._curr_pos += 1
        return self[self._curr_pos]
