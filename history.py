import os


class History(list):
    def __init__(self, file_name: str, read_count: int):
        super().__init__()
        self._file_name = file_name
        self._curr_pos = 0
        self._history_uploaded = 0
        self._read_history(read_count)
        self._translations = {}

    def upload_word_translations(self, word: str, dic: dict):
        if not word in self._translations:
            self._translations[word] = {}
        self._translations[word].update(dic)

    @property
    def current_word_translations(self) -> dict:
        if not self.current_word in self._translations:
            return None
        return self._translations[self.current_word]

    def save_history(self):
        if len(self) == 0 or len(self) == self._history_uploaded:
            return
        self._write_history()

    def append(self, obj: str) -> None:
        super().append(obj)
        self._curr_pos = len(self) - 1

    @property
    def current_word(self) -> str:
        if self._history_uploaded == 0 or self._history_uploaded == -1:
            return ''
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
        self._curr_pos = -1  # чтобы начинать с первого элемента

    def navigate_back(self):
        if self._curr_pos is -1:
            self._curr_pos = self._history_uploaded - 1
            return
        if self._curr_pos <= 0:
            self._curr_pos = 0
            return
        self._curr_pos -= 1

    def navigate_forward(self):
        if self._curr_pos >= (len(self) - 1):
            self._curr_pos = len(self) - 1
            return
        self._curr_pos += 1
