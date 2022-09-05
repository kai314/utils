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
You can check if an app is running via Rosetta 2 by opening the activity monitor and then under _type_.


## Set up Time Machine
Time Machine is a very elegant way to make incremental backups of all required files.
However, there are some points that you need to keep in mind.

macOS supports HFS+ (macOS Extended) and APFS drives (since macOS Big Sur). If you need to keep files other than Time Machine files on the same drive, it is advisable to format the drive to APFS.
APFS does not just create volumes as in HFS+, but instead puts these volumes into containers.
This allows creating multiple volumes in a single (APFS) container and dynamically allocate disk space between volumes.
This is especially handy for putting Time Machine data along with other data on a volume, since resizing a Time Machine container is a pain.
So you need to create one container, and then one Time Machine volume and a data volume within it.
In case you have multiple containers and want to resize them (especially the container with the Time Machine volume):
```bash
diskutil ap resizeContainer <container ID> <size>
```
To completely fill out the remaining disk space, use 0 as size.
Note that the empty space must be located _after_ the container, since a container cannot be extended to the front.

If you are using a macOS version earlier than Big Sur, you can resize HFS+ volumes with the following command:
```bash
diskutil cs list
diskutil cs resizeStack <LVUUID> <size>
```
You can also delete HFS+ Time Machine volume groups with
```bash
diskutil cs deleteLVG <Group UUID>
```

- Time Machine only supports drives with _one_ container. [to be checked]
- Old HFS+ backup volumes cannot be converted into new APFS backup destinations, because they work completely different.

For those still using HFS+ on their Time Machine drive, here are some instructions on how to transfer backups to another volume (tested myself, but without any warranty):
1. in the Mac settings, disable automatic backup and add the new hard drive as Time Machine drive so that the drive is correctly formatted etc.
2. remove the new drive from Time Machine again
3. copy over the `Backups.backupdb` folder (do not use `cp -R` here because of the symlinks, instead use `cmd+C`, `option+cmd+shift+V` for exact copy)
4. add the drive in Time Machine again

## Compare folder with its Time Machine backup
```bash
tmutil compare <path1> <path2> | grep -E ^-
```

The symbols in front of the files have the following meaning:
- `!` file has changed
- `-` file is missing
- `+` file is new
