# auto-pinging
Small script using the at utility to automate pinging on mailing lists

This script is called with 3 different behaviors during the lifetime of a patch:
* first it is called "manually" to add a new patch to be pinged. It will add the patch to a file that contains all patches to be pinged, and a date 2 weeks from the date when the patch is added
* The next call is through the cronjob that happens once a week. If the moment when the script is called is after the saved date for a given patch, it will be pinged
* Finally, when the patch is pushed, this script is called one last time to remove the patch from the list of patches to be pinged.

The list of patches is stored in `$HOME/.patches.csv`
There are 3 columns:
BRANCH_NAME, EMAIL_ID, PING_BY_DATE

BRANCH_NAME is how the script finds patch series to inform the user that they have to be pinged (if in remind mode) and how they are identified to be removed. This is used to facilitate integration with git hooks.
EMAIL_ID is how the script know where to send a ping email, if one is to be  sent.
PING_BY_DATE tells the cronjob when to start sending the pings.

STRETCH GOAL:
    add an option to "pause" a ping, which skips the next time the patch would be pinged.
