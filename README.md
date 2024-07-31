# BMLink
Cmd line tool to link BM talkgroups via BM APIv2


## BMLink - links and unlinks BM TGs by command line using APIv2

This is a simple Python3 script which links or unlinks BM talkgroups by command line.
You can call it manually to quickly link or unlink TGs to your repeater without login into the dashboard.
You can also call the script e.g. by crontab to schedule time dependent bookings of TGs.

Before you go to use this script, create an API key in your BM Selfcare profile and add it below.
You must also insert the DMR-ID of your repeater / hotspot below.

Please keep in mind that you can only modify repeaters where you are assigned as a sysop.
(And your own devices of course...)

The script will not only work on the particular repeater controller board, it can also be used on your Linux board at home or any other server system which provides a Python3 interpreter and has access to the BM API endpoint.


### Dependencies
pip3 install requests

### Usage

`bmlink.py start 2 263`&ensp;:&ensp;links TG263 to repeater's slot 2  
`bmlink.py stop 1 262`&emsp;:&ensp;unlinks TG262 from repeater's slot 1  
`bmlink.py list`&emsp;&emsp;&emsp;&emsp;:&ensp;lists currently linked TGs on repeater, sorted by slot no