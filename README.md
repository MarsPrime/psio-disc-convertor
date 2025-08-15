# PSIO Disc Convertor

This script just converts PS1 disc images into PSIO format.
It's just wrapper for this programs, sites and repositories:

- putnam/binmerge : for merging splited .bin files
- NRGHEAD/Cue2Cu2 : for fixing CD music
- xlenore/psx-covers : game covers
- https://psxdatacenter.com/ : I took from them table of discs codes and disc names 

## How it work
1) Program checks all arguments that was entered in terminal;
2) Program scans files in input directory;
3) Program replace files in output directory or merge .bin files if needed;
4) Program make .cu2 sheets for images with CD audio;
5) Program generate DB with game IDs, Titles and Languages (if DB is not created);
6) Program create game covers for every game.

## Usage
```bash
# uv
# run script from /scripts directory
uv run main.py /input_directory -o /output_directory
```
**-o** - change output directory, defalult is it ./converted (at the same directory as executable file)

## Dependenses

| Package        | Version | Usage                                |
| -------------  | ------- | ------------------------------------ |
| beautifulsoup4 | 4.13.4  | HTML parsing for data to GameList.db |
| colorama       | 0.4.6   | Colors in terminal                   |
| pillow         | 11.3.0  | Resize and convert cover images      |
| termcolor      | 3.1.0   | Colors in terminal                   |


## Pros 
- Program converts all files automaticly: all program need is enter directory where image files is and directory where he wants files to contain after convertation;
- Program works without connection to Internet: all images and databases are local;
- Program uses Python: it's very simple to modificate code if needed;

## Cons
- Only CLI (Command Line Interface): I think about creating UI in QT but for now this is what it is;
- My code: It's my first open source project and due my inexperince some things in file or code can be wierd or stupid, but I work on them;
- Program is testing: I need more time for testing and more people to test my project to collect new ideas and solve problems that I don't see now;
- Platforms: For now I test project on my main PC with GNU/Linux Debian 12. Testing for Windows will be soon (I need some time to make VM and configure it). Testing for MacOS is not that neccessary (because both Linux and MacOS are Unix and works about the same, I guess).

## Issues

- [ ] Some games after converting has wierd sound (some track starts, plays about 10 seconds and then stops and plays again). This problem can be related with bad image files or some issues when game have merged in one bin file (I'm not sure about that)

## About contributing
Feel free to review and change code!

## Special Thanks

- putnam
- NRGHEAD
- xlenore

