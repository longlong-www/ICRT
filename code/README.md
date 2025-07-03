# Title

## Requirements

To install requirements:

```setup
pip install -r requirements.txt
```

## How to Use

### 1.Prepare Your Data

Each script expects a `config*.json` file with match data. Example:

```json
{
  "data": [
    ["method1", "method2", 15, 10],
    ["method2", "method3", 12, 8]
  ]
}
```

- Each entry: `[playerA, playerB, winsA, winsB]`
- For `configElo.json`, you must also include a `"methods"` list:
  ```json
  "methods": ["method1", "method2", "method3"]
  ```

### 2.Run Scripts

```bash
python Elo.py
python HodgeRank.py
python RankCentrality.py
```

Each script will print the final ranking results.



