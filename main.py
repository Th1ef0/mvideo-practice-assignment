from pathlib import Path


class TriangleCompression:
    def _cut(self, part: str) -> list[str]:
        grid = []
        part = list(part)
        i = 0
        while part:
            tr = []
            for _ in range(i * 2 + 1):
                tr.append(part.pop())
            grid.append("".join(tr))
            i += 1

        return grid

    def _join(self, grid: list[str]) -> str:
        # Обратная операция к _cut
        return "".join(row[::-1] for row in reversed(grid))

    def _flip(self, down) -> list[str]:
        l, r = 0, len(down) - 1

        while l < r:
            down[l], down[r] = down[r], down[l]
            l += 1
            r -= 1

        return down

    def _split(self, part: str) -> tuple[str, str, str, str]:
        left = []
        down = []
        right = []
        grid = self._cut(part=part)
        n = len(grid)

        top = grid[: n // 2]

        i = 0
        for row in grid[n // 2 :]:
            left.append(row[: i * 2 + 1])
            right.append(row[-i * 2 - 1 :])
            down.append(row[i * 2 + 1 : -i * 2 - 1])
            i += 1

        return right, self._flip(down), left, top

    def _merge(self, right, down, left, top) -> list[str]:
        # инверсия _split, возращает лист в изначальном порядке
        down = self._flip(down)
        bottom = [left[i] + down[i] + right[i] for i in range(len(left))]
        return top + bottom

    def _shrink_once(self, part: str):
        # Сжимает треугольник ровно на один уровень. Возвращает None, если элементы разные
        if len(part) == 4:
            return part[0] if len(set(part)) == 1 else None

        right, down, left, top = self._split(part=part)

        shrunk = []
        for grid in (right, down, left, top):
            smaller = self._shrink_once(part=self._join(grid))
            if smaller is None:
                return None
            shrunk.append(self._cut(part=smaller))

        return self._join(self._merge(*shrunk))

    def compress(self, part: str) -> str:
        # Пробуем сжимать уровень за уровнем, пока получается.
        while len(part) > 1:
            smaller = self._shrink_once(part=part)
            if smaller is None:
                break
            part = smaller

        return part


def main():
    source = Path("input.txt").read_text(encoding="utf-8").strip()
    result = TriangleCompression().compress(part=source)
    Path("output.txt").write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
