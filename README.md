##################################
#           README               #
##################################

INSTALL

# 1.) Install python 3.6
# 2.) Install pip (python get-pip.py)
# 3.) Install 'requests' library (pip install requests)
# 4.) Put 1 video url per line in the videoURLS.txt file

EXECUTION

# 1.) python gdcVaultVideoDownloader.py "username" "password" "quality"
-quality must be set to:
	"low"  -> 1024x576 ~ 200MB per hour
	"high" -> 1280x720 ~ 527MB per hour

-year must be set to:
	"17" -> 2017 video
	"18" -> 2018 video

SUPPORT

Windows is currently the only supported platform. And that's only for the fact that I ensure the filename works with windows. Feel free to update the script to account for other operating systems.