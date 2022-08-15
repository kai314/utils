This repository provides some instructions on moving to a new Mac, which are not covered in the official manuals.
For a more extensive documentation of the developer setup, see [this repo](https://github.com/nicolashery/mac-dev-setup)

## Restoring keychain
Local objects (mostly Safari passwords) in keychain are not copied automatically via Migration Assistant (also not if you manually copy over the Library folder) if you have iCloud keychain disabled!
To copy them, you need to export them from the Keychain app as csv and re-import on the new Mac.

## Restoring Date Added metadata for files
Although date modified and date created are usually transferred automatically, the date added is set to the date the transfer took place.
If this is a problem (e.g. because you have your Downloads folder sorted by date added):

From the [utils/macos-get-timestamps](https://github.com/kai314/utils/tree/master/macos-restore-timestamps) folder, run `get_date_added.py` on the old Mac, copy the `date_added.json` to the new Mac and run `set_timestamps.py`.

## Installing applications
The checksum can be calculated with:
```bash
shasum -a 256 /path/to/file
```
where `-a` is short for `--algorithm`.

## Installing Homebrew
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Now, packages can be installed via Homebrew, e.g.:
```bash
brew install ffmpeg chromedriver handbrake
```

## Checking Apple Silicon Compatibility
You can check if an app is running via Rosetta 2 by opening the activity monitor and then under _kind_.
