import argparse
import subprocess
import os
import shutil
from pathlib import Path

def main():
    import sys
    from datetime import datetime
    with open("commandHistory.log", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {' '.join(sys.argv)}\n")
        
    parser = argparse.ArgumentParser(description="Generate map posters in all themes and save to output folder.")
    parser.add_argument("-c", "--city", required=True, help="City name")
    parser.add_argument("-C", "--country", required=True, help="Country name")
    # allow passing other arguments if needed, but keeping it simple for now.
    args = parser.parse_args()

    city = args.city
    country = args.country

    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print(f"Generating posters for {city}, {country} in all themes...")
    
    # Run the existing script with --all-themes
    # We use the python executable from the current environment
    import sys
    python_exe = sys.executable
    
    cmd = [
        python_exe, "create_map_poster.py",
        "-c", city,
        "-C", country,
        "--all-themes"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating posters: {e}")
        return

    # Move generated posters to 'output/<city>' folder
    # Format of poster names: {city}_{theme}_{YYYYMMDD_HHMMSS}.png
    # City in filename is lowercased and spaces replaced with underscores
    city_slug = city.lower().replace(" ", "_")
    
    # Target directory for this city's posters
    target_dir = output_dir / city
    target_dir.mkdir(exist_ok=True)
    
    posters_dir = Path("posters")
    moved_count = 0
    if posters_dir.exists():
        # Find files matching the city
        pattern = f"{city_slug}_*.png"
        for filepath in posters_dir.glob(pattern):
            dest = target_dir / filepath.name
            shutil.move(str(filepath), str(dest))
            print(f"Moved {filepath.name} to {target_dir} folder.")
            moved_count += 1

    if moved_count > 0:
        print(f"\nSuccess! {moved_count} posters for {city} have been saved to the '{target_dir}' directory.")
    else:
        print(f"\nNo posters were found for {city} in the 'posters' directory.")

if __name__ == "__main__":
    main()
