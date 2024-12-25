from tqdm import tqdm

class ProgressBar(tqdm):
    def __init__(self, total: int):
        super().__init__(total=total)
        self.idx = 0

    def increment(self, amount: int = 1):
        self.idx += amount
        self.update(amount)
