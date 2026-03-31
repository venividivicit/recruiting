from bisect import bisect_right
from collections import defaultdict


class QRangeStore:
    """
    Optimized range store:
    - write: append ranges [low, high) per agent
    - read: binary-search latest candidate interval per agent
    Public API remains:
      store[low, high] = value
      store[t] -> list[dict]
    """

    def export(self):
        rows = []
        for agent_id, lows in self._lows.items():
            highs = self._highs[agent_id]
            vals = self._vals[agent_id]
            for i in range(len(lows)):
                rows.append((lows[i], highs[i], {agent_id: vals[i]}))
        return rows

    def __init__(self):
        self._lows = defaultdict(list)   # agent_id -> [low...]
        self._highs = defaultdict(list)  # agent_id -> [high...]
        self._vals = defaultdict(list)   # agent_id -> [state...]
        self._count = 0

    def __setitem__(self, rng, value):
        try:
            low, high = rng
        except (TypeError, ValueError):
            raise IndexError("Invalid Range: must provide a low and high value.")

        if not low < high:
            raise IndexError("Invalid Range.")

        # value expected to be dict like {"Body1": {...}, "Body2": {...}}
        for agent_id, agent_state in value.items():
            self._lows[agent_id].append(low)
            self._highs[agent_id].append(high)
            self._vals[agent_id].append(agent_state)
            self._count += 1

    def __getitem__(self, key):
        ret = []
        for agent_id in self._lows.keys():
            lows = self._lows[agent_id]
            i = bisect_right(lows, key) - 1
            if i >= 0 and key < self._highs[agent_id][i]:
                ret.append({agent_id: self._vals[agent_id][i]})

        if not ret:
            raise IndexError("Not found.")
        return ret

    def __len__(self):
        return self._count