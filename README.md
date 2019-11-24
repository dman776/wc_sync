# WC_Sync

## Using WC_Sync
* Get an API token from Dropbox (allow any directory)
* copy sync_sample.ini to sync.ini
* edit sync.ini
* edit org.wc.sync.plist and change the installation directory

## Scheduling on OSX using launchd
```
sudo cp org.wc.sync.plist /Library/LaunchAgents
launchctl load /Library/LaunchAgents/org.wc.sync.plist
```

## To run it at any time
```
launchctl start org.wc.sync
```

