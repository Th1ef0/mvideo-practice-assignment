from pathlib import Path

Grid = list[str]
Parts = tuple[Grid, Grid, Grid, Grid]


class TriangleCompression:
    def _cut(self, triangle: str) -> Grid:
        chars = list(triangle)
        grid = []
        row_index = 0
        while chars:
            row = [chars.pop() for _ in range(row_index * 2 + 1)]
            grid.append("".join(row))
            row_index += 1

        return grid

    def _join(self, grid: Grid) -> str:
        return "".join(row[::-1] for row in reversed(grid))

    def _split(self, triangle: str) -> Parts:
        grid = self._cut(triangle=triangle)
        n = len(grid)

        top = grid[: n // 2]
        left, down, right = [], [], []
        for i, row in enumerate(grid[n // 2 :]):
            left.append(row[: i * 2 + 1])
            right.append(row[-i * 2 - 1 :])
            down.append(row[i * 2 + 1 : -i * 2 - 1])

        # Средний треугольник перевёрнут, разворот приводит его к обычной ориентации,
        # чтобы обрабатывать все четыре части одинаково.
        return right, down[::-1], left, top

    def _merge(self, right: Grid, down: Grid, left: Grid, top: Grid) -> Grid:
        down = down[::-1]
        bottom = [left[i] + down[i] + right[i] for i in range(len(left))]
        return top + bottom

    def _shrink_once(self, triangle: str) -> str | None:
        if len(triangle) == 4:
            return triangle[0] if len(set(triangle)) == 1 else None

        right, down, left, top = self._split(triangle=triangle)

        shrunk = []
        for grid in (right, down, left, top):
            smaller = self._shrink_once(triangle=self._join(grid))
            # Целое сжимается, только если сжимается каждая из четырёх частей.
            if smaller is None:
                return None
            shrunk.append(self._cut(triangle=smaller))

        return self._join(self._merge(*shrunk))

    def compress(self, triangle: str) -> str:
        while len(triangle) > 1:
            smaller = self._shrink_once(triangle=triangle)
            if smaller is None:
                break
            triangle = smaller

        return triangle


def main():
    source = Path("input.txt").read_text(encoding="utf-8").strip()
    result = TriangleCompression().compress(triangle=source)
    Path("output.txt").write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()


# на решение задачи ушло 3 часа 23 минуты