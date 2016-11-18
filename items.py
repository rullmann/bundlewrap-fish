pkg_dnf = {
    'fish': {},
}

directories = {}

files = {
    "/root/.config/fish/config.fish": {
        'source': "config.fish",
        'content_type': 'mako',
        'mode': "0640",
        'owner': "root",
        'group': "root",
        'needs': [
            "pkg_dnf:fish",
        ],
    },
}

actions = {
    'enable_fish': {
        'command': "chsh -s /usr/bin/fish root",
        'unless': "getent passwd root | cut -d: -f7 | grep /usr/bin/fish",
        'cascade_skip': False,
        'needs': [
            "pkg_dnf:fish",
        ],
    },
}

if node.metadata.get('fish', {}).get('install_fisherman', True):
    actions['install_fisherman'] = {
        'command': "curl -Lo ~/.config/fish/functions/fisher.fish --create-dirs git.io/fisherman",
        'unless': "test -f ~/.config/fish/functions/fisher.fish",
        'cascade_skip': False,
        'needs': [
            "pkg_dnf:fish",
            "pkg_dnf:curl",
        ],
    }
    for plugin in node.metadata.get('fish', {}).get('plugins', {}):
        actions['fisher_{}'.format(plugin)] = {
            'command': "sudo fish -c \"fisher {}\"".format(plugin),
            'unless': "grep {} ~/.config/fish/fishfile".format(plugin),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:fish",
                "action:install_fisherman",
                "action:enable_fish",
            ],
        }

for user in node.metadata.get('fish', {}).get('additional_users', {}):
    directories['/home/{}/.config/fish'.format(user)] = {
        'owner': user,
        'group': user,
        'needs': [
            "pkg_dnf:fish",
        ],
    }
    files['/home/{}/.config/fish/config.fish'.format(user)] = {
        'source': "config.fish",
        'mode': "0640",
        'owner': user,
        'group': user,
        'content_type': "mako",
        'needs': [
            "pkg_dnf:fish",
        ],
    }
    actions['enable_fish_{}'.format(user)] = {
        'command': "chsh -s /usr/bin/fish {}".format(user),
        'unless': "getent passwd {} | cut -d: -f7 | grep /usr/bin/fish".format(user),
        'cascade_skip': False,
        'needs': [
            "pkg_dnf:fish",
        ],
    }

    if node.metadata.get('fish', {}).get('install_fisherman', True):
        directories['/home/{}/.config/fisherman'.format(user)] = {
            'owner': user,
            'group': user,
            'needs': [
                "pkg_dnf:fish",
            ],
        }

        for plugin in node.metadata.get('fish', {}).get('plugins', {}):
            actions['install_fisherman_{}'.format(user)] = {
                'command': "sudo -u {} fish -c \"curl -Lo /home/{}/.config/fish/functions/fisher.fish --create-dirs git.io/fisherman\"".format(user, user),
                'unless': "test -f /home/{}/.config/fish/functions/fisher.fish".format(user),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:fish",
                    "pkg_dnf:curl",
                ],
            }
            actions['fisher_{}_{}'.format(user, plugin)] = {
                'command': "sudo -u {} fish -c \"fisher {}\"".format(user, plugin),
                'unless': "grep {} /home/{}/.config/fish/fishfile".format(plugin, user),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:fish",
                    "action:install_fisherman_{}".format(user),
                    "action:enable_fish_{}".format(user),
                ],
            }
