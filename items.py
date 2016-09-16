pkg_yum = {}

# Make sure you've added the epel-bundle to the nodes if on CentOS/RHEL!
if node.has_bundle("epel"):
    pkg_yum['fish'] = {
        'needs': [
            "pkg_yum:epel-release",
        ],
    }
else:
    pkg_yum['fish'] = {}

