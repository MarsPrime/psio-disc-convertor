# PSIO Disc Convertor

This script just converts PS1 disc images into PSIO format.
It's just wrapper for this programs:

- putnam/binmerge : for merging splited .bin files
- NRGHEAD/Cue2Cu2 : for fixing CD music

## Usage
```bash 

python3 main.py /game_file.cue -o /output_directory
uv run main.py /game_file.cue -o /output_directory

```
**-o** - change output directory, defalult is it ./converted (at the same direcory as executable)


Feel free to review and change code!

## Special Thanks

- putnam
- NRGHEAD
