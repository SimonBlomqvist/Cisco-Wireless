AireOS-to-9800.py

Before Migration

  Use the python script ”AireOS-to-9800.py” to get config files for new WLCs.
  Configure new WLCs and make sure HA SSO is working.
    Reload both WLC.
  	During reload connect RP copper cable.
  	Make sure HA SSO is up by running command “show chassis”.
    Send controllers to the site together with console cable.
  Take backup of old WLC.
During Migration
  Delete old WLC from DNAC (not a full delete).
  Unplug old WLC.
  Reconfigure switches to use LACP mode active.
  Plug in new WLC physically.
  Add new WLC to DNAC and provision WLC.
  Make sure all APs join the new controller.
  Provision all APs from DNAC.
After migration
  Testing
  Connect to SSIDs and see that communication is working.
Rollback / Troubleshooting 
  Unplug the new WLC and plug in old WLC to network.
  Configure switches to have static EtherChannel.
