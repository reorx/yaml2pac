(function () {
    // Convert an IP to a long integer.
    function ip2long( a, b, c, d ) {
        for (
            c = b = 0;
            d = a.split('.')[b++];
            c +=
            d >> 8
                |
                b > 4 ?
                NaN
                :
                d * (1 << -8 * b)
        )
            d = parseInt(
                    +d
                    &&
                    d
            );
        return c
    }


    // Determine whether the given IP falls within the specified CIDR range.
    function cidr_match(ip, range) {
        // If the range doesn't have a slash it will only match if identical to the IP.
        if (range.indexOf('/') < 0)
            return (ip === range);

        var _sp = range.split('/'),
            subnet = ip2long(_sp[0]),
            bits = Number(_sp[1]),
            mask = -1 << (32 - bits);
        ip = ip2long(ip);
        subnet &= mask;
        return (ip & mask) === subnet;
    };


    // Export our public API
    var exports = {};
    exports.cidr_match = cidr_match;
    exports.ip2long = ip2long;

    module.exports = exports;
}());