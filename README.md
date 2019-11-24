# WC_Sync

## Installing/Configuring WC_Sync
* Get an API token from Dropbox
** https://www.dropbox.com/developers/apps
** create an application (allow any directory)
** generate a token
** copy the token
* create a directory for the application (ie. /Applications/WC_Sync)
* copy sync_sample.ini to /Applications/WC_Sync/sync.ini
* edit sync.ini
** set db_token (from above)
** set src directory
** set src file list
** set dst folder
* edit org.wc.sync.plist
** change the installation directory
** set schedule

## Scheduling on OSX using launchd
```
sudo cp org.wc.sync.plist /Library/LaunchAgents
launchctl load /Library/LaunchAgents/org.wc.sync.plist
```

## To run it at any time
```
launchctl start org.wc.sync
```

