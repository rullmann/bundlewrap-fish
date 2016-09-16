# bundlewrap-fish

`bundlewrap-fish` will install and configure [fish shell](https://fishshell.com/) as well as [fisherman](http://fisherman.sh/), a package manager for fish.

## Compatibility

This bundle has been tested on the following systems:

| OS          | `[x]` |
| ----------- | ----- |
| CentOS 7    | `[x]` |
| Fedora 24   | `[x]` |
| RHEL 7      | `[ ]` |
| Fedberry 23 | `[ ]` |

## Requirements

* Bundles:
  * [epel](https://github.com/rullmann/bundlewrap-centos-epel)
     * Required for RHEL and CentOS, but not Fedora
  * [bundlewrap-centos-packages-base](https://github.com/rullmann/bundlewrap-centos-packages-base)
    * Only requires `pkg_yum:curl`, if you define it somewhere else that's fine

## Metadata

    'metadata': {
        'fish': {
            'additional_users': ["youarenotroot"], # optional
            'plugins': ["oh-my-fish/plugin-extract", "oh-my-fish/plugin-hash"], #optional
        },
    }

# Additional notes

* On Fedora 24 `chsh` is not part of `util-linux`. You'll need to install `util-linux-user` to enable fish
  * For example this can be done by using the [yum](https://github.com/rullmann/bundlewrap-yum)-bundle