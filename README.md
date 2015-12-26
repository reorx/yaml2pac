# yaml2pac

Generate high efficiency pac file from a yaml-based protocol.

`yaml2pac` is not only a Python package, a cli command, but also
a bunch of directives & terms organized in yaml. The protocol
is ease to write, very intuitive, and can handle complicated situations easily.

The reason why choosing yaml to be the carrier of the protocol is because
yaml is text based, and it has great readability, which means you can maintain
your rules in a text file, in an organized way, rather than in those proxy
programs separately. This can avoid the cost of backing up and updating
in many places when a new rule comes in.

There are already some black/white list of massive website domains, they are useful if
you don't want to consider too much at first, but gradually you'll find that
not knowing whether this site is going through a proxy or not is very annoying
sometimes, it's hard to have a conscious mind when look into the huge list of
domains, not to say modifying the pac file that is hard to debug and verify.

yaml2pac is created to solve this problem, to use yaml2pac, you need to change
your mind, throw away gfwlist, write your own rules, control the pac file like a boss.
Get start and have a try, I bet you'll like it :)

## Install

Install with pip:

```
$ pip install yaml2pac
```

Cli usage:

```
$ yaml2pac -h
usage: yaml2pac [-h] YAML

Generate pac file from yaml file

positional arguments:
  YAML        The input yaml file

optional arguments:
  -h, --help  show this help message and exit

Example:
  yaml2pac myrules.yaml > ~/.ShadowsocksX/gfwlist.js
```

## Protocol

The content of `yaml2pac` protocol must be a valid yaml file at first,
a minimal but complete `yaml2pac` yaml file looks like this:

```yaml
meta:
  default: direct
  proxy:
    default: "SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;"
    https: "HTTPS your-proxy.io:443;"
proxy:
  domain:
    - twitter.com
  keyword:
    - youtube: https
```

This yaml means:
By default, all traffic will go directly without proxy, if the host of request
matches twitter.com by suffix (twitter.com or api.twitter.com), the traffic will
go through the default proxy, which is a socks or socks5 proxy,
and will fallback to be direct if not available;
if the host matches youtube by keyword, the traffic will go through the proxy named
`https`.

Each directive will be explained detailedly below.

### `meta`

`meta` contains the metadata of the yaml file, it has these properties:

#### `default`

defines where the traffic goes by default, if value is `direct`, the traffic goes
directly with proxy; The value could also be `proxy`, means to go through the default
proxy, or exactly the name of a proxy, like `https` in the example above.
  
#### `proxy`

defines the proxy to be used, `proxy` should at least have a `default` property.
The value of the properties should be in a format of `<proxy_type> + <address:port>; [ ... ]`.

originally pac only defined 3 kind of `proxy_type`:
- DIRECT
- PROXY
- SOCKS
(see [netscape doc])
most systems (like OS X) only support these 3 `proxy_type`.

Chrome extended `proxy_type` by two more:
- HTTPS
- SOCKS5
(see [chromium doc] & [chrome extension doc])

So if you want to create pac file that are effective for both system and chrome,
you need to define a proxy with fallback, e.g:

```yaml
proxy:
  # A SOCKS5 fallback to SOCK
  - ss: SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080;
  # A HTTPS fallback to PROXY
  - https: HTTPS your-proxy.io:443; PROXY your-poor-http-proxy.io;
```

If your yaml contains SOCKS5 or HTTPS proxy definitions without a proper fallback,
warnings will show up when generating pac file, you can use `-i` option to disable
the warning.

### `proxy`

#### `domain`

#### `keyword`

#### `ip`

[netscape doc]: http://findproxyforurl.com/netscape-documentation/
[chromium doc]: https://www.chromium.org/developers/design-documents/secure-web-proxy
[chrome extension doc]: https://developer.chrome.com/extensions/proxy
