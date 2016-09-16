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

files = {
    "/root/.config/fish/config.fish": {
        'source': "config.fish",
        'content_type': 'mako',
        'mode': "0640",
        'owner': "root",
        'group': "root",
        'needs': [
            "pkg_yum:fish",
        ],
    },
}

actions = {
    'enable_fish': {
        'command': "chsh -s /usr/bin/fish root",
        'unless': "getent passwd root | cut -d: -f7 | grep /usr/bin/fish",
        'cascade_skip': False,
        'needs': [
            "pkg_yum:fish",
        ],
    },
}

if node.metadata.get('fish', {}).get('install_fisherman', True):
    actions['install_fisherman'] = {
        'command': "curl -Lo ~/.config/fish/functions/fisher.fish --create-dirs git.io/fisherman",
        'unless': "test -f ~/.config/fish/functions/fisher.fish",
        'cascade_skip': False,
        'needs': [
            "pkg_yum:fish",
            "pkg_yum:curl",
        ],
    }
    for plugin in node.metadata.get('fish', {}).get('plugins', {}):
        actions['fisher_{}'.format(plugin)] = {
            'command': "sudo fish -c \"fisher {}\"".format(plugin),
            'unless': "grep {} ~/.config/fish/fishfile".format(plugin),
            'cascade_skip': False,
            'needs': [
                "pkg_yum:fish",
                "action:install_fisherman",
                "action:enable_fish",
            ],
        }
