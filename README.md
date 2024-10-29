AireOS-to-9800.py

Before Migration

	Use the python script ”AireOS-to-9800.py” to get config files for new WLCs.
 	Configure new WLCs and make sure HA SSO is working.
		Paste the content of the config files on the new WLCs.
		Reload both WLC.
		During reload, connect RP cable.
		Make sure HA SSO is up by running command “show chassis”.
		Send controllers to the site together with console cable.
	Take backup of old WLC.
 
 During Migration
 
 	Delete old WLC from DNAC (not a full delete).
	Unplug old WLC.
 	Configure switches to use LACP.
	Plug in new WLC physically.
 	Add new WLC to DNAC and provision WLC.
	Make sure all APs join the new controller.
 	Provision all APs from DNAC.
	
After migration

 	Connect to all SSIDs and see that communication is working.
	
Rollback

	Unplug the new WLC and plug in old WLC to network.
 	Configure switches to have static EtherChannel.
