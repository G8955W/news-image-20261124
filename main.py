from pathlib import Path


source = Path(__file__).with_name("news.png")
destination = Path("/output/entry.png")
destination.parent.mkdir(parents=True, exist_ok=True)
# Copy the generated PNG bytes unchanged to the required output path.
destination.write_bytes(source.read_bytes())
print(f"{destination} {destination.stat().st_size}")
